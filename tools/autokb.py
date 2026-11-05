#!/usr/bin/env python3
"""Otonom araştırma sistemi komut satırı aracı. `kb.py` ile aynı bilgi tabanı üzerinde çalışır.

Komutlar:
  daily                     Günlük çalışma: topla → tekilleştir → sınıflandır → arşivle → keşif → bakım → reindex
  backfill ID [ID ...]      Belirli teknolojiler için önemli (çok atıf alan) tarihsel çalışmaları topla
  classify --title T [--abstract A]   Sınıflandırıcıyı tek kayıt üzerinde dene
  eval FILE                 Etiketli değerlendirme setinde sınıflandırma doğruluğunu ölç
  queue list|resolve N --tech ID|drop N
  candidates list|verify KEY --parent ID [--title-tr T]|reject KEY --reason R
  maintain [--node ID] [--draft-json F --sources-json F] [--limit N]
  proposals list|apply FILE|reject FILE
  status                    Durum özeti

Ortam değişkenleri: OPENALEX_API_KEY (önerilir, ücretsiz), KB_CONTACT_EMAIL (Crossref/OpenAlex nazik havuz),
ANTHROPIC_API_KEY (isteğe bağlı LLM modu), KB_LLM_MODEL, KB_MAX_ARCHIVE_PER_RUN ve diğerleri (config.py).
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import kb  # noqa: E402
from kbresearch.config import Config  # noqa: E402
from kbresearch.http import Http  # noqa: E402
from kbresearch.state import State, RunLock, load_json  # noqa: E402


def make(args):
    if args.root:
        kb.set_root(args.root)
    cfg = Config(kb.ROOT)
    return cfg, Http(cfg.user_agent)


def make_llm(cfg, run_counter):
    from kbresearch.llm import LLM
    llm = LLM(cfg, run_counter)
    return llm if llm.available else None


def cmd_daily(args):
    from kbresearch.pipeline import Run
    cfg, http = make(args)
    with RunLock(cfg.state_dir):
        run = Run(cfg, http, sources=tuple(args.sources.split(",")))
        if not args.no_llm:
            run.llm = make_llm(cfg, run.counter)
        stats = run.daily(backfill=not args.no_backfill, maintain=not args.no_llm)
    print(json.dumps({k: v for k, v in stats.items() if k != "maintained"}, ensure_ascii=False, indent=1))
    # 0: sorunsuz; 2: kısmi (bazı kaynaklar/adımlar başarısız, alınan sonuçlar geçerli)
    return 2 if stats["errors"] else 0


def cmd_backfill(args):
    from kbresearch.pipeline import Run
    cfg, http = make(args)
    with RunLock(cfg.state_dir):
        run = Run(cfg, http)
        run.backfill(args.ids, args.per_tech)
        run.finish()
    print(json.dumps({k: run.stats[k] for k in ("created", "merged", "unchanged", "backfill_created", "errors")},
                     ensure_ascii=False))
    return 2 if run.stats["errors"] else 0


def cmd_classify(args):
    from kbresearch.classify import Classifier
    from kbresearch.records import new_record
    make(args)
    clf = Classifier(kb.Tree(with_research=False))
    r = new_record(title=args.title, abstract=args.abstract,
                   categories=[c for c in (args.categories or "").split(",") if c])
    print(json.dumps(clf.classify(r), ensure_ascii=False, indent=1))


def cmd_eval(args):
    from kbresearch.classify import Classifier
    make(args)
    tree = kb.Tree(with_research=False)
    clf = Classifier(tree)
    items = [json.loads(l) for l in open(args.file, encoding="utf-8") if l.strip()]
    res = {"high": [0, 0, 0], "medium": [0, 0, 0], "low": [0, 0, 0]}  # [toplam, doğru, kabul edilebilir]
    wrong = []
    for it in items:
        c = clf.classify(it["record"])
        gold = set(it["gold"])
        ok_chain = gold | {a for g in gold if g in tree.nodes for a in tree.ancestors(g)}
        b = res[c["confidence"]]
        b[0] += 1
        if c["primary"] in gold:
            b[1] += 1
            b[2] += 1
        elif c["primary"] in ok_chain:
            b[2] += 1  # doğru dalın daha genel bir üst düğümü
        elif c["confidence"] == "high":
            wrong.append((it["record"]["title"], c["primary"], it["gold"]))
    for k, (n, ok, acc) in res.items():
        if n:
            print(f"{k:6s} n={n:3d}  tam doğru={ok / n:.2f}  doğru dalda (tam+üst)={acc / n:.2f}")
    hi = res["high"]
    print(f"Arşive giren (high) kayıtlarda kesinlik: {hi[2] / hi[0]:.2f} (doğru dal), {hi[1] / hi[0]:.2f} (tam)" if hi[0] else "high yok")
    for w in wrong:
        print("YANLIŞ:", w)


def cmd_queue(args):
    from kbresearch.archive import Archive, ReviewQueue
    cfg, _ = make(args)
    tree = kb.Tree()
    q = ReviewQueue(cfg.review_dir, cfg.review_queue_max)
    if args.action == "list":
        for i, it in enumerate(q.items):
            print(i, it.get("suggested"), "|", it.get("title"))
        return
    item = q.items[args.n]
    if args.action == "resolve":
        if args.tech not in tree.nodes:
            raise SystemExit(f"Teknoloji yok: {args.tech}")
        st, path = Archive(tree, cfg.today).upsert(item["record"], {"primary": args.tech, "confidence": "high",
                                                                     "method": "human", "related": []})
        print(st, path)
    q.pop(args.n)
    q.save(tree)
    kb.cmd_reindex()


def cmd_candidates(args):
    from kbresearch.classify import Classifier
    from kbresearch.discovery import Discovery
    cfg, _ = make(args)
    tree = kb.Tree()
    d = Discovery(cfg, tree, Classifier(tree))
    if args.action == "list":
        for k, c in d.cands.items():
            print(f"{c['status']:9s} {k} -> {c.get('parent_suggestion')} ({(c.get('evidence') or {}).get('papers')} makale)")
        return
    if args.action == "verify":
        nid, path = d.verify(args.key, args.parent, args.title, args.title_tr)
        print("Oluşturuldu:", nid, os.path.relpath(path, kb.ROOT))
    else:
        d.reject(args.key, args.reason)
    d.save()
    kb.cmd_reindex()


def cmd_maintain(args):
    from kbresearch import maintainer as M
    from kbresearch.sources import openalex
    cfg, http = make(args)
    tree = kb.Tree()
    st = State(cfg.state_dir, cfg.today)
    counter = st.day_counter()
    if args.draft_json:  # dışarıda (ör. elle ya da başka bir oturumda) hazırlanmış taslak + kaynaklar
        draft = json.load(open(args.draft_json, encoding="utf-8"))
        sources = json.load(open(args.sources_json, encoding="utf-8"))
        print(M.fill_node(cfg, tree, args.node, draft=draft, sources=sources))
    else:
        llm = make_llm(cfg, counter)
        if not llm:
            raise SystemExit("LLM yok: ANTHROPIC_API_KEY ayarlayın ve `pip install anthropic` çalıştırın, "
                             "ya da --draft-json/--sources-json kullanın.")
        nodes = [args.node] if args.node else M.priority_queue(tree, args.limit)
        for nid in nodes:
            print(M.fill_node(cfg, tree, nid, llm, http, openalex))
        st.save_counters()
    kb.cmd_reindex()


def cmd_proposals(args):
    from kbresearch import maintainer as M
    cfg, _ = make(args)
    if args.action == "list":
        for p, m in M.list_proposals(cfg):
            print(m.get("kind"), m.get("technology_id"), os.path.relpath(p, kb.ROOT))
        return
    if args.action == "apply":
        M.apply_proposal(cfg, kb.Tree(), args.file)
    else:
        M.set_proposal_status(args.file, "rejected")
    kb.cmd_reindex()


def cmd_status(args):
    cfg, _ = make(args)
    st = State(cfg.state_dir, cfg.today)
    print(json.dumps({"checkpoints": st.checkpoints, "today": st.counters.get(cfg.today.isoformat()),
                      "review_queue": len(load_json(os.path.join(cfg.review_dir, "classification-queue.json"), [])),
                      "candidates": len(load_json(os.path.join(cfg.review_dir, "technology-candidates.json"), {}))},
                     ensure_ascii=False, indent=1))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("daily")
    p.add_argument("--sources", default="arxiv,openalex")
    p.add_argument("--no-llm", action="store_true")
    p.add_argument("--no-backfill", action="store_true")
    p.set_defaults(fn=cmd_daily)
    p = sub.add_parser("backfill")
    p.add_argument("ids", nargs="+")
    p.add_argument("--per-tech", type=int)
    p.set_defaults(fn=cmd_backfill)
    p = sub.add_parser("classify")
    p.add_argument("--title", required=True)
    p.add_argument("--abstract")
    p.add_argument("--categories", help="ör. arXiv:cs.CR")
    p.set_defaults(fn=cmd_classify)
    p = sub.add_parser("eval")
    p.add_argument("file")
    p.set_defaults(fn=cmd_eval)
    p = sub.add_parser("queue")
    p.add_argument("action", choices=["list", "resolve", "drop"])
    p.add_argument("n", type=int, nargs="?")
    p.add_argument("--tech")
    p.set_defaults(fn=cmd_queue)
    p = sub.add_parser("candidates")
    p.add_argument("action", choices=["list", "verify", "reject"])
    p.add_argument("key", nargs="?")
    p.add_argument("--parent")
    p.add_argument("--title")
    p.add_argument("--title-tr")
    p.add_argument("--reason", default="")
    p.set_defaults(fn=cmd_candidates)
    p = sub.add_parser("maintain")
    p.add_argument("--node")
    p.add_argument("--limit", type=int, default=3)
    p.add_argument("--draft-json")
    p.add_argument("--sources-json")
    p.set_defaults(fn=cmd_maintain)
    p = sub.add_parser("proposals")
    p.add_argument("action", choices=["list", "apply", "reject"])
    p.add_argument("file", nargs="?")
    p.set_defaults(fn=cmd_proposals)
    sub.add_parser("status").set_defaults(fn=cmd_status)
    args = ap.parse_args(argv)
    return args.fn(args) or 0


if __name__ == "__main__":
    sys.exit(main())
