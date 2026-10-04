# 22 - Comprehensive Viva-Voce Defense & Examiner Q&A Guide

**Project Title**: Puppet-Provisioned Supplier Quality Review Portal  
**Student Name**: Aaditya Aswale  
**Student ID**: 23102B0044  
**Course**: DevOps Engineering & Enterprise Cloud Automation  
**Release Tag**: `v1.0.0`  

---

## 1. Top 15 Viva Voce Questions & Authoritative Answers

### Q1: What makes this project an "enterprise-grade DevOps" system rather than just a web application?
**Answer**:
"The portal incorporates every phase of the modern DevOps lifecycle:
1. **Automated Quality Testing**: 4/4 automated headless Selenium WebDriver E2E tests and 5/5 Pytest unit/integration tests running in Maven and Python.
2. **Quality Gates & Continuous Testing**: A deliberate defect injection architecture (`-DinjectDefect=true`) that trips the CI pipeline, prevents broken builds from reaching Docker, and captures automated failure screenshots.
3. **Containerization**: Multi-stage Docker builds separating compiler toolchains from lightweight, non-root runtime containers fronted by Nginx.
4. **Declarative Infrastructure as Code**: Puppet modules enforcing idempotent system configurations, paired with Ansible playbooks for zero-touch deployment and automated rollback.
5. **Observability**: Standardized RFC-compliant `/health/` probes for Kubernetes/load-balancer liveness detection."

---

### Q2: Explain the mathematical formula used for supplier quality scoring. Why are these specific weights chosen?
**Answer**:
"The formula is:
$$\text{Overall Score} = \min(100.00, \max(0.00, (\text{PQ} \times 0.45) + (\text{CS} \times 0.30) + (\text{DS} \times 0.25) - (\text{Defects} \times 0.50)))$$
- **Product Quality (45%)** carries the highest weight because physical component integrity is the core criteria in manufacturing.
- **Compliance (30%)** guarantees adherence to regulatory frameworks such as ISO 9001 and AS9100.
- **Delivery (25%)** ensures just-in-time SLA fulfillment without holding up assembly lines.
- **Defect Penalty (0.50 per unit)** introduces an active penalty deduction that lowers the score if physical batch defects are found."

---

### Q3: Why did you implement both Puppet and Ansible in the same project?
**Answer**:
"Puppet and Ansible serve complementary roles in enterprise architectures:
- **Puppet** is **declarative and pull-based with a continuous agent daemon**. It is optimal for **base infrastructure compliance and drift prevention**, ensuring that system packages, service users, and daemons stay in their certified state 24/7.
- **Ansible** is **agentless, push-based, and task-oriented over SSH**. It is optimal for **application deployment orchestration, rolling updates, database schema migrations, and rapid rollbacks** triggered on demand from a Jenkins CI/CD pipeline."

---

### Q4: How does your Git branching strategy prevent merge conflicts and protect the production branch?
**Answer**:
"We implement the GitFlow branching model:
- `main` is protected and tagged (`v1.0.0`); only certified release commits merge into it.
- `develop` serves as the daily integration trunk.
- Features are developed in isolated branches (`feature/supplier-management`, `feature/review-workflow`) and merged via simulated pull requests.
- To prove conflict resolution competency (Week 6), we intentionally created conflicting commits on `README.md` across `develop` and `feature/conflict-demo`, manually reconciled the three-way conflict markers, committed the resolution (`af4e09d`), and verified a clean tree before tagging."

---

### Q5: What is the purpose of the Page Object Model (POM) in your Selenium test suite?
**Answer**:
"The Page Object Model creates an abstraction layer between the test specifications and the webpage's DOM locators. If a button ID or input name changes in `review_form.html`, only `ReviewPage.java` needs modification; the underlying test assertions in `ReviewWorkflowE2ETest.java` remain untouched. This eliminates test code duplication, ensures maintainability, and provides readable, fluent test scripts."

---

### Q6: How does the system handle database concurrency and preserve audit immutability?
**Answer**:
"Every review state change (`Draft` &rarr; `Pending Review` &rarr; `Approved` / `Rejected`) executes within a Django atomic transaction (`transaction.atomic()`). Furthermore, the `ReviewAuditLog` table is strictly append-only; records are created via automated signals or service methods with a foreign key to the actor, preserving an immutable historical ledger for corporate governance."

---

## 2. Live Viva Voce Demonstration Script

| Step | Action | Expected Output |
|---|---|---|
| **Step 1** | Open browser to `http://127.0.0.1:8000/` | Split-pane login screen with Quick Demo credentials. |
| **Step 2** | Click **Reviewer** quick button & login | Navigates to Dashboard as `reviewer`. |
| **Step 3** | Navigate to `/reviews/create/` | Interactive audit entry form. Enter defect count `2` and scores `90`, `90`, `90`. Observe **Live Calculated Score display 89.00%**. |
| **Step 4** | Click **Submit for Approval** | Review created in `Pending Review` status. Audit log records `CREATED` and `SUBMITTED`. |
| **Step 5** | Logout and click **Manager** quick button & login | Quality Manager dashboard loaded. |
| **Step 6** | Open review & click **Approve** | Provide manager remarks and submit. Status transitions to `Approved`, updating supplier rating. |
| **Step 7** | In terminal run `mvn test -Dheadless=true` | Runs 4 automated Selenium tests in ~10 seconds with **0 failures**. |
| **Step 8** | In terminal run `mvn test -Dheadless=true -DinjectDefect=true` | Demonstrates deliberate quality gate trip and screenshot capture in `target/screenshots/`. |
| **Step 9** | Probe `/health/` via cURL | Returns `{"status": "healthy", "database": "connected"}`. |
