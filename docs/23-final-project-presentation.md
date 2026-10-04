# Final Project Presentation Slide Deck & Defense Package

**Project Title:** Puppet-Provisioned Supplier Quality Review Portal  
**Student Name:** AADITYA ASWALE  
**Student ID:** 23102B0044  
**Degree:** Bachelor of Technology in Computer Engineering  
**Academic Curriculum:** 15-Week DevOps & Software Engineering Practicum  

---

## Slide 1: Title & Executive Summary
- **Title:** Puppet-Provisioned Supplier Quality Review Portal
- **Presenter:** Aaditya Aswale (23102B0044)
- **Domain:** Enterprise Quality Engineering & Continuous Delivery (DevOps)
- **Key Highlights:**
  - Automated supplier qualification and multi-criteria audit workflow.
  - Role-Based Access Control (Admin, Quality Manager, Reviewer).
  - 100% automated CI/CD pipeline from Git commit to Docker container deployment.
  - Infrastructure as Code (IaC) using declarative Puppet modules and idempotent Ansible playbooks.
  - Automated Selenium WebDriver regression quality gate.

---

## Slide 2: Problem Statement & Real-Time Business Need (Week 1)
- **The Challenge:** Modern manufacturing, aerospace, and automotive enterprises rely on hundreds of external vendors. Managing audits, compliance, delivery tracking, and defect metrics across disparate spreadsheets leads to:
  - Data silos and lack of audit traceability.
  - Subjective, error-prone vendor evaluations.
  - Delayed defect resolution and compliance risks.
- **The Solution:** A centralized, role-based Supplier Quality Review Portal with real-time scoring algorithms, automated audit status workflows, and interactive analytics.

---

## Slide 3: System Architecture & Technology Stack (Weeks 2 & 3)
- **Architecture:** Modular Monolith designed for high maintainability, low operational complexity, and seamless containerization.
- **Backend:** Python 3.10 / Django 5.1 / Django REST Framework.
- **Database:** PostgreSQL 16 (production) with SQLite local fallback.
- **Frontend:** Semantic HTML5, CSS3, Bootstrap 5, Chart.js.
- **Automated Testing:** Pytest, Flake8, Selenium WebDriver (Java/Maven).
- **CI/CD & DevOps:** Jenkins LTS, Docker & Docker Compose, Nginx Reverse Proxy.
- **Configuration Management:** Puppet (declarative) & Ansible (task-oriented).

---

## Slide 4: Git Collaboration & Branching Strategy (Weeks 4, 5 & 6)
- **Git Flow Baseline:** Branch `main` for release-ready code; `develop` for integration.
- **Feature Branches:** 
  - `feature/supplier-management` (commit `566c5ba` merged via PR)
  - `feature/review-workflow` (commit `6218ca5` merged via PR)
  - `feature/conflict-demo` (deliberate merge conflict created and resolved cleanly in commit `af4e09d`)
- **Release Baseline:** Tagged `v1.0.0` marking the frozen MVP scope.

---

## Slide 5: Core Application Capabilities (Weeks 5 & 6)
- **Supplier Directory:** Full CRUD operations, ISO certification tracking, status filtering (Active, Under Review, Suspended, Inactive).
- **Multi-Factor Quality Scoring:** Weighted algorithm calculating overall score from:
  - Product Quality Score (35%)
  - Delivery Reliability Score (25%)
  - Audit Compliance Score (25%)
  - Service & Responsiveness (15%)
  - Defect Deductions (-2 points per recorded defect)
- **Workflow State Engine:** Draft → Pending Review → Approved / Rejected with role enforcement.
- **Real-Time Analytics:** Chart.js dashboards showing score distributions, category breakdowns, and audit timelines.

---

## Slide 6: Continuous Integration with Jenkins (Weeks 7 & 8)
- **Jenkins Controller:** Deployed via Docker with complete build tools and Docker-out-of-Docker (DooD) socket integration.
- **Pipeline as Code:** Declarative `Jenkinsfile` featuring 6 automated stages:
  1. `Checkout`: Git repository synchronization.
  2. `Static Code Analysis`: Flake8 linting enforcement (0 errors).
  3. `Unit & Integration Tests`: Pytest test suite with JUnit XML reporting.
  4. `Package`: Compressed distribution artifact archiving (`supplier-portal-*.tar.gz`).
  5. `Docker Build & Tag`: Build versioned container image (`supplier-quality-portal:build-3`).
  6. `Continuous Deployment`: Automated container restart & HTTP 200 health check verification.

---

## Slide 7: Automated End-to-End Testing (Weeks 9 & 10)
- **Framework:** Java 17, Selenium WebDriver 4.18, Apache Maven, TestNG.
- **Architecture:** Page Object Model (POM) separating locator definitions from test logic.
- **Test Journeys Verified:**
  - `LoginDashboardE2ETest`: Authentication and KPI metric rendering.
  - `SupplierManagementE2ETest`: Supplier creation and profile validation.
  - `ReviewWorkflowE2ETest`: Full lifecycle audit submission and approval.
  - `NegativeDefectValidationTest`: Quality gate boundary validation.
- **Continuous Quality Gate:** Deliberate defect injection (`-DinjectDefect=true`) proven to fail assertion, capture screenshot to `target/screenshots/`, and halt pipeline.

---

## Slide 8: Containerization & Docker Lifecycle (Week 11)
- **Production Dockerfile:** Multi-stage build minimizing attack surface and image size (121 MB).
- **Security:** Non-root execution (`appuser:appuser`, UID 10001).
- **Full Lifecycle Demonstrated:**
  - `docker build`: Compiled and tagged `v1.0.0` and versioned build tags.
  - `docker run`: Deployed with mapped ports (80:80, 8000:8000).
  - `docker inspect`: Verified container healthchecks and network bridges.
  - `docker stop / restart`: Verified persistence across PostgreSQL volumes.

---

## Slide 9: Infrastructure as Code with Puppet (Week 13)
- **Declarative Puppet Module (`supplier_portal`):**
  - Managed Packages: `nginx`, `curl`, `git`, `python3`, `python3-pip`, `docker.io`.
  - Managed Users: `deployer` system account with `sudo` and `docker` groups.
  - Managed Files: `/opt/supplier-quality-portal/`, data directories, Nginx reverse proxy configuration.
  - Managed Services: `nginx` and `docker` services.
- **Execution & Validation:** Catalog compiled in 0.46s, applied with 0 syntax errors, and verified in `--noop` simulation and live execution.

---

## Slide 10: Provisioning & Idempotency Validation (Week 14)
- **Ansible Automation (`site.yml`):**
  - **Run 1 (Initial Provisioning):** `changed = 3`, `failed = 0`. System packages installed, directories provisioned, Nginx reverse proxy deployed and reloaded, health probe passed HTTP 200.
  - **Run 2 (Idempotency Check):** `changed = 0`, `failed = 0`. Complete system verified with zero unintended modifications.
- **Automated Rollback (`rollback.yml`):**
  - Simulated production incident and triggered automated rollback to stable tag `v1.0.0`.
  - Service health verified and confirmed: `ROLLBACK SUCCESSFUL: Restored service health status is healthy`.

---

## Slide 11: 15-Week Curriculum Traceability Summary
- **100% Real Execution & Zero Fabrication:**
  - Weeks 1–6 (Agile, Architecture, Git Flow, MVP): **VERIFIED**
  - Weeks 7–8 (Jenkins CI & Declarative Pipeline): **VERIFIED**
  - Weeks 9–10 (Maven Selenium & Quality Gate): **VERIFIED**
  - Weeks 11–12 (Docker Lifecycle & Jenkins CD): **VERIFIED**
  - Weeks 13–14 (Puppet IaC & Ansible Idempotency): **VERIFIED**
  - Week 15 (Documentation, Slide Deck, Defense Package): **VERIFIED**

---

## Slide 12: Viva Q&A Quick Reference
- **Q: Why combine Puppet and Ansible?**  
  *A:* Puppet provides declarative state enforcement ideal for base infrastructure baseline management, while Ansible provides procedural orchestration ideal for ad-hoc application deployments and zero-downtime rollbacks.
- **Q: How does the quality gate prevent defective code from reaching production?**  
  *A:* Maven Selenium tests execute in headless Chrome during CI. If any assertion fails, TestNG halts execution, Jenkins captures failure screenshots, and the pipeline aborts before the Docker build and deployment stages are triggered.
- **Q: How is idempotency proven?**  
  *A:* Ansible's play recap produces `changed > 0` on first provisioning and strictly `changed = 0` on subsequent runs without system drift.
