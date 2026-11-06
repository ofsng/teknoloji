"""Otonom araştırma sistemi testleri (ağ erişimi gerektirmez).

Çalıştırma: python3 -m unittest discover -s tools/tests -v
"""
import json
import os
import shutil
import sys
import tempfile
import unittest
import urllib.error
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import kb  # noqa: E402
from kbresearch import maintainer as M  # noqa: E402
from kbresearch.archive import Archive  # noqa: E402
from kbresearch.classify import Classifier  # noqa: E402
from kbresearch.config import Config  # noqa: E402
from kbresearch.discovery import Discovery, acronym_definitions  # noqa: E402
from kbresearch.http import Http, Response, SourceUnavailable  # noqa: E402
from kbresearch.llm import LLM, BudgetExceeded  # noqa: E402
from kbresearch.pipeline import Run  # noqa: E402
from kbresearch.records import dedupe_batch, new_record  # noqa: E402
from kbresearch.sources import crossref  # noqa: E402

TODAY = date(2026, 11, 5)
TAXONOMY = [  # (göreli yol, id, title, title_tr, parent, refs, aliases)
    ("Bilgisayar-Bilimleri", "computer-science", "Computer Science", "Bilgisayar Bilimleri", "root", ["arXiv:cs"], []),
    ("Bilgisayar-Bilimleri/Kriptografi", "cryptography", "Cryptography", "Kriptografi", "computer-science",
     ["arXiv:cs.CR"], []),
    ("Bilgisayar-Bilimleri/Kriptografi/Sifir-Bilgi-Ispatlari", "zero-knowledge-proofs", "Zero-Knowledge Proofs",
     "Sıfır Bilgi İspatları", "cryptography", [], ["ZKP"]),
    ("Bilgisayar-Bilimleri/Kriptografi/Sifir-Bilgi-Ispatlari/zk-SNARK", "zk-snarks", "zk-SNARKs", "zk-SNARK",
     "zero-knowledge-proofs", [], []),
    ("Bilgisayar-Bilimleri/Yapay-Zeka", "artificial-intelligence", "Artificial Intelligence", "Yapay Zeka",
     "computer-science", ["arXiv:cs.AI"], ["AI"]),
    ("Bilgisayar-Bilimleri/Yapay-Zeka/Makine-Ogrenmesi", "machine-learning", "Machine Learning", "Makine Öğrenmesi",
     "artificial-intelligence", ["arXiv:cs.LG"], []),
    ("Bilgisayar-Bilimleri/Yapay-Zeka/Makine-Ogrenmesi/Derin-Ogrenme", "deep-learning", "Deep Learning",
     "Derin Öğrenme", "machine-learning", [], []),
    ("Bilgisayar-Bilimleri/Yapay-Zeka/Makine-Ogrenmesi/Derin-Ogrenme/Cizge-Sinir-Aglari", "graph-neural-networks",
     "Graph Neural Networks", "Çizge Sinir Ağları", "deep-learning", [], ["GNN"]),
    ("Bilgisayar-Bilimleri/Yapay-Zeka/Makine-Ogrenmesi/Derin-Ogrenme/Transformer-Mimarileri",
     "transformer-architectures", "Transformer Architectures", "Transformer Mimarileri", "deep-learning", [], []),
    ("Bilgisayar-Bilimleri/Yapay-Zeka/Makine-Ogrenmesi/Derin-Ogrenme/Mixture-of-Experts", "mixture-of-experts",
     "Mixture of Experts", "Uzmanlar Karışımı", "deep-learning", [], ["MoE"]),
    ("Fizik", "physics", "Physics", "Fizik", "root", ["arXiv:physics"], []),
    ("Fizik/Kuantum-Mekanigi", "quantum-mechanics", "Quantum Mechanics", "Kuantum Mekaniği", "physics",
     ["arXiv:quant-ph"], []),
]


def build_kb(root):
    kb.set_root(root)
    for rel, nid, title, tr, parent, refs, aliases in TAXONOMY:
        d = os.path.join(root, rel)
        os.makedirs(os.path.join(d, kb.RESEARCH_DIR), exist_ok=True)
        depth = len(rel.split("/"))
        meta = {"id": nid, "title": title, "title_tr": tr, "type": kb.node_type(depth), "parent": parent,
                "status": "established", "classification_confidence": "high", "aliases": aliases, "related": [],
                "depends_on": [], "applied_in": [], "classification_refs": refs, "content_verified": False,
                "created": "2026-11-05"}
        kb.write(os.path.join(d, kb.INDEX), kb.new_index_text(meta))
    kb.cmd_reindex()


def rec(**kw):
    base = dict(title="Untitled", authors=["Ada Lovelace"], published_date="2026-11-01", abstract=None,
                abstract_license="cc0-1.0 (arxiv metadata)", source_ids=["test:1"], language="en")
    base.update(kw)
    return new_record(**base)


class FakeOpener:
    """URL alt dizisi -> yanıt (ya da istisna) eşlemesi; çağrıları kaydeder."""

    def __init__(self, routes):
        self.routes, self.calls = routes, []

    def __call__(self, req, timeout):
        url = req.full_url
        self.calls.append(url)
        for key, val in self.routes:
            if key in url:
                if callable(val):
                    val = val(url)
                if isinstance(val, Exception):
                    raise val
                return val
        return Response(404, {}, b"{}")


def json_resp(obj, status=200):
    return Response(status, {}, json.dumps(obj).encode())


def atom(entries, total=None):
    items = "".join(f"""<entry><id>http://arxiv.org/abs/{e['id']}v1</id><title>{e['title']}</title>
<summary>{e.get('abstract', '')}</summary><published>{e.get('date', '2026-11-02')}T10:00:00Z</published>
<updated>{e.get('date', '2026-11-02')}T10:00:00Z</updated><author><name>{e.get('author', 'Ada Lovelace')}</name></author>
<arxiv:primary_category term="{e.get('cat', 'cs.LG')}"/><category term="{e.get('cat', 'cs.LG')}"/></entry>"""
                    for e in entries)
    return Response(200, {}, f"""<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom"
xmlns:arxiv="http://arxiv.org/schemas/atom" xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">
<opensearch:totalResults>{total if total is not None else len(entries)}</opensearch:totalResults>{items}</feed>""".encode())


GNN_ABS = ("We propose a graph neural network architecture for molecular property prediction. Graph neural "
           "networks aggregate messages over graph neighborhoods; our deep learning model improves accuracy.")


class Base(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="kbtest-")
        build_kb(self.root)
        self.cfg = Config(self.root, today=TODAY)
        self.cfg.max_archive, self.cfg.max_per_tech = 20, 10
        self.cfg.arxiv_page_size = 2
        self.cfg.openalex_max_pages = 1
        self.cfg.max_catchup_days = 1

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def http(self, routes):
        self.opener = FakeOpener(routes)
        return Http("test", opener=self.opener, sleep=lambda s: None, max_retries=2)

    def tree(self):
        return kb.Tree()

    def check(self):
        class A:
            verbose = False
        return kb.cmd_check(A())

    def research_files(self):
        out = []
        for d, _, fs in os.walk(self.root):
            if os.path.basename(d) == kb.RESEARCH_DIR:
                out += [os.path.join(d, f) for f in fs if f.endswith(".md")]
        return out


class TestDedupe(Base):
    def test_same_doi_from_two_sources(self):
        a = rec(title="GNNs for Molecules", doi="https://doi.org/10.1000/ABC", source_ids=["openalex:W1"],
                abstract=GNN_ABS, abstract_license="cc-by", peer_reviewed=True)
        b = rec(title="GNNs for molecules", doi="10.1000/abc", source_ids=["crossref:10.1000/abc"])
        merged = dedupe_batch([a, b])
        self.assertEqual(len(merged), 1)
        self.assertEqual(set(merged[0]["source_ids"]), {"openalex:W1", "crossref:10.1000/abc"})
        tree = self.tree()
        arch = Archive(tree, TODAY)
        cls = {"primary": "graph-neural-networks", "confidence": "high", "method": "test", "related": []}
        self.assertEqual(arch.upsert(a, cls)[0], "created")
        self.assertIn(arch.upsert(b, cls)[0], ("merged", "unchanged"))
        self.assertEqual(len(self.research_files()), 1)
        kb.cmd_reindex()
        self.assertEqual(self.check(), 0)

    def test_arxiv_and_published_version_merge(self):
        tree = self.tree()
        arch = Archive(tree, TODAY)
        cls = {"primary": "graph-neural-networks", "confidence": "high", "method": "test", "related": []}
        pre = rec(title="Message Passing GNNs", arxiv="2611.00001v2", peer_reviewed=False, abstract=GNN_ABS,
                  source_ids=["arxiv:2611.00001"], publication="arXiv")
        st, path = arch.upsert(pre, cls)
        rid = kb.parse_frontmatter(kb.read(os.path.join(self.root, path)))[0]["research_id"]
        self.assertEqual(rid, "arxiv:2611.00001")
        pub = rec(title="Message Passing GNNs", doi="10.1000/pub.1", arxiv="2611.00001", peer_reviewed=True,
                  publication="Journal of Graphs", source_ids=["openalex:W9"], abstract_license=None)
        st2, path2 = arch.upsert(pub, cls)
        self.assertEqual((st2, path2), ("merged", path))
        meta = kb.parse_frontmatter(kb.read(os.path.join(self.root, path)))[0]
        self.assertEqual(meta["research_id"], rid, "kalıcı kimlik değişmemeli")
        self.assertTrue(meta["peer_reviewed"])
        self.assertEqual(meta["doi"], "10.1000/pub.1")
        self.assertIn({"relation": "preprint", "arxiv": "2611.00001", "source": "merge"}, meta["related_versions"])
        kb.cmd_reindex()
        self.assertEqual(self.check(), 0)

    def test_no_doi_gets_stable_kb_id_and_dedupes_by_title(self):
        tree = self.tree()
        arch = Archive(tree, TODAY)
        cls = {"primary": "zero-knowledge-proofs", "confidence": "high", "method": "test", "related": []}
        r1 = rec(title="A Note on Zero-Knowledge Proofs", authors=["Shafi Goldwasser"], published_date="1989-01-01")
        st, path = arch.upsert(r1, cls)
        meta = kb.parse_frontmatter(kb.read(os.path.join(self.root, path)))[0]
        self.assertTrue(meta["research_id"].startswith("kb:1989-goldwasser-"))
        self.assertEqual(meta["research_id"], kb.kb_id(meta))
        self.assertEqual(arch.upsert(dict(r1), cls)[0], "unchanged")
        self.assertEqual(len(self.research_files()), 1)


class TestClassification(Base):
    def test_missing_abstract(self):
        clf = Classifier(self.tree())
        r = rec(title="Graph Neural Networks for Traffic Forecasting", categories=["arXiv:cs.LG"], abstract=None)
        c = clf.classify(r)
        self.assertEqual(c["primary"], "graph-neural-networks")
        arch = Archive(self.tree(), TODAY)
        st, path = arch.upsert(r, c)
        meta, body = kb.parse_frontmatter(kb.read(os.path.join(self.root, path)))
        self.assertEqual(meta["content_status"], "metadata_only")
        self.assertIn("özet bulunmuyor", body)

    def test_multiple_technologies(self):
        clf = Classifier(self.tree())
        r = rec(title="Mixture of Experts Graph Neural Networks",
                abstract="We combine mixture of experts routing with graph neural networks and transformer "
                         "architectures for deep learning on graphs.", categories=["arXiv:cs.LG"])
        c = clf.classify(r)
        self.assertIn(c["primary"], {"graph-neural-networks", "mixture-of-experts", "deep-learning"})
        self.assertTrue(c["related"] or c["primary"] == "deep-learning")

    def test_unclassifiable_not_archived(self):
        http = self.http([("export.arxiv.org", atom([{"id": "2611.09999", "title": "A Recipe for Sourdough Bread",
                                                      "abstract": "We bake bread with flour and water.",
                                                      "cat": "physics.pop-ph"}]))])
        run = Run(self.cfg, http, sources=("arxiv",), log=lambda *a: None)
        stats = run.daily(backfill=False, maintain=False)
        self.assertEqual(stats["created"], 0)
        self.assertEqual(stats["queued"], 0)
        self.assertEqual(stats["classified"]["low"], 1)


class TestDiscovery(Base):
    def _papers(self, phrase, acro, n, authors=True, months=True):
        out = []
        for i in range(n):
            out.append(rec(title=f"{phrase} for task {i}", source_ids=[f"arxiv:2611.0{i:04d}"], arxiv=f"2611.0{i:04d}",
                           authors=[f"Author{i if authors else 0} Smith"],
                           published_date=f"2026-{9 + (i % 2 if months else 0):02d}-1{i % 9}",
                           abstract=f"We introduce {phrase} ({acro}), building on graph neural networks. {GNN_ABS}"))
        return out

    def test_acronym_extraction(self):
        self.assertIn(("Hypergraph Neural Networks", "HGNNs"),
                      acronym_definitions("We study Hypergraph Neural Networks (HGNNs) here."))

    def test_single_paper_is_not_a_candidate(self):
        tree = self.tree()
        d = Discovery(self.cfg, tree, Classifier(tree))
        clf = Classifier(tree)
        for r in self._papers("Hypergraph Neural Networks", "HGNNs", 1):
            d.observe(r, clf.classify(r))
        self.assertEqual(d.update_candidates(), [])

    def test_synonym_of_existing_is_rejected(self):
        tree = self.tree()
        clf = Classifier(tree)
        d = Discovery(self.cfg, tree, clf)
        for r in self._papers("Mixture of Expert Networks", "MoE", 6):
            d.observe(r, clf.classify(r))
        d.update_candidates()
        c = d.cands["mixture of expert network"]
        self.assertEqual(c["status"], "rejected")
        self.assertEqual(c["reason"], "synonym_of:mixture-of-experts")

    def test_new_subtechnology_candidate_and_verify(self):
        tree = self.tree()
        clf = Classifier(tree)
        d = Discovery(self.cfg, tree, clf)
        papers = self._papers("Hypergraph Neural Networks", "HGNNs", 6)
        arch = Archive(tree, TODAY)
        arch.upsert(papers[0], {"primary": "graph-neural-networks", "confidence": "high", "method": "t", "related": []})
        for r in papers:
            d.observe(r, clf.classify(r))
        created = d.update_candidates(count_fn=lambda phrase: 250)
        self.assertIn("hypergraph neural network", created)
        c = d.cands["hypergraph neural network"]
        self.assertEqual(c["status"], "candidate")
        self.assertEqual(c["parent_suggestion"], "graph-neural-networks")
        self.assertEqual(c["literature_count"], 250)
        nid, path = d.verify("hypergraph neural network", "graph-neural-networks", title_tr="Hiperçizge Sinir Ağları")
        d.save()
        kb.cmd_reindex()
        t2 = self.tree()
        self.assertIn(nid, t2.nodes)
        self.assertEqual(t2.nodes[nid]["parent_id"], "graph-neural-networks")
        self.assertEqual(t2.nodes[nid]["meta"]["status"], "emerging")
        linked = [r for r in t2.research if nid in (r["meta"].get("related_technologies") or [])]
        self.assertEqual(len(linked), 1)
        self.assertEqual(self.check(), 0)
        # aynı aday ikinci kez onaylanamaz / aynı teknoloji yeniden oluşturulamaz
        with self.assertRaises(ValueError):
            d.verify("hypergraph neural network", "graph-neural-networks")


class FakeLLMClient:
    def __init__(self, outputs):
        self.outputs, self.calls = list(outputs), 0
        client = self

        class Messages:
            def create(self_inner, **kw):
                client.calls += 1
                out = client.outputs.pop(0)
                block = type("B", (), {"type": "text", "text": json.dumps(out)})()
                usage = type("U", (), {"input_tokens": 1000, "output_tokens": 200})()
                return type("R", (), {"stop_reason": "end_turn", "content": [block], "usage": usage})()

        self.beta = type("Beta", (), {"messages": Messages()})()
        self.messages = Messages()


SOURCES = [{"sid": "S1", "title": "A survey of graph neural networks", "authors": ["Jie Zhou", "Ganqu Cui"],
            "year": "2020", "doi": "10.1016/j.aiopen.2021.01.001", "publication": "AI Open", "peer_reviewed": True,
            "type": "review", "abstract": "GNNs are neural models that capture the dependence of graphs via message passing between "
                        "the nodes of graphs, and nodes update their representations from neighbors in 2 steps."},
           {"sid": "S2", "title": "Preprint on GNN limits", "authors": ["X Y"], "year": "2026", "doi": None,
            "url": "https://arxiv.org/abs/2611.00002", "publication": "arXiv", "peer_reviewed": False,
            "type": "preprint", "abstract": "We show that the expressive power of message passing graph neural networks is "
                          "bounded by the Weisfeiler-Lehman test."}]
DRAFT = {**{f"s{n}": [] for n in M.FILL_SECTIONS}, "conflicts": [],
         "s1": [{"text": "Çizge sinir ağları, çizge yapısındaki bağımlılıkları mesaj geçirme ile modelleyen sinir ağlarıdır.",
                 "evidence": "GNNs are neural models that capture the dependence of graphs via message passing",
                 "sources": ["S1"], "basis": "review"},
                {"text": "Kaynaksız bir iddia burada yer alıyor ve atılmalıdır.", "evidence": "x", "sources": ["S9"],
                 "basis": "review"},
                {"text": "Uydurma alıntıya dayanan bir ifade atılmalıdır.",
                 "evidence": "GNNs always outperform every other model on all benchmarks", "sources": ["S1"],
                 "basis": "review"},
                {"text": "Düğümler temsillerini 5 adımda günceller.",
                 "evidence": "nodes update their representations from neighbors in 2 steps", "sources": ["S1"],
                 "basis": "review"}],
         "s2": [{"text": "Düğümler komşularından gelen mesajları birleştirerek temsillerini günceller.",
                 "evidence": "GNNs are neural models that capture the dependence of graphs via message passing between the nodes",
                 "sources": ["S1"], "basis": "review"},
                {"text": "GNNs are neural models that capture the dependence of graphs.",
                 "evidence": "GNNs are neural models that capture the dependence of graphs via message passing", "sources": ["S1"],
                 "basis": "review"},
                {"text": "Mesaj geçirme, düğümlerin bir çizgedeki komşularından bilgi almasıdır.",
                 "evidence": "nodes update their representations from neighbors in 2 steps", "sources": ["S1"],
                 "basis": "review"}],
         "s10": [{"text": "Mesaj geçirme tabanlı modellerin ifade gücü sınırlıdır.",
                  "evidence": "the expressive power of message passing graph neural networks is bounded by the Weisfeiler-Lehman test",
                  "sources": ["S2"], "basis": "review"}]}


class TestMaintainer(Base):
    def _write_manual(self, nid, n, text):
        tree = self.tree()
        p = os.path.join(self.root, tree.nodes[nid]["dir"], kb.INDEX)
        meta, body = kb.parse_frontmatter(kb.read(p))
        meta["content_status"] = "manual"
        kb.write(p, kb.dump_frontmatter(meta) + "\n" + kb.replace_section(body, n, text))
        return p

    def test_manual_content_is_preserved_and_validation(self):
        p = self._write_manual("graph-neural-networks", 1, "Elle yazılmış tanım. [Kaynak: ders notu]")
        res = M.fill_node(self.cfg, self.tree(), "graph-neural-networks", draft=DRAFT, sources=SOURCES)
        meta, body = kb.parse_frontmatter(kb.read(p))
        self.assertEqual(kb.get_section(body, 1), "Elle yazılmış tanım. [Kaynak: ders notu]")
        self.assertIn("Düğümler komşularından", kb.get_section(body, 2))
        self.assertIn("[1]", kb.get_section(body, 2))
        self.assertIn("ön baskı bulgusu", kb.get_section(body, 10))
        self.assertNotIn("Kaynaksız", body)
        self.assertNotIn("Uydurma", body, "özette geçmeyen alıntı atılmalı")
        self.assertNotIn("5 adımda", body, "kanıtta olmayan sayı atılmalı")
        self.assertEqual(res["dropped"], 5)
        self.assertEqual(res["drop_reasons"].get("ifade Türkçe değil / biçim sızıntısı"), 1)
        self.assertEqual(res["drop_reasons"].get("kanıt bu teknolojiden söz etmiyor"), 1)
        self.assertIn("  > “GNNs are neural models", body, "kaynak alıntısı görünür olmalı")
        self.assertEqual(meta["content_status"], "ai_draft_sourced")
        self.assertFalse(meta["content_verified"])
        self.assertIn("10.1016/j.aiopen.2021.01.001", kb.get_section(body, 14))
        self.assertTrue(res["proposal"] and os.path.exists(res["proposal"]))
        kb.cmd_reindex()
        self.assertEqual(self.check(), 0)

    def test_migration_keeps_manual_text(self):
        p = os.path.join(self.root, self.tree().nodes["quantum-mechanics"]["dir"], kb.INDEX)
        meta, _ = kb.parse_frontmatter(kb.read(p))
        meta.pop("layout"), meta.pop("content_status"), meta.pop("content_sources")
        v1 = ("# Kuantum Mekaniği (Quantum Mechanics)\n\n## 1. Tanım\n\nElle tanım.\n\n## 2. Temel çalışma prensibi\n\n" + kb.PLACEHOLDER +
              "\n\n<!-- AUTO:BEGIN (x) -->\n## 3. Üst teknoloji\n<!-- AUTO:END -->\n\n## 8. Başlıca araştırma konuları\n\n"
              "Elle konu listesi.\n\n## 10. Kaynaklar\n\n- Kitap X\n")
        kb.write(p, kb.dump_frontmatter(meta) + "\n" + v1)
        self.assertTrue(kb.migrate_index(p))
        meta2, body = kb.parse_frontmatter(kb.read(p))
        self.assertEqual(meta2["layout"], 2)
        self.assertEqual(kb.get_section(body, 1), "Elle tanım.")
        self.assertEqual(kb.get_section(body, 14), "- Kitap X")
        self.assertIn("Elle konu listesi.", body)
        kb.cmd_reindex()
        self.assertEqual(self.check(), 0)

    def test_contradiction_goes_to_review(self):
        tree = self.tree()
        M.fill_node(self.cfg, tree, "graph-neural-networks", draft=DRAFT, sources=SOURCES)
        p = os.path.join(self.root, tree.nodes["graph-neural-networks"]["dir"], kb.INDEX)
        before = kb.read(p)
        client = FakeLLMClient([{"significant": True, "change_type": "contradiction", "section": 10,
                                 "proposed_text": "Bu ön baskı, ifade gücü sınırının aşılabildiğini bildiriyor.",
                                 "contradicts": ["Mesaj geçirme tabanlı modellerin ifade gücü sınırlıdır."],
                                 "rationale": "Mevcut sınırlılık ifadesiyle çelişiyor."}])
        st = {"llm_calls": 0, "llm_usd": 0.0}
        llm = LLM(self.cfg, st, client=client)
        rmeta = {"research_id": "arxiv:2611.12345", "title": "Beyond the WL limit", "authors": ["A B"], "year": 2026,
                 "peer_reviewed": False, "url": "https://arxiv.org/abs/2611.12345"}
        prop = M.assess_new_research(self.cfg, self.tree(), "graph-neural-networks", rmeta, "abstract text", llm)
        self.assertTrue(prop and "--contradiction" in prop)
        self.assertEqual(kb.read(p), before, "_index.md otomatik değişmemeli")
        pm, pb = kb.parse_frontmatter(kb.read(prop))
        self.assertEqual(pm["status"], "pending")
        self.assertIn("Çeliştiği mevcut ifadeler", pb)
        # insan onayı ile uygulanır; mevcut metin korunur
        M.apply_proposal(self.cfg, self.tree(), prop)
        body = kb.parse_frontmatter(kb.read(p))[1]
        self.assertIn("ifade gücü sınırlıdır", kb.get_section(body, 10))
        self.assertIn("aşılabildiğini", kb.get_section(body, 10))

    def test_llm_cache_and_budget(self):
        client = FakeLLMClient([{"a": 1}])
        st = {"llm_calls": 0, "llm_usd": 0.0}
        llm = LLM(self.cfg, st, client=client)
        schema = {"type": "object", "properties": {"a": {"type": "integer"}}, "required": ["a"], "additionalProperties": False}
        self.assertEqual(llm.json_call("t", "s", "u", schema), {"a": 1})
        self.assertEqual(llm.json_call("t", "s", "u", schema), {"a": 1})
        self.assertEqual(client.calls, 1, "aynı istem modele ikinci kez gönderilmemeli")
        self.cfg.llm_max_calls = 1
        with self.assertRaises(BudgetExceeded):
            llm.json_call("t", "s", "farklı", schema)


class TestRetraction(Base):
    def test_retraction_marks_record_and_creates_proposal(self):
        tree = self.tree()
        arch = Archive(tree, TODAY)
        doi = "10.1016/s0140-6736(97)11096-0"
        r = rec(title="Ileal-lymphoid-nodular hyperplasia", doi=doi, peer_reviewed=True, source_ids=["openalex:W5"])
        arch.upsert(r, {"primary": "deep-learning", "confidence": "high", "method": "t", "related": []})
        # bilgi dosyası bu yayına dayanıyor olsun
        p = os.path.join(self.root, tree.nodes["deep-learning"]["dir"], kb.INDEX)
        meta, body = kb.parse_frontmatter(kb.read(p))
        meta["content_sources"] = [doi]
        kb.write(p, kb.dump_frontmatter(meta) + "\n" + body)
        fixture = json.load(open(os.path.join(HERE, "fixtures", "crossref-updates-retraction.json")))
        http = self.http([("api.crossref.org/works?", json_resp(fixture))])
        run = Run(self.cfg, http, sources=(), log=lambda *a: None)
        run.check_retractions()
        files = self.research_files()
        meta, body = kb.parse_frontmatter(kb.read(files[0]))
        self.assertEqual(meta["retraction_status"], "retracted")
        self.assertIn("geri çekilmiştir", body)
        self.assertEqual({n["type"] for n in meta["notices"]}, {"retraction", "correction"})
        self.assertEqual(run.stats["retractions_found"], 1)
        props = M.list_proposals(self.cfg)
        self.assertEqual([m["kind"] for _, m in props], ["retraction"])
        kb.cmd_reindex()
        idx = kb.read(p)
        self.assertIn("GERİ ÇEKİLDİ", idx)


class TestRobustness(Base):
    PAGE1 = [{"id": "2611.10001", "title": "Graph Neural Networks for Chemistry", "abstract": GNN_ABS},
             {"id": "2611.10002", "title": "Zero-Knowledge Proofs for Private Graph Neural Networks Inference",
              "abstract": "Zero-knowledge proofs and zk-SNARKs verify inference of graph neural networks.", "cat": "cs.CR"}]
    PAGE2 = [{"id": "2611.10003", "title": "Mixture of Experts Transformer Architectures",
              "abstract": "A mixture of experts layer for transformer architectures in deep learning."}]

    def arxiv_routes(self, fail_page2=False):
        def handler(url):
            if "start=0" in url:
                return atom(self.PAGE1, total=3)
            if fail_page2:  # bu çalışma boyunca ikinci sayfa erişilemez (ör. kesinti)
                return Response(503, {}, b"")
            return atom(self.PAGE2, total=3)
        return [("export.arxiv.org", handler)]

    def test_api_unavailable(self):
        http = self.http([("export.arxiv.org", urllib.error.URLError("down"))])
        with self.assertRaises(SourceUnavailable):
            http.get("https://export.arxiv.org/api/query?x=1")
        self.assertEqual(len(self.opener.calls), 3, "kontrollü yeniden deneme (1 + 2)")
        run = Run(self.cfg, http, sources=("arxiv",), log=lambda *a: None)
        stats = run.daily(backfill=False, maintain=False)
        self.assertTrue(any("arxiv" in e for e in stats["errors"]))
        self.assertIsNone(run.state.checkpoint("arxiv").get("last_complete_day"), "kontrol noktası ilerlememeli")
        self.assertEqual(self.check(), 0)

    def test_interrupted_run_resumes_without_duplicates(self):
        http = self.http(self.arxiv_routes(fail_page2=True))
        run1 = Run(self.cfg, http, sources=("arxiv",), log=lambda *a: None)
        s1 = run1.daily(backfill=False, maintain=False)
        self.assertTrue(s1["errors"])
        cp = run1.state.checkpoint("arxiv")
        self.assertEqual(cp["start"], 2, "ilk sayfa işlendi, ikinci sayfadan devam edilmeli")
        n1 = len(self.research_files())
        run2 = Run(self.cfg, self.http(self.arxiv_routes()), sources=("arxiv",), log=lambda *a: None)
        s2 = run2.daily(backfill=False, maintain=False)
        self.assertFalse([e for e in s2["errors"] if "arxiv" in e])
        self.assertTrue(all("start=2" in u for u in self.opener.calls if "search_query" in u))
        self.assertEqual(len(self.research_files()), n1 + s2["created"])
        self.assertEqual(self.check(), 0)

    def test_daily_twice_creates_nothing_new(self):
        run1 = Run(self.cfg, self.http(self.arxiv_routes()), sources=("arxiv",), log=lambda *a: None)
        s1 = run1.daily(backfill=False, maintain=False)
        self.assertGreater(s1["created"], 0)
        files = sorted(self.research_files())
        # aynı gün ikinci çalışma: kontrol noktası tamam, aynı veriler yeniden gelse de kayıt oluşmaz
        run2 = Run(self.cfg, self.http(self.arxiv_routes()), sources=("arxiv",), log=lambda *a: None)
        s2 = run2.daily(backfill=False, maintain=False)
        self.assertEqual(s2["created"], 0)
        self.assertEqual(sorted(self.research_files()), files)
        # kontrol noktası sıfırlansa bile mükerrer oluşmaz (görülen kayıt + arşiv anahtarları)
        os.remove(os.path.join(self.cfg.state_dir, "checkpoints.json"))
        os.remove(os.path.join(self.cfg.state_dir, "seen.json"))
        run3 = Run(self.cfg, self.http(self.arxiv_routes()), sources=("arxiv",), log=lambda *a: None)
        s3 = run3.daily(backfill=False, maintain=False)
        self.assertEqual(s3["created"], 0)
        self.assertEqual(sorted(self.research_files()), files)
        self.assertEqual(self.check(), 0)

    def test_failed_run_leaves_valid_state_and_exit_code(self):
        sys.path.insert(0, os.path.dirname(HERE))
        import autokb
        os.environ["KB_MAX_CATCHUP_DAYS"] = "1"
        orig = Http.__init__

        def failing_init(self_, ua, **kw):
            orig(self_, ua, opener=FakeOpener([("", urllib.error.URLError("no network"))]), sleep=lambda s: None,
                 max_retries=1)
        Http.__init__ = failing_init
        try:
            code = autokb.main(["--root", self.root, "daily", "--no-llm", "--no-backfill"])
        finally:
            Http.__init__ = orig
            kb.set_root(self.root)
        self.assertEqual(code, 2, "kısmi başarısızlık çıkış kodu 2 olmalı (iş akışı bunu raporlar)")
        for f in os.listdir(self.cfg.state_dir):
            if f.endswith(".json"):
                json.load(open(os.path.join(self.cfg.state_dir, f)))
        self.assertFalse(os.path.exists(os.path.join(self.cfg.state_dir, ".lock")), "kilit bırakılmalı")
        self.assertEqual(self.check(), 0)

    def test_daily_assesses_new_research_for_filled_nodes(self):
        tree = self.tree()
        M.fill_node(self.cfg, tree, "graph-neural-networks", draft=DRAFT, sources=SOURCES)
        p = os.path.join(self.root, tree.nodes["graph-neural-networks"]["dir"], kb.INDEX)
        before = kb.parse_frontmatter(kb.read(p))[1].split("<!-- AUTO:RESEARCH")[0]
        client = FakeLLMClient([{"significant": True, "change_type": "application", "section": 8,
                                 "proposed_text": "Kimyada molekül özelliği tahmini için kullanıldığı bildiriliyor.",
                                 "contradicts": [], "rationale": "Yeni uygulama alanı."}])
        self.cfg.maintain_nodes_per_run = 0
        self.cfg.review_per_run = 0  # kuyruk boş: tek LLM çağrısı güncelleme değerlendirmesi olmalı
        run = Run(self.cfg, self.http(self.arxiv_routes()), sources=("arxiv",), log=lambda *a: None)
        run.llm = LLM(self.cfg, run.counter, client=client)
        stats = run.daily(backfill=False, maintain=True)
        self.assertEqual(client.calls, 1)
        self.assertEqual(stats["proposals"], 1)
        self.assertEqual([m["kind"] for _, m in M.list_proposals(self.cfg)], ["update"])
        after = kb.parse_frontmatter(kb.read(p))[1].split("<!-- AUTO:RESEARCH")[0]
        self.assertEqual(before, after, "bilgi metni otomatik değişmemeli; yalnızca öneri")

    def test_ids_and_links_preserved(self):
        before = {n: v["dir"] for n, v in self.tree().nodes.items()}
        Run(self.cfg, self.http(self.arxiv_routes()), sources=("arxiv",), log=lambda *a: None).daily(
            backfill=False, maintain=False)
        after = {n: v["dir"] for n, v in self.tree().nodes.items()}
        self.assertEqual(before, after)
        self.assertEqual(self.check(), 0)


class TestWorkflowSafety(unittest.TestCase):
    def test_workflow_never_pushes_main(self):
        wf = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".github", "workflows", "daily-research.yml")
        text = open(wf, encoding="utf-8").read()
        self.assertIn("auto/research", text)
        self.assertNotRegex(text, r"git push[^\n]*\bmain\b")
        self.assertIn("kb.py check", text)
        self.assertIn("unittest", text)


class TestRealRepository(unittest.TestCase):
    """Gerçek depo üzerinde bütünlük: kimlikler benzersiz, bağlantılar sağlam."""

    def test_real_repo_check(self):
        kb.set_root(os.path.dirname(os.path.dirname(HERE)))

        class A:
            verbose = False
        self.assertEqual(kb.cmd_check(A()), 0)


if __name__ == "__main__":
    unittest.main()


class TestNoLoss(Base):
    """Bütçeye takılan kayıtlar kaybolmaz; kuyruklar sınırlıdır; geç dizinlenenler yakalanır."""

    PAGE = [{"id": f"2611.200{i:02d}", "title": f"Graph Neural Networks for Molecules {i}", "abstract": GNN_ABS,
             "author": f"Author{i} Smith"} for i in range(6)]

    def routes(self, entries):
        def handler(url):
            if "id_list=" in url:
                ids = url.split("id_list=")[1].split("&")[0].replace("%2C", ",").split(",")
                return atom([e for e in entries if e["id"] in ids])
            return atom(entries)
        return [("export.arxiv.org", handler)]

    def test_budget_overflow_goes_to_backlog_and_drains_later(self):
        self.cfg.max_archive, self.cfg.max_per_tech = 2, 10
        run1 = Run(self.cfg, self.http(self.routes(self.PAGE)), sources=("arxiv",), log=lambda *a: None)
        s1 = run1.daily(backfill=False, maintain=False)
        self.assertEqual(s1["created"], 2)
        self.assertEqual(s1["backlog_size"], 4, "bütçeye sığmayan 4 kayıt backlog'da beklemeli")
        # ertesi gün: yeni veri yok, backlog'dan arşivlenir (tam metadata arXiv id_list ile yeniden çekilir)
        from datetime import timedelta
        self.cfg.today = TODAY + timedelta(days=1)
        run2 = Run(self.cfg, self.http(self.routes(self.PAGE)), sources=("arxiv",), log=lambda *a: None)
        s2 = run2.daily(backfill=False, maintain=False)
        self.assertEqual(s2["created"], 2)
        self.assertTrue(any("id_list=" in u for u in self.opener.calls))
        self.assertEqual(s2["backlog_size"], 2)
        self.cfg.today = TODAY + timedelta(days=2)
        Run(self.cfg, self.http(self.routes(self.PAGE)), sources=("arxiv",), log=lambda *a: None).daily(
            backfill=False, maintain=False)
        self.assertEqual(len(self.research_files()), 6, "6 kaydın hepsi sonunda arşivlenmeli")
        self.assertEqual(self.check(), 0)

    def test_backlog_caps_move_to_ledger_and_restore(self):
        from kbresearch.backlog import Backlog, Ledger
        self.cfg.backlog_per_tech = 2
        led = Ledger(self.cfg.state_dir, TODAY)
        bl = Backlog(self.cfg, led)
        for i in range(5):
            r = rec(title=f"Paper {i}", arxiv=f"2611.3000{i}", source_ids=[f"arxiv:2611.3000{i}"])
            bl.add(r, {"primary": "graph-neural-networks", "score": 6 + i, "related": []}, "arxiv")
        self.assertEqual(bl.enforce_limits({}), 3)
        self.assertEqual(len(bl), 2)
        self.assertEqual(sorted(e["score"] for e in bl.entries.values()), [9, 10], "en yüksek öncelikliler kalır")
        led.flush()
        self.assertEqual(len(led.read_all()), 3, "taşanlar silinmez, deftere yazılır")
        self.cfg.backlog_per_tech = 30
        self.assertEqual(bl.restore(tech="graph-neural-networks"), 3)
        self.assertEqual(len(bl), 5)

    def test_review_queue_merges_duplicates_caps_and_expires(self):
        from datetime import timedelta
        from kbresearch.archive import ReviewQueue
        from kbresearch.backlog import Ledger
        led = Ledger(self.cfg.state_dir, TODAY)
        q = ReviewQueue(self.cfg.review_dir, 3, led, expire_days=30)
        c = {"primary": "deep-learning", "score": 4.0, "candidates": [["deep-learning", 4.0]], "confidence": "medium"}
        a = rec(title="Same work", arxiv="2611.40000", source_ids=["arxiv:2611.40000"])
        b = rec(title="Same work", arxiv="2611.40000", doi="10.1/x", source_ids=["openalex:W1"])
        self.assertTrue(q.add(a, c, "r", TODAY))
        self.assertFalse(q.add(b, {**c, "score": 5.0}, "r", TODAY), "aynı çalışma birleştirilmeli")
        self.assertEqual(len(q.items), 1)
        self.assertEqual(q.items[0]["seen"], 2)
        self.assertIn("doi:10.1/x", q.items[0]["keys"])
        for i in range(4):
            q.add(rec(title=f"Other {i}", arxiv=f"2611.4100{i}"), {**c, "score": 3.0 + i}, "r", TODAY)
        q.items.append({"keys": ["arxiv:old"], "title": "Old", "score": 9, "added": (TODAY - timedelta(days=40)).isoformat(),
                        "record": {}, "seen": 1})
        moved = q.enforce_limits(TODAY)
        self.assertEqual(len(q.items), 3)
        self.assertEqual(moved, 3)
        led.flush()
        reasons = sorted(e["ledger_reason"] for e in led.read_all())
        self.assertEqual(reasons, ["queue_expired", "queue_overflow", "queue_overflow"])

    def test_openalex_revisit_processes_only_newly_indexed(self):
        from kbresearch.records import new_record
        run = Run(self.cfg, self.http([]), sources=(), log=lambda *a: None)
        old = new_record(title="Graph Neural Networks for Old", source_ids=["openalex:W10"], oa_created="2026-10-20",
                         abstract=GNN_ABS, abstract_license="cc-by", peer_reviewed=True)
        new = new_record(title="Graph Neural Networks for New", source_ids=["openalex:W11"], oa_created="2026-11-01",
                         abstract=GNN_ABS, abstract_license="cc-by", peer_reviewed=True)
        run.process([old, new], "openalex", created_since="2026-10-28", use_seen=False)
        self.assertEqual(run.stats["skipped_known"], 1)
        self.assertEqual(run.stats["backlogged"], 1)

    def test_recovery_planned_from_run_log(self):
        os.makedirs(self.cfg.state_dir, exist_ok=True)
        with open(os.path.join(self.cfg.state_dir, "run-log.jsonl"), "w") as f:
            f.write(json.dumps({"date": "2026-11-05", "fetched": 3867, "budget_skipped": 561}) + "\n")
            f.write(json.dumps({"date": "2026-11-06", "fetched": 0, "budget_skipped": 0}) + "\n")
        run = Run(self.cfg, self.http([]), sources=(), log=lambda *a: None)
        run.plan_recovery()
        jobs = run.state.checkpoint("recovery")["jobs"]
        self.assertIn({"source": "arxiv", "day": "2026-11-03"}, jobs)
        self.assertIn({"source": "openalex", "stream": "journal", "day": "2026-11-02"}, jobs)
        self.assertEqual(len(jobs), 3)
        run.plan_recovery()  # ikinci kez planlanmaz
        self.assertEqual(len(run.state.checkpoint("recovery")["jobs"]), 3)


class TestCandidateConflicts(Base):
    def setUp(self):
        super().setUp()
        tree = self.tree()
        self.d = Discovery(self.cfg, tree, Classifier(tree))

    def cand(self, key, acronyms, parent=None):
        c = {"key": key, "display": key, "status": "candidate", "acronyms": acronyms, "parent_suggestion": parent,
             "notes": []}
        self.d.assess_conflicts(c)
        return c

    def test_acronym_only_match_is_not_synonym(self):
        # ZKP takma adı var; "zonal kernel pooling (ZKP)" anlamca ilgisiz: eş anlamlı sayılmamalı
        c = self.cand("zonal kernel pooling", ["ZKP"])
        self.assertEqual(c["status"], "candidate")
        self.assertEqual(c["ambiguous_acronyms"][0]["existing"], "zero-knowledge-proofs")

    def test_old_acronym_only_rejection_is_reverted(self):
        c = {"key": "zonal kernel pooling", "display": "x", "status": "rejected", "reason": "synonym_of:zero-knowledge-proofs",
             "acronyms": ["ZKP"], "notes": []}
        self.d.assess_conflicts(c)
        self.assertEqual(c["status"], "candidate")

    def test_near_duplicate_rejected_and_overlap_flagged(self):
        self.assertEqual(self.cand("graph neural network model", [])["status"], "candidate")
        dup = self.cand("neural graph network", [])
        self.assertEqual(dup["status"], "rejected")
        self.assertTrue(dup["reason"].startswith("duplicate_of:graph-neural-networks"))
        sub = self.cand("transformer graph neural network", [], parent="transformer-architectures")
        self.assertEqual(sub["variant_of"], "graph-neural-networks", "mevcut adı içeren aday alt türdür")
        self.assertFalse(sub["possible_duplicate"])
        near = self.cand("zero knowledge graph proof", [], parent="graph-neural-networks")
        self.assertTrue(near["possible_duplicate"], "ZKP ile güçlü örtüşme işaretlenmeli")
        with self.assertRaises(ValueError):
            self.d.cands[near["key"]] = near
            self.d.verify(near["key"], "graph-neural-networks")
