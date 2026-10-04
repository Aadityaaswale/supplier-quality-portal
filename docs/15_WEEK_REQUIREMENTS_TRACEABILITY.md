# 15-Week Authoritative Requirements Traceability Matrix

**Project:** Puppet-Provisioned Supplier Quality Review Portal  
**Student:** AADITYA ASWALE (Student ID: 23102B0044)  
**Academic Degree:** Bachelor of Technology in Computer Engineering  
**Repository Baseline:** Release Tag `v1.0.0` | Active Branch: `develop`  
**Standard Status Legend:**
- `NOT STARTED`: Requirement not yet implemented or designed.
- `IMPLEMENTED`: Code, configuration, or documentation files are written and present in repository.
- `EXECUTED`: Actual command or pipeline run has been triggered.
- `VERIFIED`: Actual execution logs, assertions, tests, and outputs have been verified and confirmed successful.
- `BLOCKED`: Work cannot proceed due to an environmental or external dependency issue.

---

## Traceability Matrix

| Week | Milestone Requirement | Implementation Location & Files | Execution Command / Tool | Expected Verification Result | Evidence Required | Current Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Week 1** | Problem definition, stakeholder analysis, constraints, measurable criteria, frozen MVP scope | `docs/01-problem-definition.md`, `README.md` | Formal requirements review | Frozen MVP scope with 3 roles, suppliers & audit scoring | Approved SRS problem statement & boundary | **VERIFIED** |
| **Week 2** | Agile user stories, acceptance criteria, backlog, 15-week sprint plan, DoD, DevOps workflow diagram | `docs/03-user-stories-and-backlog.md`, `docs/02-software-requirements-specification.md` | Agile backlog inspection | Prioritized product backlog with sprint mapping and Mermaid workflow | Backlog table, DoD checklist, and workflow diagram | **VERIFIED** |
| **Week 3** | Minimum working application architecture, modular monolith setup, data models, REST API list, local dev setup | `backend/`, `backend/config/settings.py`, `docs/04-database-design.md`, `docs/05-rest-api-documentation.md` | `python backend/manage.py check` | Clean Django app registry, database models mapped, settings configured | Working Django project structure, UML data models | **VERIFIED** |
| **Week 4** | Git repository initialization, GitHub structure, `.gitignore`, branch policy, issue templates, meaningful commit history | `.git`, `.gitignore`, `.gitattributes`, `README.md`, `.github/` | `git status`, `git log --oneline` | Clean working tree, appropriate ignore rules, standard commit messages | Git log history, branch pointers | **VERIFIED** |
| **Week 5** | Feature branch development (`feature/supplier-management`), git workflow (`add`, `commit`, PR, code review, merge to `develop`) | Git branch `feature/supplier-management`, commit `566c5ba`, merge commit `0b8cc6e` | `git log --graph --oneline` | Branch created, feature implemented, merged cleanly to `develop` | Branch history & PR merge log in Git tree | **VERIFIED** |
| **Week 6** | MVP completion, second feature branch (`feature/review-workflow`), merge conflict creation and resolution (`feature/conflict-demo`), release tag `v1.0.0` | Git branch `feature/conflict-demo`, commit `af4e09d`, tag `v1.0.0` | `git tag -l -n`, `git log -n 1 v1.0.0` | Conflict in README resolved; release tag `v1.0.0` created | Tag `v1.0.0` commit pointer & conflict resolution log | **VERIFIED** |
| **Week 7** | Real Jenkins server installation, Git repository connection, CI pipeline job configuration, build trigger, archived build artifact (`.tar.gz`) | `jenkins/Jenkinsfile`, Live Jenkins LTS container (`jenkins_ci_server`), Job `supplier-quality-portal-ci` | `python scripts/setup_jenkins_job.py` / Jenkins Job Build #1 & #3 | Real Jenkins instance executed job, Flake8 clean, Pytest passed, archived `dist/supplier-portal-build-3.tar.gz` | Jenkins Build #3 console log, archived build tarball & `unit-tests.xml` | **VERIFIED** |
| **Week 8** | Pipeline as Code (`Jenkinsfile`) with stages (Checkout, Build, Package, Deploy), environment parameterization, deployed app verification | `jenkins/Jenkinsfile`, target server stack | Jenkins Declarative Pipeline run (Build #3) | Pipeline executed 6 declarative stages cleanly, deployed container stack, verified `/health/` HTTP 200 | Jenkins Build #3 stage view log, HTTP 200 health probe output | **VERIFIED** |
| **Week 9** | Java Selenium WebDriver suite executed locally via Apache Maven (`pom.xml`), Page Object Model, failure screenshot capture | `selenium-tests/`, `selenium-tests/pom.xml`, `selenium-tests/src/` | `mvn clean test -Dheadless=true` | 4/4 test journeys pass (Login, Dashboard, Supplier, Review Workflow) | Maven `BUILD SUCCESS` log, Surefire XML reports | **VERIFIED** |
| **Week 10**| Continuous Testing in Jenkins, deliberate defect injection demonstration (`-DinjectDefect=true`), failure halts deployment, bugfix rerun | `jenkins/Jenkinsfile.defect-demo`, `NegativeDefectValidationTest.java` | `mvn test -DinjectDefect=true` | Quality gate intentionally halts build, captures screenshot to `target/screenshots/`; clean rerun passes | Injected defect assertion log, archived failure screenshot | **VERIFIED** |
| **Week 11**| Multi-stage production `Dockerfile`, versioned tagging (`supplier-quality-portal:v1.0.0`), container lifecycle (run, logs, inspect, stop, start), healthcheck | `infrastructure/docker/Dockerfile`, `docker-compose.yml`, `entrypoint.sh` | `docker build -t supplier-quality-portal:v1.0.0`, `docker inspect`, `docker compose stop/start` | Multi-stage image 121 MB, non-root user `appuser`, healthy PostgreSQL/Gunicorn/Nginx containers | Container inspect JSON, `docker compose ps` healthy output | **VERIFIED** |
| **Week 12**| Jenkins-Docker continuous deployment workflow (Commit -> Build -> Test -> Docker build -> Deploy fresh container) | `jenkins/Jenkinsfile`, `infrastructure/docker/docker-compose.yml` | Jenkins Declarative Pipeline Stage `Continuous Deployment` | Automated commit-to-container pipeline built image `supplier-quality-portal:build-3`, launched fresh stack, verified health probe | Jenkins Build #3 console output, live container health probe | **VERIFIED** |
| **Week 13**| Server prerequisites configuration management using Puppet module (`supplier_portal`) and secondary Ansible playbook (`site.yml`) | `infrastructure/puppet/modules/supplier_portal/manifests/init.pp`, `infrastructure/puppet/manifests/site.pp`, `infrastructure/ansible/site.yml` | `docker exec iac_target_node puppet apply --modulepath=/infrastructure/puppet/modules /infrastructure/puppet/manifests/site.pp --verbose` | Catalog compiled in 0.46s; managed packages, deployer user, directories, Nginx conf & services | Puppet execution log, catalog compilation report, 0 syntax errors | **VERIFIED** |
| **Week 14**| Automated provisioning on clean environment, idempotency validation (`changed=0` on rerun), health check, automated rollback (`rollback.yml`) | `infrastructure/ansible/site.yml`, `infrastructure/ansible/rollback.yml`, Puppet manifests | `docker exec iac_target_node ansible-playbook -i /infrastructure/ansible/inventory.ini /infrastructure/ansible/site.yml` | Run 1: `changed=3`, `failed=0`; Run 2 (Idempotency): `changed=0`, `failed=0`; Rollback: stable `v1.0.0` restored | Real execution logs with change counters (`3` -> `0`), rollback health check confirmation | **VERIFIED** |
| **Week 15**| Complete technical documentation suite (23 files), user manual, architecture models, presentation slide deck, viva defense guide | `docs/01-problem-definition.md` through `docs/23-final-project-presentation.md`, `README.md` | Full academic deliverables review | Complete documentation covering all academic criteria, presentation deck, and viva defense questions | 23 comprehensive Markdown files in `docs/`, working application & CI/CD/IaC evidence | **VERIFIED** |

---

## Summary of Verification Progress

- **Total Curriculum Weeks:** 15
- **Fully Verified Weeks (Real Execution + Output Logs Confirmed):** ALL 15 WEEKS (Weeks 1 through 15)
- **Implemented, Pending Execution Verification:** 0
- **Blocked Weeks:** 0
- **Overall Completion:** 100% Complete, Fully Traceable, Self-Contained and Audited.
