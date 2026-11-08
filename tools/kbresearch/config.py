import os
from datetime import date


def env_int(name, default):
    try:
        return int(os.environ.get(name, default))
    except ValueError:
        return default


def env_float(name, default):
    try:
        return float(os.environ.get(name, default))
    except ValueError:
        return default


class Config:
    """Çalışma ayarları. Ortam değişkenleriyle değiştirilebilir; testler alanları doğrudan atar."""

    def __init__(self, root, today=None):
        self.root = root
        self.state_dir = os.path.join(root, "state")
        self.review_dir = os.path.join(root, "review")
        self.today = today or date.today()
        # kimlik ve anahtarlar (değerler asla dosyaya yazılmaz)
        self.contact_email = os.environ.get("KB_CONTACT_EMAIL") or None
        self.openalex_key = os.environ.get("OPENALEX_API_KEY") or None
        # günlük bütçeler
        self.max_archive = env_int("KB_MAX_ARCHIVE_PER_RUN", 40)
        self.max_per_tech = env_int("KB_MAX_PER_TECH_PER_RUN", 3)
        self.arxiv_page_size = env_int("KB_ARXIV_PAGE_SIZE", 500)
        self.arxiv_max_results = env_int("KB_ARXIV_MAX_RESULTS", 3000)
        self.arxiv_lag_days = 2          # arXiv duyuruları gönderim tarihinden sonra gelir
        self.openalex_lag_days = 3       # OpenAlex dizinlemesi gecikmeli; from_created_date ücretli plan ister
        self.openalex_per_page = 100
        # Anahtarla günlük dergi akışının tamamı (~90 sayfa ≈ $0,009); anahtarsız paylaşımlı bütçede 20 sayfa
        self.openalex_max_pages = env_int("KB_OPENALEX_MAX_PAGES", 100 if self.openalex_key else 20)
        # Geç dizinlenen yayınlar: aynı yayın günü bu gecikmelerle yeniden taranır; yalnızca ilk taramadan
        # sonra OpenAlex'e eklenen (created_date) kayıtlar işlenir
        self.openalex_revisit_lags = [int(x) for x in os.environ.get("KB_OPENALEX_REVISIT_LAGS", "10,30").split(",") if x]
        self.arxiv_revisit_lags = [int(x) for x in os.environ.get("KB_ARXIV_REVISIT_LAGS", "7").split(",") if x]
        self.seen_days = env_int("KB_SEEN_DAYS", 21)
        self.max_catchup_days = env_int("KB_MAX_CATCHUP_DAYS", 3)
        self.review_queue_max = env_int("KB_REVIEW_QUEUE_MAX", 150)
        self.review_expire_days = env_int("KB_REVIEW_EXPIRE_DAYS", 30)
        self.backlog_max = env_int("KB_BACKLOG_MAX", 3000)
        self.backlog_per_tech = env_int("KB_BACKLOG_PER_TECH", 30)
        self.review_per_run = env_int("KB_REVIEW_PER_RUN", 30)
        self.verify_per_run = env_int("KB_VERIFY_PER_RUN", 60)
        self.retraction_checks_per_run = env_int("KB_RETRACTION_CHECKS", 40)
        # tarihsel tamamlama (günlük toplamadan ayrı bütçe)
        self.backfill_techs_per_run = env_int("KB_BACKFILL_TECHS", 3)
        self.backfill_per_tech = env_int("KB_BACKFILL_PER_TECH", 5)
        # teknoloji keşfi
        self.discovery_min_papers = env_int("KB_DISCOVERY_MIN_PAPERS", 5)
        self.discovery_min_authors = env_int("KB_DISCOVERY_MIN_AUTHORS", 3)
        self.discovery_min_literature = env_int("KB_DISCOVERY_MIN_LITERATURE", 20)
        self.discovery_lit_checks = env_int("KB_DISCOVERY_LIT_CHECKS", 5)
        self.discovery_auto_verify = os.environ.get("KB_DISCOVERY_AUTO_VERIFY") == "1"
        # LLM (isteğe bağlı)
        self.llm_model = os.environ.get("KB_LLM_MODEL", "claude-opus-5-5")
        self.llm_max_calls = env_int("KB_LLM_MAX_CALLS", 40)
        self.llm_max_usd = env_float("KB_LLM_MAX_USD", 1.0)
        self.maintain_nodes_per_run = env_int("KB_MAINTAIN_NODES", 3)

    @property
    def user_agent(self):
        ua = "Technology-Knowledge-Base/1.0 (+https://github.com/ofsng/teknoloji)"
        return ua + (f" mailto:{self.contact_email}" if self.contact_email else "")
