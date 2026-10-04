# 24 - Enterprise Troubleshooting, System Limitations & Future Enhancements

**Project Title**: Puppet-Provisioned Supplier Quality Review Portal  
**Student Name**: Aaditya Aswale  
**Student ID**: 23102B0044  
**Curriculum**: DevOps Engineering & Enterprise Cloud Automation (Week 15 Release)  
**Standard**: IEEE 829 Software Test & Engineering Operations Standard  

---

## 1. System Setup & Architecture Quick-Start

### 1.1 Deployment Topology
The system operates as a containerized multi-tier micro-infrastructure orchestrated via Docker Compose:
- **Nginx Reverse Proxy (`supplier_portal_nginx`)**: Listens on port `80`, routing static assets and proxying dynamic requests.
- **Django Application (`supplier_portal_web`)**: Python 3.10 / Django 5.1 running under Gunicorn on port `8000`.
- **PostgreSQL Database (`supplier_portal_db`)**: Version 16 Alpine running on internal port `5432` with persistent Docker volumes.
- **Jenkins CI Server (`jenkins_ci_server`)**: Jenkins LTS listening on port `8080` with JDK 17, Maven 3.9, and Chromium headless.
- **IaC Target Node (`iac_target_node`)**: Ubuntu 22.04 LTS container with Puppet agent and SSH daemon for configuration management.

### 1.2 Quick-Start Commands
```bash
# 1. Start application stack
docker compose -f infrastructure/docker/docker-compose.yml up -d

# 2. Verify all services are healthy
docker compose -f infrastructure/docker/docker-compose.yml ps

# 3. Test HTTP health endpoint
curl -f http://localhost/health/
```

---

## 2. Comprehensive Troubleshooting Runbook

This runbook documents actual challenges encountered, diagnosed, and resolved during the 15-week implementation lifecycle:

| Failure / Symptom | Root Cause Analysis | Diagnostic Command | Permanent Engineering Resolution |
|---|---|---|---|
| **Django HTTP 400 `Invalid HTTP_HOST header`** | Django strictly enforces RFC 1034 hostname standards. Hostnames containing underscores (e.g., `supplier_portal_web`) are rejected by Django's `ALLOWED_HOSTS` validator. | `docker logs supplier_portal_web --tail 50` | Updated `ALLOWED_HOSTS = ['*']` in settings and ensured Nginx passes `proxy_set_header Host $host;` matching `localhost` or standard FQDNs. |
| **Jenkins Chromium Headless Crash in Container** | Containerized Chromium requires Linux shared memory and sandboxing bypass (`/dev/shm` limitations in Docker). | `docker exec jenkins_ci_server chromium --version` | Configured Chrome options in `BaseSeleniumTest.java`: `--headless=new`, `--no-sandbox`, `--disable-dev-shm-usage`, and `--disable-gpu`. |
| **Selenium Timing Race Condition during Login Redirect** | Rapid assertion checks failed before Django completed session cookie negotiation and redirected from `/accounts/login/` to `/`. | Inspect TestNG log: expected `http://localhost/` but found `http://localhost/accounts/login/` | Implemented explicit `WebDriverWait` in `SupplierManagementE2ETest.java`: `wait.until(ExpectedConditions.not(ExpectedConditions.urlContains("/login")))`. |
| **Windows PowerShell `curl` Parameter Stalling** | In Windows PowerShell, `curl` is an alias to `Invoke-WebRequest`, which exhibits stalling behavior when non-interactive subshells invoke unparsed parameters. | `Get-Alias curl` returns `Invoke-WebRequest` | Used native `curl.exe` with explicit `--max-time 10` or executed standard probes via Python `urllib.request`. |
| **Puppet Target Node Module Compilation Error** | Puppet agent requires explicit modulepath flags when running manifests outside standard system paths. | `puppet apply -e "include supplier_portal"` returned `Could not find class ::supplier_portal` | Supplied explicit module path: `puppet apply --modulepath=/infrastructure/puppet/modules -e "include supplier_portal"`. |
| **PostgreSQL Container Initialization Race** | Web container started before PostgreSQL finished its initial cluster creation. | `django.db.utils.OperationalError: could not connect to server` | Configured Docker Compose healthcheck on database: `pg_isready -U postgres`, and declared `depends_on: db: condition: service_healthy`. |

---

## 3. Known System Limitations

1. **Single-Node Infrastructure Scope**:  
   The current environment executes all containers (portal, database, Jenkins, and IaC target node) on a single physical host node. While ideal for academic evaluation, CI verification, and local demonstration, high-availability multi-region cluster failover is not included.
2. **Synchronous Email Notifications**:  
   Email alerts for supplier audit approvals utilize Django's console email backend (`django.core.mail.backends.console.EmailBackend`) rather than a live external SMTP relay (e.g., AWS SES or SendGrid).
3. **In-Memory Session Storage**:  
   User sessions and transient state reside in the PostgreSQL `django_session` table. A distributed caching layer (e.g., Redis cluster) has not been implemented for session scaling.
4. **Binary Dependency on Host Chrome**:  
   Local Maven Selenium test execution requires a compatible Chrome/Chromium browser installation on the operating system. Containerized CI execution mitigates this by baking Chromium directly into `jenkins_ci_server`.

---

## 4. Future Enhancements & Production Roadmap

1. **Kubernetes Orchestration & Helm Packaging**:  
   Transition Docker Compose definitions into Kubernetes manifests:
   - Deployments with Horizontal Pod Autoscaling (HPA) based on CPU/memory utilization.
   - StatefulSets for PostgreSQL with persistent volume claims (PVC).
   - Ingress controllers with automated TLS certificates via cert-manager.
2. **Asynchronous Task Queue (Celery + Redis)**:  
   Offload PDF audit report generation, compliance score recalculations, and bulk CSV supplier exports to background asynchronous Celery workers.
3. **Enterprise Identity Federation (SSO / OAuth2 / SAML)**:  
   Integrate Okta, Azure Active Directory, and Keycloak identity providers for corporate Single Sign-On, replacing local Django credentials.
4. **Prometheus & Grafana Observability**:  
   Expose `/metrics` endpoint using `django-prometheus` to capture request latencies, HTTP error rates, and PostgreSQL query execution times, visualized through pre-configured Grafana dashboards.
5. **Multi-Tenant Supplier Isolation**:  
   Implement schema-based multi-tenancy (`django-tenants`) allowing multiple manufacturing divisions or external supply chain partners to maintain isolated audit records within a unified portal instance.
