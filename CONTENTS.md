# Package Manifest & ZIP Contents

**Project:** Puppet-Provisioned Supplier Quality Review Portal  
**Student:** AADITYA ASWALE (23102B0044)  
**Package Name:** `Supplier_Quality_Portal_Project_Handover.zip`  
**Purpose:** Comprehensive project handover archive for ChatGPT code inspection, architecture walkthrough, and viva voce defense.

---

## 1. What is Included in this Package

| Folder / File Path | Description & Purpose |
| :--- | :--- |
| `backend/` | Complete Django application source code, models, views, serializers, templates, static CSS design system, and Pytest test suite. |
| `backend/apps/` | Modular applications: `accounts`, `core`, `dashboard`, `reports`, `reviews`, `suppliers`. |
| `backend/templates/` | Semantic HTML5 templates styled with modern enterprise dark theme and Phosphor icons. |
| `backend/static/` | Custom CSS design system (`main.css`), icons, and UI assets. |
| `backend/tests/` | Automated unit and integration test suite (5/5 passed). |
| `backend/db.sqlite3` | Local database pre-seeded with 10 registered suppliers, 13 quality reviews, and 3 demo user accounts. |
| `selenium-tests/` | Complete Apache Maven + Java 17 Selenium WebDriver automated browser regression suite (Page Object Model). |
| `infrastructure/docker/` | Production multi-stage `Dockerfile`, `docker-compose.yml`, and `entrypoint.sh`. |
| `infrastructure/nginx/` | Nginx reverse proxy configuration (`default.conf`) with static caching and health routing. |
| `infrastructure/puppet/` | Declarative Puppet module (`supplier_portal`) managing base packages, deployer user, dirs, and daemons. |
| `infrastructure/ansible/` | Ansible playbooks: `site.yml` (idempotent provisioning) and `rollback.yml` (automated Git rollback). |
| `jenkins/` | Declarative `Jenkinsfile`, defect demonstration pipeline, and exported Jenkins XML job configuration. |
| `docs/` | 24-part academic documentation suite (SRS, architecture, database ERD, operations guide, viva guide, presentation deck). |
| `docs/evidence/` | Live Surefire HTML test execution reports and defect failure screenshots. |
| `scripts/` | Seed data populator (`seed_data.py`), automated route authorization probe (`test_portal_access.py`), and Jenkins setup. |
| `PROJECT_EXPLANATION_GUIDE.md` | Authoritative 14-section comprehensive project guide written for ChatGPT and examiner viva explanation. |
| `IMPLEMENTATION_INVENTORY.md` | Full implementation matrix tracking all 18 curriculum requirements and verification evidence. |
| `PROJECT_MASTER_CONTEXT.md` | Permanent master recovery context document with real execution logs. |
| `GIT_LOG_HISTORY.txt` | Complete Git commit history export with commit hashes, messages, branches, and diff statistics. |
| `.env.example` | Sanitized environment configuration template. |
| `run_all.bat` / `run_all.py` | One-click application launcher. |
| `README.md` | Project overview, quick start, and architecture summary. |

---

## 2. Items Intentionally Excluded for Security & Hygiene

To comply with enterprise security standards and keep the archive clean and compact:
- **Virtual Environments (`backend/venv/`, `.venv/`):** Excluded to eliminate redundant platform-specific binaries (~300 MB). All dependencies are preserved in `backend/requirements.txt`.
- **Python Cache (`__pycache__/`, `*.pyc`, `.pytest_cache/`):** Excluded compiled bytecode.
- **Maven Build Artifacts (`selenium-tests/target/` class files and JARs):** Excluded heavy compiler output while preserving source code, `pom.xml`, test reports, and failure screenshots in `docs/evidence/`.
- **Git Internal Database (`.git/`):** Excluded internal Git database objects to prevent credential leakage. Full Git history is safely exported in `GIT_LOG_HISTORY.txt`.
- **Real Secrets & Passwords:** No production credentials, private SSH keys, or API tokens are present. All accounts use standard intentional academic demo credentials (`Admin@12345`, `Manager@12345`, `Reviewer@12345`).
- **Heavy Docker Container Images:** Docker image layer tars are excluded; reproducible build definitions are preserved in `infrastructure/docker/Dockerfile` and `docker-compose.yml`.
- **Compiled Distribution Tarballs (`dist/`):** Excluded packaged tarball artifacts (`supplier-portal-*.tar.gz`) to keep the archive clean, fast, and optimized for AI code review models.
