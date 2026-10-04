# 21 - User Manual & Enterprise Operations Guide

**Project Title**: Puppet-Provisioned Supplier Quality Review Portal  
**Author**: Aaditya Aswale (Student ID: 23102B0044)  
**Target Audience**: Quality Inspectors, Quality Managers, System Administrators  
**Portal URL**: `http://127.0.0.1:8000/`  

---

## 1. Demo Credentials & Quick Role Access

| Role | Username | Password | Operational Scope |
|---|---|---|---|
| **System Administrator** | `admin` | `Admin@12345` | Full administrative control, user RBAC, supplier CRUD |
| **Quality Manager** | `manager` | `Manager@12345` | Certifying authority: reviews audits, approves/rejects |
| **Quality Reviewer** | `reviewer` | `Reviewer@12345` | Factory floor inspector: inputs audits, records defects |

> **Pro Tip**: The Sign-In screen at `/accounts/login/` features one-click "Quick Demo Credentials" buttons for instant role switching during presentations.

---

## 2. Navigating the Portal

```mermaid
graph LR
    Login[/accounts/login/] --> Dashboard[Executive Dashboard /]
    Dashboard --> Suppliers[/suppliers/ Directory]
    Dashboard --> Reviews[/reviews/ Quality Audits]
    Dashboard --> Reports[/reports/ Analytics & CSV]
    Dashboard --> AdminPanel[/accounts/users/ User RBAC]
    
    Suppliers --> SupplierDetail[/suppliers/:id/ 360 View]
    Reviews --> CreateReview[/reviews/create/ Audit Entry]
    Reviews --> ReviewDetail[/reviews/:id/ Evaluation & Approval]
```

### 2.1 Executive Dashboard (`/`)
- **KPI Summary Cards**: Real-time counts of Total Registered Suppliers, Pending Manager Reviews, Average Global Quality Score, and Active Inspections.
- **Interactive Visualizations (Chart.js)**:
  1. *Overall Supplier Score Distribution*: Dynamic bar chart ranking suppliers.
  2. *Defect Distribution Trend*: Horizontal bar chart highlighting defect hotspots.
  3. *Audit Status Breakdown*: Doughnut chart illustrating `Draft`, `Pending`, `Approved`, and `Rejected` proportions.
  4. *Grade Allocation Doughnut*: Tier ratings (`A+`, `A`, `B`, `C`, `D`).

### 2.2 Conducting a Quality Audit Review (`/reviews/create/`)
1. Select the manufacturing supplier from the dropdown.
2. The Audit Evaluation Date automatically defaults to the current day.
3. Enter the **Defective Units Count** (e.g. `2`).
4. Enter scores for **Product Quality (45%)**, **Compliance (30%)**, and **Delivery (25%)**.
5. Observe the **Live Score Calculator Card**:
   - The card dynamically recalculates the exact weighted percentage and letter grade as values are entered.
6. Click **Submit for Approval** to submit directly for manager review, or **Save Draft** to edit later.

### 2.3 Approving an Audit (Quality Manager Journey)
1. Log in as `manager` / `Manager@12345`.
2. Navigate to **Quality Reviews** and select the **Pending Review** tab.
3. Click on the target review to open the detailed breakdown.
4. Review inspector comments, score breakdowns, and defect counts.
5. Click the green **Approve** button.
6. In the modal, provide formal certification remarks (e.g. *"Certified compliant with AS9100 standards"*).
7. Click **Certify & Approve**.
8. The portal immediately updates the review to `Approved`, appends the transition to the immutable **Audit Trail**, and updates the supplier's institutional rating and grade.
