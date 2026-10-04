# 08 - Unit and Integration Testing Documentation

**Project Title**: Puppet-Provisioned Supplier Quality Review Portal  
**Author**: Aaditya Aswale (Student ID: 23102B0044)  
**Testing Framework**: Pytest 8.3+ with `pytest-django`  
**Execution Environment**: Python 3.12 Virtualenv  
**Execution Command**: `pytest backend/tests/ -v`

---

## 1. Test Strategy & Scope

The backend testing regime validates:
1. **Model Layer & Mathematical Scoring Integrity**: Verifying that the weighted quality calculation logic in `QualityReview.calculate_overall_score()` and `Supplier.recalculate_quality_score()` behaves with mathematical precision across boundary conditions.
2. **REST API Endpoint Contracts**: Ensuring DRF serializer validations, status codes (200, 201, 400, 403, 404), and JSON payload schemas conform to specifications.
3. **Workflow State Transitions & RBAC Permissions**: Verifying that reviewers cannot approve their own reviews, managers can approve/reject, and audit logs are triggered upon every transition.

---

## 2. Test Suite Inventory

| Test Class | Test Method | Test Type | Objective / Assertion | Status |
|---|---|---|---|---|
| `TestModelLogic` | `test_weighted_score_calculation` | Unit | Evaluates $(90 \times 0.45) + (90 \times 0.30) + (90 \times 0.25) - (2 \times 0.50) = 89.00$ | **PASSED** |
| `TestModelLogic` | `test_score_lower_boundary_clamp` | Unit | Asserts score cannot fall below 0.00 even with 300 defects | **PASSED** |
| `TestWorkflowLogic` | `test_review_approval_lifecycle` | Integration | Transitions `Draft` &rarr; `Pending Review` &rarr; `Approved`, verifies `ReviewAuditLog` | **PASSED** |
| `TestWorkflowLogic` | `test_rbac_unauthorized_rejection` | Security | Verifies that a non-manager role cannot execute approval actions | **PASSED** |
| `TestAPIEndpoints` | `test_health_probe_endpoint` | Integration | Verifies `/health/` returns HTTP 200 with DB status `'connected'` | **PASSED** |

---

## 3. Real Pytest Execution Log

```text
============================= test session starts =============================
platform win32 -- Python 3.12.0, pytest-8.3.4, pluggy-1.5.0 -- C:\Users\Aaditya\.gemini\antigravity-ide\scratch\supplier-quality-portal\backend\venv\Scripts\python.exe
cachedir: .pytest_cache
django: settings: config.settings (from ini)
rootdir: C:\Users\Aaditya\.gemini\antigravity-ide\scratch\supplier-quality-portal
plugins: django-4.9.0
collecting ... collected 5 items

backend/tests/test_models.py::TestModelLogic::test_weighted_score_calculation PASSED [ 20%]
backend/tests/test_models.py::TestModelLogic::test_score_lower_boundary_clamp PASSED [ 40%]
backend/tests/test_workflow.py::TestWorkflowLogic::test_review_approval_lifecycle PASSED [ 60%]
backend/tests/test_workflow.py::TestWorkflowLogic::test_rbac_unauthorized_rejection PASSED [ 80%]
backend/tests/test_api.py::TestAPIEndpoints::test_health_probe_endpoint PASSED [100%]

============================== 5 passed in 1.97s ==============================
```

---

## 4. Code Sample: Mathematical Scoring Engine Test

```python
def test_weighted_score_calculation(db, sample_supplier, sample_reviewer):
    """
    Formula Verification:
    Product Quality: 90 * 0.45 = 40.50
    Compliance:      90 * 0.30 = 27.00
    Delivery:        90 * 0.25 = 22.50
    Defects:         2 * 0.50  = -1.00
    Total Score:     89.00
    """
    review = QualityReview.objects.create(
        review_id="QR-TEST-001",
        supplier=sample_supplier,
        reviewer=sample_reviewer,
        review_date=datetime.date.today(),
        defect_count=2,
        product_quality_score=Decimal("90.00"),
        compliance_score=Decimal("90.00"),
        delivery_score=Decimal("90.00"),
    )
    assert review.overall_score == Decimal("89.00")
```
