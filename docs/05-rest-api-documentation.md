# 05 - REST API Architecture & OpenAPI Specifications

**Project Title**: Puppet-Provisioned Supplier Quality Review Portal  
**Author**: Aaditya Aswale (Student ID: 23102B0044)  
**API Specification Standard**: OpenAPI 3.0 / RESTful JSON  
**Base URL**: `http://127.0.0.1:8000/api/v1/`  
**Authentication**: Session Authentication (`csrftoken` / `sessionid`) & HTTP Basic Auth  

---

## 1. API Endpoint Inventory

| HTTP Method | Endpoint URI | Description | Minimum Role |
|---|---|---|---|
| `GET` | `/health/` | Public system health & DB liveness probe | Anonymous |
| `GET` | `/api/v1/suppliers/` | List all suppliers (supports search/filter) | Any Authenticated |
| `POST` | `/api/v1/suppliers/` | Register new supplier | `ADMIN` |
| `GET` | `/api/v1/suppliers/{id}/` | Retrieve full supplier dossier & history | Any Authenticated |
| `PUT` / `PATCH` | `/api/v1/suppliers/{id}/` | Update supplier master metadata | `ADMIN` |
| `DELETE` | `/api/v1/suppliers/{id}/` | Soft/Hard delete supplier entity | `ADMIN` |
| `GET` | `/api/v1/reviews/` | List quality reviews (tab & status filters)| Any Authenticated |
| `POST` | `/api/v1/reviews/` | Submit new quality review audit | `REVIEWER` / `ADMIN` |
| `GET` | `/api/v1/reviews/{id}/` | Retrieve audit details & scoring breakdown | Any Authenticated |
| `POST` | `/api/v1/reviews/{id}/transition/` | Execute state transition (`submit`/`approve`/`reject`)| `QUALITY_MANAGER` / `ADMIN` |
| `GET` | `/api/v1/dashboard/metrics/` | Aggregated executive KPIs and chart series | Any Authenticated |

---

## 2. Detailed Endpoint Specifications

### 2.1 Public Health Probe
* **Endpoint**: `GET /health/`
* **Response (HTTP 200 OK)**:
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2026-10-04T09:30:00.123456Z",
  "system": "Supplier Quality Review Portal",
  "author": "AADITYA ASWALE (23102B0044)"
}
```

---

### 2.2 Supplier Collection: `GET /api/v1/suppliers/`
* **Query Parameters**:
  - `q`: Search substring across `name`, `code`, or `country`.
  - `status`: Filter by `Active`, `Suspended`, `Under Review`.
* **Sample Response (HTTP 200 OK)**:
```json
[
  {
    "id": 1,
    "supplier_id": "SUP-1001",
    "code": "APEX-IND",
    "name": "Apex Components Inc.",
    "contact_name": "Rajesh Sharma",
    "contact_email": "r.sharma@apexcomponents.com",
    "phone": "+91-98200-11223",
    "address": "Plot 42, Electronic City Phase 1",
    "country": "India",
    "status": "Active",
    "overall_quality_score": "95.54",
    "grade": "A+",
    "reviews_count": 3
  }
]
```

---

### 2.3 Quality Review Creation: `POST /api/v1/reviews/`
* **Request Payload**:
```json
{
  "supplier": 1,
  "review_date": "2026-10-04",
  "defect_count": 2,
  "product_quality_score": 90.0,
  "compliance_score": 90.0,
  "delivery_score": 90.0,
  "comments": "Batch 4022 passed tensile stress tests with 2 minor cosmetic surface scratches."
}
```
* **Score Calculation Executed by Server**:
  $$\text{Score} = (90.0 \times 0.45) + (90.0 \times 0.30) + (90.0 \times 0.25) - (2 \times 0.5) = 40.5 + 27.0 + 22.5 - 1.0 = 89.00$$
* **Sample Response (HTTP 201 Created)**:
```json
{
  "id": 9,
  "review_id": "QR-APEX-IND-261004145726",
  "supplier": 1,
  "supplier_name": "Apex Components Inc.",
  "reviewer": 3,
  "reviewer_name": "reviewer",
  "review_date": "2026-10-04",
  "defect_count": 2,
  "product_quality_score": "90.00",
  "compliance_score": "90.00",
  "delivery_score": "90.00",
  "overall_score": "89.00",
  "status": "Pending Review",
  "comments": "Batch 4022 passed tensile stress tests with 2 minor cosmetic surface scratches.",
  "manager_remarks": null
}
```

---

### 2.4 Review Workflow Transition: `POST /api/v1/reviews/{id}/transition/`
* **Authorization**: Must belong to `QUALITY_MANAGER` or `ADMIN`.
* **Request Payload**:
```json
{
  "action": "approve",
  "remarks": "Formally certified under ISO 9001 compliance standards. Batch approved for production assembly."
}
```
* **Response (HTTP 200 OK)**:
```json
{
  "message": "Review QR-APEX-IND-261004145726 successfully updated to 'Approved'.",
  "review_id": "QR-APEX-IND-261004145726",
  "new_status": "Approved",
  "supplier_new_cumulative_score": "95.54",
  "supplier_grade": "A+"
}
```

---

## 3. Real cURL Command Verification

```bash
# 1. Probe System Health
curl -s http://127.0.0.1:8000/health/

# 2. Retrieve Authenticated Supplier List
curl -s -u admin:Admin@12345 http://127.0.0.1:8000/api/v1/suppliers/

# 3. Retrieve Executive Metrics
curl -s -u manager:Manager@12345 http://127.0.0.1:8000/api/v1/dashboard/metrics/
```
