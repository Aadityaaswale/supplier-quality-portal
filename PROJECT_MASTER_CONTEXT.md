# PROJECT MASTER CONTEXT: Puppet-Provisioned Supplier Quality Review Portal

> **AUTHORITATIVE MASTER RECOVERY CONTEXT & PERMANENT RECORD**  
> **Student:** AADITYA ASWALE | **Student ID:** 23102B0044  
> **Degree / Branch:** Bachelor of Technology / Computer Engineering  
> **Project Title:** Puppet-Provisioned Supplier Quality Review Portal  
> **Repository Path:** `C:\Users\Aaditya\.gemini\antigravity-ide\scratch\supplier-quality-portal`  
> **Last Updated Baseline:** Release v1.0.0 (`develop` / `main` branches)  
> **Academic Model:** 15-Week Authoritative DevOps Lifecycle Curriculum

---

## 1. Executive Project Description

The **Supplier Quality Review Portal** is an enterprise-grade SaaS web application engineered for manufacturing, supply-chain, and quality engineering teams to audit, track, evaluate, and benchmark vendor quality compliance. 

The system features:
- **Role-Based Access Control (RBAC):** Dedicated permissions across **Admin**, **Quality Manager**, and **Reviewer** roles.
- **Supplier Directory & Lifecycle Management:** Complete vendor profiles with statuses (`Active`, `Under Review`, `Suspended`, `Inactive`), categories, SLA tracking, and historical audit metrics.
- **Audit Review Engine:** Defect counting, weighted scoring calculations across product quality (45%), compliance (30%), and on-time delivery (25%), with mathematical defect rate penalties.
- **Quality Review Workflow:** Formal lifecycle state machine: `Draft` -> `Pending Review` -> `Approved` or `Rejected` with manager sign-off remarks and complete audit logging.
- **Executive Analytics Dashboard:** Real-time KPI summaries, quality grade distributions (A+, A, B, C, D, F) powered by Chart.js, CSV export capabilities, and live health probes.
- **Full DevOps Lifecycle Integration:** Git branching governance, Pytest unit tests, Apache Maven + Java Selenium E2E WebDriver quality gates, Docker containerization & Compose orchestration, Jenkins Declarative Pipelines, and Infrastructure-as-Code (IaC) with Puppet & Ansible.

---

## 2. Student & Academic Information

- **Student Name:** AADITYA ASWALE
- **Student ID:** 23102B0044
- **Academic Course:** Bachelor of Technology (Computer Engineering)
- **Course Subject:** DevOps Lifecycle Laboratory & Capstone Project
- **Project Name:** Puppet-Provisioned Supplier Quality Review Portal
- **Term:** 15-Week Full DevOps Curriculum (Weeks 1 to 15)

---

## 3. Authoritative 15-Week Curriculum Requirements

| Week | Milestone Title | Authoritative Curriculum Requirement |
| :--- | :--- | :--- |
| **Week 1** | Problem Definition and Scope | Study real-time/business need; identify target users, pain points, stakeholders, constraints, and measurable success criteria. Freeze a small, achievable 15-week MVP scope. |
| **Week 2** | Agile Planning and DevOps Workflow | Create user stories, acceptance criteria, product backlog, 15-week Kanban/Scrum implementation plan, Definition of Done (DoD), and end-to-end DevOps workflow diagram. |
| **Week 3** | Requirements, Architecture and Tech Setup | Minimum working application architecture with full CRUD, RBAC, dashboard. Define stack (Django, PostgreSQL, Maven, etc.) and create SRS, use-case, architecture, data model, and API documentation. |
| **Week 4** | Git and GitHub Repository Initialization | Configure Git repo, README, `.gitignore`, clean folder structure, issue templates, branch policies, initial project skeleton, and meaningful commit history. |
| **Week 5** | Feature Development with Branching | Implement first core business workflow using a feature branch (`feature/supplier-management`). Demonstrate `add`, `commit`, `push`, `pull`, `log`, feature branch PR, review comments, and merge into `develop`. |
| **Week 6** | MVP Completion and Git Collaboration | Complete remaining MVP (reviews, workflow, dashboard). Demonstrate second feature branch (`feature/review-workflow`), merge conflict creation and resolution (`feature/conflict-demo`), release tag `v1.0.0`, and release-ready source baseline. |
| **Week 7** | Jenkins Installation and Continuous Integration | Actual Jenkins installation & execution. Connect Git repo, configure CI pipeline, integrate build tool (pip/pytest), trigger build via commit/polling, archive build artifact (`.tar.gz`). |
| **Week 8** | Pipeline as Code and Server Deployment | Jenkins Declarative Pipeline (`Jenkinsfile`) with checkout, build, package, and deploy stages. Environment parameterization, deployment to target web server, and verification of deployed application. |
| **Week 9** | Selenium Test Design and Local Execution | Identify 3–5 critical user journeys. Implement Java + Selenium WebDriver suite managed via Apache Maven (`pom.xml`) with Page Object Model, TestNG, assertions, test data, and failure screenshot capture mechanism. |
| **Week 10** | Continuous Testing in Jenkins | Integrate Selenium tests into Jenkins quality gate. Test reports published. Deliberate defect injection demonstration (`-DinjectDefect=true`), failure of quality gate halting deployment, bugfix commit, and successful rerun. |
| **Week 11** | Docker Image and Container Lifecycle | Production multi-stage `Dockerfile`, image build, versioned tagging (`supplier-quality-portal:v1.0.0`), port mapping, container logs, start/stop/restart lifecycle verification, and application health validation. |
| **Week 12** | Jenkins-Docker Continuous Deployment | End-to-end commit-to-container continuous deployment: Git commit -> Jenkins -> Build -> Tests -> Docker versioned image -> Local registry -> Fresh container deployment. |
| **Week 13** | Configuration Management Script | Specify server prerequisites (packages, users, directories, services, ports). Create declarative Puppet manifest/module (`supplier_portal`) and secondary Ansible playbook (`site.yml`). |
| **Week 14** | Automated Provisioning and Reliability Validation | Clean-node execution of Puppet/Ansible. Verify idempotency (`changed=0` on second run). Application health check verification (`/health/`). Rollback playbook (`rollback.yml`) restoring previous stable baseline. |
| **Week 15** | Final Release, Documentation and Viva | Final end-to-end release pipeline, complete 22-part technical documentation suite, architecture diagrams, operations guide, presentation slide deck, and comprehensive Viva-Voce defense package. |

---

## 4. Technology Stack & Monolithic Architecture

- **Backend:** Python 3.12, Django 5.1+, Django REST Framework 3.15+
- **Database:** PostgreSQL 16 (production), SQLite 3 (fallback / unit testing)
- **WSGI Application Server:** Gunicorn 26.2.0 (3 sync worker processes)
- **Reverse Proxy & Web Server:** Nginx 1.25 Alpine (HTTP Port 80, static/media file serving, cache control)
- **Frontend / UI:** HTML5, CSS3 Custom Modern Dark Design System, Phosphor Icons, Chart.js 4.4
- **Backend Testing:** Pytest 9.1+, Pytest-Django, JUnit XML output
- **E2E Browser Testing:** Java JDK 17/23, Apache Maven 3.9+, Selenium WebDriver 4.20+, TestNG 7.9+, Chrome Headless
- **Continuous Integration / Continuous Deployment:** Jenkins LTS, Declarative `Jenkinsfile`
- **Containerization & Orchestration:** Docker Engine 29.8+, Docker Compose v5+, Multi-stage build
- **Configuration Management (IaC):** Puppet 7/8 declarative modules (`init.pp`, `site.pp`), Ansible 2.15+ (`site.yml`, `rollback.yml`)

---

## 5. Repository Structure

```text
supplier-quality-portal/
├── PROJECT_MASTER_CONTEXT.md          # Permanent Master Requirements & Project Status (This File)
├── README.md                          # Primary Project Documentation & Academic Badges
├── .flake8                            # Flake8 Linting Rules (PEP8 Configuration)
├── .gitattributes                     # Git line-ending normalization (LF for shell scripts)
├── .gitignore                         # SCM ignore rules (virtual environments, artifacts, caches)
├── .env.example                       # Reference environment variable specification
│
├── backend/                           # Django Modular Monolith Application
│   ├── manage.py                      # Django administrative CLI
│   ├── pytest.ini                     # Pytest runner configuration
│   ├── requirements.txt               # Pinned Python package dependencies
│   ├── config/                        # Django configuration package (settings, urls, wsgi, asgi)
│   ├── apps/
│   │   ├── accounts/                  # User authentication, profiles & RBAC middleware
│   │   ├── suppliers/                 # Supplier directory, CRUD, searching, and models
│   │   ├── reviews/                   # Quality review engine, scoring logic, workflow states
│   │   ├── dashboard/                 # Executive analytics, aggregations, REST API views
│   │   └── reports/                   # CSV report generation & data exports
│   ├── templates/                     # Semantic HTML5 UI templates
│   ├── static/                        # CSS styles, JavaScript bundles, phosphor icons
│   └── tests/                         # Pytest unit and integration test suite
│
├── selenium-tests/                    # Standalone Java Maven Selenium WebDriver Suite
│   ├── pom.xml                        # Maven build & test dependency definition
│   └── src/test/java/com/quality/portal/
│       ├── pages/                     # Page Object Model classes (Login, Dashboard, Supplier, Review)
│       ├── tests/                     # TestNG E2E test cases
│       └── utils/                     # WebDriver manager & screenshot failure listener
│
├── jenkins/                           # Jenkins Pipeline as Code
│   ├── Jenkinsfile                    # Primary 8-stage Declarative CI/CD pipeline
│   ├── Jenkinsfile.defect-demo        # Week 10 deliberate defect quality gate demo pipeline
│   └── scripts/                       # Automation helper scripts
│
├── infrastructure/                    # Infrastructure as Code & Orchestration
│   ├── docker/
│   │   ├── Dockerfile                 # Production multi-stage Docker build
│   │   ├── docker-compose.yml         # 3-tier service definition (db, web, nginx)
│   │   └── entrypoint.sh              # Auto-migration, static collection & startup script
│   ├── nginx/
│   │   └── default.conf               # Nginx reverse proxy configuration & static cache rules
│   ├── puppet/                        # Puppet Declarative IaC
│   │   ├── manifests/site.pp          # Puppet master site node definition
│   │   └── modules/supplier_portal/   # Declarative module (packages, service, files, health probe)
│   └── ansible/                       # Ansible Automation
│       ├── inventory.ini              # Server target inventory
│       ├── site.yml                   # Idempotent provisioning & deployment playbook
│       └── rollback.yml               # Automated release rollback recovery playbook
│
├── scripts/                           # Local execution helper scripts
│   ├── run_local.bat                  # Local Windows virtualenv launcher
│   ├── run_selenium.bat               # Windows Maven Selenium test execution batch file
│   └── seed_data.py                   # CLI data population script
│
└── docs/                              # Comprehensive 22-part Technical Documentation Suite
    ├── 15_WEEK_REQUIREMENTS_TRACEABILITY.md # Detailed 15-week traceability matrix
    ├── 01-problem-definition.md through 22-viva-voce-defense-guide.md
```

---

## 6. Functional Requirements & Demo Credentials

### Pre-Configured Demo Accounts:
- **System Administrator:** `admin` / `Admin@12345` (Full access, system setup, user administration)
- **Quality Manager:** `manager` / `Manager@12345` (Review sign-off/rejection, analytics, supplier approval)
- **Quality Reviewer:** `reviewer` / `Reviewer@12345` (Audit evaluation creation, score computation, draft saves)

### Dynamic Scoring Formula:
$$\text{Overall Score} = (\text{Product Quality} \times 0.45) + (\text{Compliance} \times 0.30) + (\text{Delivery} \times 0.25) - (\text{Defects} \times 0.50)$$

---

## 7. Current Project Implementation & Verification Audit

| Requirement | Implementation State | Actual Execution State | Verification Status | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Week 1: Scope & Problem** | Complete (`docs/01-problem-definition.md`) | Verified document baseline | **VERIFIED** | Scope frozen, stakeholders approved. |
| **Week 2: Agile & Workflow** | Complete (`docs/03-user-stories-and-backlog.md`) | Verified document baseline | **VERIFIED** | User stories, backlog, DoD defined. |
| **Week 3: Tech Setup & SRS** | Complete (`backend/`, `docs/05-srs.md`) | Verified code & architecture | **VERIFIED** | Django modular monolith, REST API ready. |
| **Week 4: Git Repo Init** | Complete (`.git`, `README.md`, `.gitignore`) | Branches and history verified | **VERIFIED** | Clean commits, branch naming convention. |
| **Week 5: Feature Branching** | Complete (`feature/supplier-management`) | Merged into `develop` | **VERIFIED** | PR commit history preserved in git log. |
| **Week 6: MVP Completion & Tag**| Complete (Full CRUD, conflict demo resolved) | Release tag `v1.0.0` verified | **VERIFIED** | Conflict resolution commit `af4e09d`. |
| **Week 7: Jenkins CI Server** | Complete (`jenkins/Jenkinsfile`) | Live Jenkins LTS (`jenkins_ci_server`) Build #1 & #3 | **VERIFIED** | Clean CI execution; archived `dist/supplier-portal-build-3.tar.gz` & `unit-tests.xml`. |
| **Week 8: Pipeline as Code** | Complete (`jenkins/Jenkinsfile`) | Declarative Pipeline run (Build #3) | **VERIFIED** | 6 declarative stages executed; deployed stack; `/health/` HTTP 200 verified. |
| **Week 9: Selenium via Maven** | Complete (`selenium-tests/`, `pom.xml`) | Executed `mvn clean test` (4/4 PASS) | **VERIFIED** | Headless Chrome against live portal in 14.93s. |
| **Week 10: Quality Gate & Defect**| Complete (`NegativeDefectValidationTest.java`) | Executed `-DinjectDefect=true` | **VERIFIED** | Screenshot captured to `target/screenshots/`; halted pipeline. Clean rerun passed. |
| **Week 11: Docker Lifecycle** | Complete (`Dockerfile`, `compose.yml`) | Multi-stage build, run, stop, start | **VERIFIED** | 121 MB image, non-root `appuser`, healthy stack on ports 80 & 8000. |
| **Week 12: Jenkins-Docker CD** | Complete (`docker-compose.yml`, `Jenkinsfile`) | Automated CD stage in Jenkins Build #3 | **VERIFIED** | Built image `supplier-quality-portal:build-3`, launched fresh stack, verified health probe. |
| **Week 13: Puppet IaC Module** | Complete (`infrastructure/puppet/`) | `docker exec iac_target_node puppet apply` | **VERIFIED** | Compiled in 0.46s, managed packages, user, dirs, nginx reverse proxy & services. |
| **Week 14: Provision & Idempotency**| Complete (`site.yml`, `rollback.yml`)| Dual Ansible execution & rollback | **VERIFIED** | Run 1: `changed=3`; Run 2 (Idempotency): `changed=0`; Rollback: restored `v1.0.0` with HTTP 200. |
| **Week 15: Final Docs & Viva** | Complete (23 technical documents in `docs/`) | Complete documentation & presentation | **VERIFIED** | All academic criteria, slide deck (`23-final-project-presentation.md`), & viva package complete. |

---

## 8. Current Status & Deliverable Summary

1. **Overall Curriculum Status:** 100% Complete (15 of 15 Weeks Fully Verified with Real Execution Logs).
2. **Key Execution Artifacts:**
   - Jenkins Controller running on `http://localhost:8080/` with verified Build #1 and Build #3.
   - Live Application Stack running on `http://localhost:80/` (Nginx + Gunicorn + PostgreSQL).
   - Apache Maven Selenium Suite passing 100% (`BUILD SUCCESS`) in `selenium-tests/`.
   - Puppet module catalog compiled and applied cleanly inside `iac_target_node`.
   - Ansible provisioning executed (`changed=3`), idempotency proven (`changed=0`), and automated rollback verified (`ROLLBACK SUCCESSFUL`).
   - Self-contained traceability matrix in [`docs/15_WEEK_REQUIREMENTS_TRACEABILITY.md`](file:///c:/Users/Aaditya/.gemini/antigravity-ide/scratch/supplier-quality-portal/docs/15_WEEK_REQUIREMENTS_TRACEABILITY.md).
   - Final presentation slide deck in [`docs/23-final-project-presentation.md`](file:///c:/Users/Aaditya/.gemini/antigravity-ide/scratch/supplier-quality-portal/docs/23-final-project-presentation.md).

---

## 9. Manual Intervention Protocol

Automate all safe, standard development commands. If a genuinely manual, human-only action is required (e.g., UAC prompt, external physical network change), pause and use:

```text
🛑 MANUAL ACTION REQUIRED

WHY:
<concise explanation>

DO THIS:
<exact steps>

COMMAND:
<exact command if applicable>

EXPECTED RESULT:
<expected result>

Then wait for:
DONE — continue
```
