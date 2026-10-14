# PROJECT EXPLANATION GUIDE: Puppet-Provisioned Supplier Quality Review Portal

**Academic Project Title:** Puppet-Provisioned Supplier Quality Review Portal  
**Student Name:** AADITYA ASWALE  
**Student ID:** 23102B0044  
**Curriculum:** 15-Week DevOps & Software Engineering Practicum  
**Repository Baseline:** Release `v1.0.0` | Active Branch: `develop`  
**Application URLs:** `http://localhost/` (Nginx Reverse Proxy) | `http://localhost:8000/` (Direct Gunicorn) | `http://localhost:8080/` (Jenkins LTS)

---

## 1. What the Project Does & Problem Statement
In industrial manufacturing and aerospace supply chains, enterprises manage dozens or hundreds of external vendor contracts. Traditionally, supplier evaluations, incoming batch defect counts, ISO compliance audits, and delivery timelines were tracked through disconnected spreadsheets and manual email threads. This led to:
- Lack of an immutable audit trail and historical accountability.
- Subjective, error-prone vendor evaluations without standard mathematical rubrics.
- Delayed defect detection allowing defective components to reach assembly lines.
- Manual deployment and configuration drift across staging and production servers.

### The Solution:
The **Supplier Quality Review Portal** is a production-ready, containerized web application with an automated DevOps delivery pipeline. It provides:
1. **Role-Based Access Control (RBAC):** Distinct operational scopes for Administrator, Quality Manager, and Quality Reviewer.
2. **Supplier Directory Management:** Complete vendor lifecycle tracking (Mechanical, Electronics, Raw Materials, Packaging, Chemicals).
3. **Audit Review Engine & Scoring Matrix:** Dynamic weighted scoring across Product Quality, On-time Delivery, and Regulatory Compliance with automated defect deductions and letter grading (A+, A, B, C, D).
4. **State-Machine Workflow:** Multi-stage review lifecycle (`Draft` $\rightarrow$ `Pending Review` $\rightarrow$ `Approved` / `Rejected`) with append-only audit logs.
5. **Interactive Executive Analytics:** Real-time Chart.js visual distributions, category benchmarks, and CSV export capabilities.
6. **Complete 15-Week DevOps Lifecycle:** Continuous Integration in Jenkins LTS, automated headless browser quality gates via Apache Maven and Selenium WebDriver, multi-stage Docker containerization, and Infrastructure as Code with Puppet and Ansible.

---

## 2. Complete Folder Structure & File Purpose

```text
supplier-quality-portal/
├── backend/                               # Django Application Source Root
│   ├── apps/
│   │   ├── accounts/                      # Authentication & RBAC Module
│   │   │   ├── models.py                  # UserProfile model (role: ADMIN, QUALITY_MANAGER, REVIEWER)
│   │   │   ├── permissions.py             # DRF permission classes (IsAdminUserRole, IsQualityManagerOrAdmin)
│   │   │   ├── views.py                   # Login, logout, profile, and user management views
│   │   │   └── urls.py                    # /accounts/ routes
│   │   ├── core/                          # Cross-Cutting Shared Utilities
│   │   │   ├── context_processors.py      # Injects CURRENT_USER_ROLE, IS_ADMIN, IS_QUALITY_MANAGER
│   │   │   └── views.py                   # RFC-compliant /health/ probe & custom error handlers (404/500)
│   │   ├── dashboard/                     # Executive Quality Dashboard
│   │   │   ├── views.py                   # KPI calculations, leaderboard, and pending review queue
│   │   │   ├── api_views.py               # REST API /api/dashboard/summary/
│   │   │   └── urls.py                    # Root / routes
│   │   ├── reports/                       # Analytics & Reporting Module
│   │   │   ├── views.py                   # Chart.js analytics aggregation & CSV export engine
│   │   │   └── urls.py                    # /reports/ routes
│   │   ├── reviews/                       # Quality Audit & Scoring Engine
│   │   │   ├── models.py                  # QualityReview (scoring formulas) & ReviewAuditLog
│   │   │   ├── views.py                   # Review CRUD, submission, approve/reject workflow
│   │   │   ├── api_views.py               # REST API /api/reviews/ (ViewSet)
│   │   │   └── serializers.py             # QualityReviewSerializer with dynamic grade field
│   │   └── suppliers/                     # Supplier Directory Module
│   │       ├── models.py                  # Supplier model (quality score recalculation & grade)
│   │       ├── views.py                   # Supplier CRUD & search views
│   │       ├── api_views.py               # REST API /api/suppliers/ (SupplierViewSet with filtering)
│   │       ├── api_urls.py                # DRF DefaultRouter with basename='api-supplier'
│   │       └── serializers.py             # SupplierSerializer
│   ├── config/                            # Project Settings & Routing
│   │   ├── settings.py                    # PostgreSQL in Docker, SQLite fallback, REST framework config
│   │   ├── urls.py                        # Master URL routing table
│   │   └── wsgi.py / asgi.py              # WSGI/ASGI entrypoints for Gunicorn
│   ├── static/css/main.css                # Custom Enterprise Dark-Mode Design System
│   ├── templates/                         # Django HTML Templates (Semantic HTML5 + Phosphor Icons)
│   │   ├── base.html                      # App shell, responsive sidebar, user profile card
│   │   ├── accounts/                      # login.html (quick demo buttons), user_management.html
│   │   ├── dashboard/index.html           # KPI cards, Chart.js canvases, top supplier leaderboard
│   │   ├── reviews/                       # review_list.html, review_detail.html, review_form.html
│   │   └── suppliers/                     # supplier_list.html (live API search), supplier_detail.html
│   ├── tests/                             # Automated Backend Tests (Pytest)
│   │   ├── test_api.py                    # Health check & dashboard summary API tests
│   │   ├── test_models.py                 # Grade calculations & weighted scoring tests
│   │   └── test_workflow.py               # Review status state-machine transitions
│   ├── manage.py                          # Django management CLI
│   ├── requirements.txt                   # Frozen Python dependencies (Django 5.1, DRF, Pytest, Gunicorn)
│   ├── pytest.ini                         # Pytest configuration
│   └── .flake8                            # PEP8 linting rules (max-line-length = 120)
├── selenium-tests/                        # Automated Browser E2E Test Suite (Java / Maven)
│   ├── pom.xml                            # Maven dependencies (Selenium 4.18, TestNG 7.9)
│   └── src/test/java/com/quality/portal/
│       ├── pages/                         # Page Object Model (POM) Abstractions
│       │   ├── BasePage.java              # Explicit wait utilities and safe click/type helpers
│       │   ├── LoginPage.java             # Authentication page interactions
│       │   ├── DashboardPage.java         # KPI assertions & sidebar navigation
│       │   ├── SupplierPage.java          # Supplier search, profile view, onboarding form
│       │   └── ReviewPage.java            # Dynamic score calculation & audit approval modal
│       ├── tests/                         # TestNG Test Classes
│       │   ├── BaseTest.java              # Headless Chrome driver initialization & screenshot on failure
│       │   ├── LoginDashboardE2ETest.java # Journey 1: Authentication & KPI rendering
│       │   ├── SupplierManagementE2ETest.java # Journey 2: Search, view profile & supplier creation
│       │   ├── ReviewWorkflowE2ETest.java # Journey 3: Audit creation, dynamic score & manager approval
│       │   └── NegativeDefectValidationTest.java # Journey 4: Quality gate defect injection demonstration
│       └── utils/                         # TestListener for failure screenshot capturing
├── infrastructure/                        # Infrastructure as Code & Orchestration
│   ├── docker/
│   │   ├── Dockerfile                     # Multi-stage production build (121 MB runtime, non-root appuser)
│   │   ├── docker-compose.yml             # Orchestration: web (Django), db (PostgreSQL 16), nginx
│   │   └── entrypoint.sh                  # Database wait script, migration runner, gunicorn starter
│   ├── nginx/
│   │   └── default.conf                   # Reverse proxy configuration, static cache, health pass-through
│   ├── puppet/                            # Declarative Infrastructure as Code (Puppet)
│   │   ├── manifests/site.pp              # Node manifest applying supplier_portal module
│   │   └── modules/supplier_portal/       # Module managing packages, deployer user, dirs, nginx proxy
│   └── ansible/                           # Procedural Configuration Management & Rollback
│       ├── inventory.ini                  # Target node inventory
│       ├── site.yml                       # Idempotent server provisioning playbook
│       └── rollback.yml                   # Automated zero-downtime rollback to stable Git tag v1.0.0
├── jenkins/                               # Continuous Integration Pipeline as Code
│   ├── Jenkinsfile                        # Declarative pipeline (Checkout -> Flake8 -> Pytest -> Selenium -> Build -> Deploy -> Health)
│   ├── Jenkinsfile.defect-demo            # Pipeline demonstrating quality gate rejection on defect
│   └── supplier-quality-portal-ci-job.xml # Exported Jenkins XML job configuration
├── docs/                                  # 24-Part Comprehensive Academic & Engineering Documentation
│   ├── 01-problem-definition.md           # Scope & requirements analysis
│   ├── 02-software-requirements-specification.md # SRS document
│   ├── 03-system-architecture.md          # Monolith architecture & dataflow diagrams
│   ├── 04-database-design.md              # Entity-Relationship diagram & schema definitions
│   ├── 05-rest-api-documentation.md       # API endpoints, request/response contracts
│   ├── 09-automated-testing-selenium-suite.md # Selenium POM architecture & test matrix
│   ├── 10-continuous-testing-quality-gates.md # Quality gate failure analysis & screenshot archive
│   ├── 11-containerization-docker-architecture.md # Multi-stage build design & security
│   ├── 12-ci-cd-pipeline-jenkins-declarative.md # Complete Jenkins pipeline stage breakdown
│   ├── 14-infrastructure-as-code-puppet.md # Puppet module design & catalog compilation
│   ├── 15-configuration-management-ansible.md # Ansible idempotency & task orchestration
│   ├── 15_WEEK_REQUIREMENTS_TRACEABILITY.md # Authoritative 15-week traceability matrix
│   ├── 20-disaster-recovery-and-rollback.md # RTO/RPO targets & automated rollback runbook
│   ├── 21-user-manual-and-operations-guide.md # Role-by-role user manual & walkthroughs
│   ├── 22-viva-voce-defense-guide.md      # Top 15 examiner Q&A & live demo script
│   ├── 23-final-project-presentation.md   # 12-slide presentation deck
│   ├── 24-troubleshooting-limitations-and-future-work.md # Troubleshooting runbook & future roadmap
│   └── evidence/                          # Live test reports & defect failure screenshots
├── scripts/                               # Automation & Helper Scripts
│   ├── seed_data.py                       # Populates realistic demo suppliers, reviews, and users
│   ├── test_portal_access.py              # Automated HTTP probe verifying all roles & routes
│   └── setup_jenkins_job.py               # Automates Jenkins job creation inside controller
├── PROJECT_MASTER_CONTEXT.md              # Authoritative permanent master recovery context
├── IMPLEMENTATION_INVENTORY.md            # Comprehensive feature-by-feature verification matrix
├── CONTENTS.md                            # Package contents description & exclusion manifest
├── GIT_LOG_HISTORY.txt                    # Complete Git commit history export
└── .env.example                           # Sanitized environment configuration template
```

---

## 3. Application Architecture & Communication Flow

The portal follows an **Enterprise Modular Monolith** pattern:

```text
[ Browser / Client ]
        │
        ▼ (Port 80)
┌────────────────────────────────────────────────────────┐
│  Nginx Reverse Proxy (supplier_portal_nginx)           │
│  - Serves static assets directly (/static/, /media/)   │
│  - Forwards /health/ and dynamic traffic to Gunicorn   │
└───────────────────────────────────┬────────────────────┘
                                    │ (Internal Network)
                                    ▼
┌────────────────────────────────────────────────────────┐
│  Django Application Server (supplier_portal_web:8000)  │
│  - Python 3.10 / Django 5.1 / Django REST Framework    │
│  - WSGI Gunicorn Workers (sync workers)                │
│  - Template Engine (Django Templates + Phosphor Icons) │
│  - REST API Routers (/api/suppliers/, /api/reviews/)   │
└───────────────────────────────────┬────────────────────┘
                                    │ (Port 5432)
                                    ▼
┌────────────────────────────────────────────────────────┐
│  PostgreSQL Database (supplier_portal_db:5432)         │
│  - Relational Schema with Foreign Keys & Constraints   │
│  - Persistent Docker Volume (postgres_data)            │
│  - SQLite Fallback for Local Standalone Execution      │
└────────────────────────────────────────────────────────┘
```

### Communication Flow:
1. **Frontend to Django:** Web browsers connect to Nginx on port `80`. Nginx routes static requests directly from `/app/staticfiles/` with HTTP caching headers, and proxies dynamic requests to Gunicorn on port `8000`.
2. **AJAX API Fetching:** When viewing `/suppliers/`, client-side JavaScript issues an asynchronous `fetch('/api/suppliers/?search=...')` request. The session cookie is automatically passed, allowing Django REST Framework's `SessionAuthentication` to validate permissions.
3. **Django to Database:** Django models interact with PostgreSQL 16 using psycopg2/psycopg. In standalone local mode, `backend/config/settings.py` automatically falls back to `backend/db.sqlite3` when `USE_SQLITE=True`.

---

## 4. Page-by-Page Feature Explanation

### 4.1 Sign-In Screen (`/accounts/login/`)
- Split-pane responsive layout with an enterprise shield brand logo.
- Interactive **One-Click Demo Credentials** buttons (`Admin`, `Manager`, `Reviewer`) that auto-fill the login form for rapid examiner demonstration.
- Form authentication handled by Django's `AuthenticationForm` with CSRF protection.

### 4.2 Executive Quality Dashboard (`/` or `/dashboard/`)
- **KPI Ribbon Cards:** Total Registered Suppliers, Average Quality Score, Pending Quality Approvals, Approved Audits, and Rejected Audits.
- **Chart.js Visualizations:**
  - *Review Status Distribution:* Doughnut chart showing proportions of Draft, Pending, Approved, and Rejected reviews.
  - *Category Quality Score:* Horizontal bar chart comparing average supplier performance across categories.
- **Pending Approvals Queue:** Prominently highlights reviews awaiting managerial sign-off with an "Evaluate" shortcut button.
- **Top Supplier Quality Leaderboard:** Top 5 certified suppliers ranked by weighted quality score with grade pills.

### 4.3 Supplier Management Directory (`/suppliers/`)
- **Live Search & Filter Bar:** Debounced search input (`id="input-search-supplier"`) searching by name, supplier ID, code, or contact person.
- **Dynamic Category & Status Filtering:** Instant filtering without page refreshes, synced directly with `/api/suppliers/`.
- **Supplier Records Table:** Clean tabular view displaying Supplier ID, Name, Code, Contact Person, Email, Category, Status, Quality Score, Grade, and Actions.
- **State Handling:**
  - *Loading State:* Glowing sync indicator with spinner.
  - *Empty State:* "No suppliers found" prompt with a "Clear Search & Filters" action.
  - *Error State:* Graceful alert banner with a "Retry Connection" action.
- **Actions:** "View Details" (navigates to `/suppliers/<id>/`) and "Edit" (restricted to Quality Manager and Admin).

### 4.4 Supplier 360° Profile View (`/suppliers/<int:pk>/`)
- Complete vendor profile card displaying contact information, address, registration date, and overall performance grade.
- Historical Quality Trend Chart rendered via Chart.js plotting quality scores across consecutive audits.
- Full audit review history list with scores, reviewer names, dates, and certified statuses.

### 4.5 Supplier Onboarding Form (`/suppliers/create/`)
- Accessible only to Quality Managers and Administrators.
- Validates unique constraints on `supplier_id` and `code`.
- Auto-formats supplier code to uppercase.

### 4.6 Quality Reviews Directory (`/reviews/`)
- Multi-tab navigation filtering by status: **All Reviews**, **Pending Approval**, **Certified Approved**, and **Rejected**.
- Action button to create a **New Quality Review** (`/reviews/create/`).

### 4.7 Audit Review Entry Form (`/reviews/create/`)
- Accessible to Reviewers, Managers, and Admins.
- Select supplier from dropdown; review date defaults to today.
- Input defect count and numerical scores (0–100) for:
  - Product Quality Score (45% weight)
  - Compliance Score (30% weight)
  - Delivery Score (25% weight)
- **Live Interactive Score Calculator:** Client-side JavaScript dynamically updates the calculated percentage and projected letter grade in real time as scores and defect counts are typed.
- Actions: **Submit for Approval** (transitions to `Pending Review`) or **Save Draft** (saves as `Draft`).

### 4.8 Review Evaluation & Approval View (`/reviews/<int:pk>/`)
- Detailed score breakdown card with defect penalty calculations.
- Immutable **Audit Trail Timeline** displaying transitions, timestamps, and actors.
- **Manager Approval Modal:** Quality Managers provide certification remarks and click **Certify & Approve** (updates status to `Approved` and recalculates supplier's score) or **Reject Audit** (marks review `Rejected`).

### 4.9 Analytics & Reporting (`/reports/`)
- Executive analytics dashboard displaying score distributions, grade allocations (A+, A, B, C, D), and monthly review throughput.
- **Export CSV Button:** Generates and downloads a formatted CSV audit report (`supplier_quality_report.csv`).

### 4.10 User Management (`/accounts/users/`)
- Administrator-only view displaying registered users, their roles, active status, and permissions.

### 4.11 System Health Probe (`/health/`)
- Public, unauthenticated JSON endpoint returning HTTP 200:
  ```json
  {
    "status": "healthy",
    "application": "Supplier Quality Review Portal",
    "student": "AADITYA ASWALE (23102B0044)",
    "database": "ok",
    "environment": "production-docker",
    "version": "1.0.0"
  }
  ```

---

## 5. Role-Based Access Control (RBAC) Matrix

Implemented via `apps.accounts.models.UserProfile`, `apps.core.context_processors.global_context`, and DRF permissions in `apps.accounts.permissions`:

| Feature / Action | Reviewer | Quality Manager | Administrator | Code Enforcement Location |
| :--- | :---: | :---: | :---: | :--- |
| View Dashboard & KPIs | ✅ | ✅ | ✅ | `apps.dashboard.views.dashboard_view` |
| View Supplier Directory | ✅ | ✅ | ✅ | `apps.suppliers.views.supplier_list_view` |
| Onboard / Edit Supplier | ❌ | ✅ | ✅ | `apps.suppliers.views.supplier_create_view` (`IS_QUALITY_MANAGER`) |
| Delete Supplier | ❌ | ❌ | ✅ | `apps.suppliers.views.supplier_delete_view` (`user_role == 'ADMIN'`) |
| Create Quality Review | ✅ | ✅ | ✅ | `apps.reviews.views.review_create_view` |
| Approve / Reject Review | ❌ | ✅ | ✅ | `apps.reviews.views.review_action_view` (`IS_QUALITY_MANAGER`) |
| Export Analytics & CSV | ✅ | ✅ | ✅ | `apps.reports.views.reports_index_view` |
| User Management | ❌ | ❌ | ✅ | `apps.accounts.views.user_management_view` (`IS_ADMIN`) |
| REST API Write Operations | ❌ | ✅ | ✅ | `IsQualityManagerOrAdmin` in `apps.accounts.permissions` |

---

## 6. Audit Workflow Lifecycle

```text
[ Reviewer creates audit ]
           │
           ▼
     ┌───────────┐
     │   Draft   │ ──(Submit for Approval)──► ┌──────────────────┐
     └───────────┘                            │  Pending Review  │
                                              └─────────┬────────┘
                                                        │
                              ┌─────────────────────────┴─────────────────────────┐
                              │ (Quality Manager Review)                          │
                              ▼                                                   ▼
                    ┌──────────────────┐                                ┌──────────────────┐
                    │     Approved     │                                │     Rejected     │
                    └─────────┬────────┘                                └──────────────────┘
                              │
                              ▼
        [ Recalculates Supplier Overall Score & Grade ]
```

- Every state change occurs inside a database transaction (`transaction.atomic()`).
- State changes write an append-only entry to `ReviewAuditLog` with the actor, timestamp, action, and comment.

---

## 7. Mathematical Scoring Formula & Letter Grades

Implemented in `backend/apps/reviews/models.py` (`QualityReview.calculate_overall_score`) and `backend/apps/suppliers/models.py` (`Supplier.grade`):

### 7.1 Review Weighted Score:
$$\text{Overall Score} = \min(100.00, \max(0.00, (\text{PQ} \times 0.45) + (\text{CS} \times 0.30) + (\text{DS} \times 0.25) - (\text{Defects} \times 0.50)))$$
- **Product Quality ($\text{PQ}$):** 45% weight (core component physical specifications).
- **Compliance Score ($\text{CS}$):** 30% weight (adherence to ISO 9001, AS9100, RoHS).
- **Delivery Reliability ($\text{DS}$):** 25% weight (on-time delivery fulfillment).
- **Defect Penalty:** Deduction of 0.50 points per recorded defective unit.

### 7.2 Supplier Overall Score Recalculation:
When a review is approved, `Supplier.recalculate_overall_score()` calculates the arithmetic mean of all approved reviews for that supplier.

### 7.3 Letter Grade Scale:
| Overall Score Range | Grade | Operational Classification |
| :--- | :---: | :--- |
| $90.00\% - 100.00\%$ | **A+** | Preferred Strategic Partner |
| $80.00\% - 89.99\%$ | **A** | Certified High Quality |
| $70.00\% - 79.99\%$ | **B** | Standard Qualified Vendor |
| $60.00\% - 69.99\%$ | **C** | Conditional Approval (Remediation Plan) |
| $> 0.00\% \text{ and } < 60.00\%$ | **D** | High Risk / Disqualified |
| $0.00\%$ (No Approved Audits) | **N/A** | Uncertified Baseline |

---

## 8. Git $\rightarrow$ Jenkins $\rightarrow$ Testing $\rightarrow$ Docker $\rightarrow$ Deployment Pipeline

```text
  [ Git Commit on develop ]
              │
              ▼
  [ Stage 1: Checkout SCM ]
              │
              ▼
  [ Stage 2: Code Quality & PEP8 Linting (Flake8) ]
              │
              ▼
  [ Stage 3: Automated Pytest Suite (unit-tests.xml) ]
              │
              ▼
  [ Stage 4: Maven Selenium WebDriver Quality Gate ]
              │
              ├─► IF FAILURE (-DinjectDefect=true):
              │     - Captures failure screenshot (failure_*.png)
              │     - Archives screenshot in Jenkins
              │     - STOPS PIPELINE (Prevents Deployment)
              │
              ▼ (IF ALL 4/4 PASS)
  [ Stage 5: Package Release Baseline Artifact (.tar.gz) ]
              │
              ▼
  [ Stage 6: Build Versioned Docker Image (supplier-quality-portal:build-N) ]
              │
              ▼
  [ Stage 7: Deploy Fresh Container Stack (docker compose up -d) ]
              │
              ▼
  [ Stage 8: Automated Health Check Verification (/health/ -> HTTP 200) ]
```

### Distinction Between Pipeline Stages & Standalone Tasks:
- **Integrated in Jenkins (`jenkins/Jenkinsfile`):** Checkout $\rightarrow$ Flake8 linting $\rightarrow$ Pytest $\rightarrow$ Maven Selenium quality gate $\rightarrow$ Release packaging $\rightarrow$ Docker image build $\rightarrow$ Container restart $\rightarrow$ Health probe polling.
- **Separate Standalone Tasks:**
  - Puppet catalog compilation and provisioning on target nodes (`docker exec iac_target_node puppet apply ...`).
  - Ansible provisioning (`site.yml`) and emergency rollback (`rollback.yml`).

---

## 9. Puppet Configuration Management & Automated Rollback

### 9.1 Declarative Puppet Module (`supplier_portal`)
Located in [`infrastructure/puppet/modules/supplier_portal/manifests/init.pp`](file:///c:/Users/Aaditya/.gemini/antigravity-ide/scratch/supplier-quality-portal/infrastructure/puppet/modules/supplier_portal/manifests/init.pp):
- **Packages Managed:** `nginx`, `curl`, `git`, `python3`, `python3-pip`, `docker.io`.
- **User Managed:** System user `deployer` with `sudo` and `docker` secondary groups.
- **Directories Managed:** `/opt/supplier-quality-portal/`, data directories with permissions `0755`.
- **Files Managed:** Nginx reverse proxy virtual host `/etc/nginx/sites-available/supplier_portal.conf`.
- **Services Managed:** `nginx` and `docker` services set to `ensure => running, enable => true`.

### 9.2 Idempotency Proof:
- **Run 1:** Applied catalog in 0.24s $\rightarrow$ `changed > 0` (resources provisioned).
- **Run 2 (Repeat run without state changes):** Applied catalog in 0.08s $\rightarrow$ `changed = 0`, 0 errors.

### 9.3 Automated Ansible Rollback (`rollback.yml`)
Located in [`infrastructure/ansible/rollback.yml`](file:///c:/Users/Aaditya/.gemini/antigravity-ide/scratch/supplier-quality-portal/infrastructure/ansible/rollback.yml):
- Checks out certified Git release tag `v1.0.0`.
- Validates database schema consistency.
- Restarts Gunicorn daemon and polls `/health/` until HTTP 200 is verified.

---

## 10. How to Run Locally

### Option A: Using the One-Click Launcher
Run in the project root:
```cmd
run_all.bat
```
*(or `python run_all.py`)*  
This automatically checks virtual environment dependencies, applies database migrations, launches the server on port 8000, and opens your default browser.

### Option B: Using Docker Compose (Full Multi-Tier Stack)
```bash
# 1. Start all containers (Postgres, Django Web, Nginx)
docker compose -f infrastructure/docker/docker-compose.yml up -d

# 2. Check container status
docker compose -f infrastructure/docker/docker-compose.yml ps

# 3. Open in browser:
# http://localhost/ (Nginx port 80)
```

---

## 11. Intentional Demo Credentials

| Role | Username | Password | Purpose |
| :--- | :--- | :--- | :--- |
| **System Administrator** | `admin` | `Admin@12345` | Full administrative control, user management, supplier CRUD |
| **Quality Manager** | `manager` | `Manager@12345` | Certifying authority: audits, evaluates & approves/rejects |
| **Quality Reviewer** | `reviewer` | `Reviewer@12345` | Factory inspector: inputs audits, records defects |

---

## 12. Known Limitations & Engineering Boundaries

1. **Single-Node Infrastructure:** All containers execute on a single physical host node rather than a multi-node Kubernetes cluster.
2. **Console Email Backend:** Audit approval email notifications log to the standard console rather than an external SMTP relay.
3. **In-Memory Sessions:** User sessions reside in PostgreSQL `django_session` table without a distributed Redis cache cluster.
4. **Binary Chrome Dependency for Selenium:** Running local Maven Selenium tests requires a compatible Chrome browser on the host machine. (In Jenkins CI, Chromium is baked directly into the Docker image).

---

## 13. Top 10 Viva Voce Questions & Authoritative Answers

### Q1: What makes this an enterprise DevOps project rather than just a web application?
**Answer:** The portal implements every phase of the DevOps lifecycle: automated unit testing (Pytest), automated browser quality gates (Selenium WebDriver via Maven), a deliberate defect injection quality gate that halts CI builds, multi-stage Docker containerization with non-root security, declarative Infrastructure as Code using Puppet modules, and automated rollback playbooks via Ansible.

### Q2: How does the quality gate prevent broken builds from deploying?
**Answer:** In Jenkins Stage 4, Maven executes the headless Selenium suite. If any assertion fails (e.g., when `-DinjectDefect=true` is set), TestNG catches the failure, triggers `TestListener` to capture an automated screenshot into `target/screenshots/`, and exits with code 1. Jenkins immediately terminates the pipeline, preventing Docker image creation and container deployment.

### Q3: Why did you implement both Puppet and Ansible?
**Answer:** Puppet and Ansible serve complementary roles:
- **Puppet** is declarative and pull-based, ideal for continuous 24/7 baseline compliance and drift prevention (managing system packages, users, daemons).
- **Ansible** is agentless, push-based, and task-oriented over SSH, ideal for ad-hoc application deployments, schema migrations, and rapid rollbacks triggered by Jenkins.

### Q4: Explain the mathematical scoring formula.
**Answer:** The review score formula is:
$$\text{Overall Score} = \min(100.00, \max(0.00, (\text{PQ} \times 0.45) + (\text{CS} \times 0.30) + (\text{DS} \times 0.25) - (\text{Defects} \times 0.50)))$$
Product quality is weighted highest (45%) because physical part conformity is critical in manufacturing. Compliance (30%) guarantees regulatory conformance, Delivery (25%) tracks SLA timeliness, and physical defect deductions lower the overall score.

### Q5: How is idempotency proven in Puppet and Ansible?
**Answer:** Idempotency is demonstrated through dual execution: Run 1 performs necessary state changes (`changed > 0`), while Run 2 executes the identical catalog without manual intervention and reports strictly `changed = 0`, verifying zero unintended modifications.

### Q6: What is the purpose of the Page Object Model (POM) in Selenium?
**Answer:** POM decouples test logic from HTML DOM locators. If a button ID or input field changes in a template, only the respective Page class (`SupplierPage.java`, `ReviewPage.java`) requires updating; test specifications in `SupplierManagementE2ETest.java` remain untouched.

### Q7: How does your Docker multi-stage build improve security and efficiency?
**Answer:** Stage 1 uses Python build toolchains to compile dependencies into wheel binaries. Stage 2 copies only the compiled packages into a minimal Debian slim runtime image, drops all compilers and development headers, creates a non-root system user `appuser` (UID 999), and reduces the final image size to 121 MB.

### Q8: How was the sidebar routing bug resolved?
**Answer:** DRF's `DefaultRouter` registered `SupplierViewSet` with `basename='supplier'`, which created route names `supplier-list` and `supplier-detail` colliding with Django's HTML views. Changing the router basename to `api-supplier` disambiguated reversing so `{% url 'supplier-list' %}` cleanly points to `/suppliers/` (HTML) while `/api/suppliers/` remains the dedicated JSON REST endpoint.

### Q9: How does the application ensure audit trail immutability?
**Answer:** When an audit review transitions states (`Draft` $\rightarrow$ `Pending Review` $\rightarrow$ `Approved`), an append-only record is written to `ReviewAuditLog` containing the actor foreign key, action verb, timestamp, and manager remarks within an atomic database transaction.

### Q10: How does the health probe integrate with production orchestration?
**Answer:** The `/health/` endpoint performs an active database query (`connection.ensure_connection()`) and returns an RFC-compliant JSON response with HTTP 200. Container orchestrators (Docker Compose, Kubernetes) query this endpoint to determine liveness and readiness.

---

## 14. Important Source Files Reference

| Purpose / Feature | Important Files to Open During Demonstration |
| :--- | :--- |
| **Authentication & RBAC** | [`backend/apps/accounts/models.py`](file:///c:/Users/Aaditya/.gemini/antigravity-ide/scratch/supplier-quality-portal/backend/apps/accounts/models.py), [`backend/apps/accounts/views.py`](file:///c:/Users/Aaditya/.gemini/antigravity-ide/scratch/supplier-quality-portal/backend/apps/accounts/views.py) |
| **Scoring Formula & State Machine** | [`backend/apps/reviews/models.py`](file:///c:/Users/Aaditya/.gemini/antigravity-ide/scratch/supplier-quality-portal/backend/apps/reviews/models.py), [`backend/apps/reviews/views.py`](file:///c:/Users/Aaditya/.gemini/antigravity-ide/scratch/supplier-quality-portal/backend/apps/reviews/views.py) |
| **Supplier Directory & API** | [`backend/apps/suppliers/views.py`](file:///c:/Users/Aaditya/.gemini/antigravity-ide/scratch/supplier-quality-portal/backend/apps/suppliers/views.py), [`backend/apps/suppliers/api_views.py`](file:///c:/Users/Aaditya/.gemini/antigravity-ide/scratch/supplier-quality-portal/backend/apps/suppliers/api_views.py) |
| **Interactive Frontend Templates** | [`backend/templates/suppliers/supplier_list.html`](file:///c:/Users/Aaditya/.gemini/antigravity-ide/scratch/supplier-quality-portal/backend/templates/suppliers/supplier_list.html), [`backend/templates/dashboard/index.html`](file:///c:/Users/Aaditya/.gemini/antigravity-ide/scratch/supplier-quality-portal/backend/templates/dashboard/index.html) |
| **Design System & Theme** | [`backend/static/css/main.css`](file:///c:/Users/Aaditya/.gemini/antigravity-ide/scratch/supplier-quality-portal/backend/static/css/main.css) |
| **CI/CD Pipeline as Code** | [`jenkins/Jenkinsfile`](file:///c:/Users/Aaditya/.gemini/antigravity-ide/scratch/supplier-quality-portal/jenkins/Jenkinsfile), [`jenkins/Jenkinsfile.defect-demo`](file:///c:/Users/Aaditya/.gemini/antigravity-ide/scratch/supplier-quality-portal/jenkins/Jenkinsfile.defect-demo) |
| **Selenium E2E Quality Gate** | [`selenium-tests/src/test/java/com/quality/portal/tests/SupplierManagementE2ETest.java`](file:///c:/Users/Aaditya/.gemini/antigravity-ide/scratch/supplier-quality-portal/selenium-tests/src/test/java/com/quality/portal/tests/SupplierManagementE2ETest.java) |
| **Docker Multi-Stage Build** | [`infrastructure/docker/Dockerfile`](file:///c:/Users/Aaditya/.gemini/antigravity-ide/scratch/supplier-quality-portal/infrastructure/docker/Dockerfile), [`infrastructure/docker/docker-compose.yml`](file:///c:/Users/Aaditya/.gemini/antigravity-ide/scratch/supplier-quality-portal/infrastructure/docker/docker-compose.yml) |
| **Puppet Infrastructure as Code** | [`infrastructure/puppet/modules/supplier_portal/manifests/init.pp`](file:///c:/Users/Aaditya/.gemini/antigravity-ide/scratch/supplier-quality-portal/infrastructure/puppet/modules/supplier_portal/manifests/init.pp) |
| **Ansible Idempotency & Rollback** | [`infrastructure/ansible/site.yml`](file:///c:/Users/Aaditya/.gemini/antigravity-ide/scratch/supplier-quality-portal/infrastructure/ansible/site.yml), [`infrastructure/ansible/rollback.yml`](file:///c:/Users/Aaditya/.gemini/antigravity-ide/scratch/supplier-quality-portal/infrastructure/ansible/rollback.yml) |
