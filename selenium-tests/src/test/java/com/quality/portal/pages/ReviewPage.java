package com.quality.portal.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class ReviewPage extends BasePage {
    private final By addReviewBtn = By.id("btn-add-review");
    private final By defectInput = By.id("id_defect_count");
    private final By productQualityInput = By.id("id_product_quality_score");
    private final By complianceInput = By.id("id_compliance_score");
    private final By deliveryInput = By.id("id_delivery_score");
    private final By commentsInput = By.id("id_comments");
    private final By computedScoreDisplay = By.id("computed_overall_score_val");
    private final By submitDraftBtn = By.id("btn-save-draft");
    private final By submitDirectBtn = By.id("btn-submit-direct");

    // Detail actions
    private final By approveBtn = By.id("btn-approve-review");
    private final By rejectBtn = By.id("btn-reject-review");
    private final By remarksInput = By.id("remarks");
    private final By confirmDecisionBtn = By.id("btn-confirm-decision");
    private final By reviewOverallScoreDisplay = By.id("review_overall_score_val");

    public ReviewPage(WebDriver driver) {
        super(driver);
    }

    public void startNewReview() {
        click(addReviewBtn);
    }

    public void fillScores(int defects, double pq, double comp, double deliv) {
        setValue(defectInput, String.valueOf(defects));
        setValue(productQualityInput, String.format(java.util.Locale.US, "%.1f", pq));
        setValue(complianceInput, String.format(java.util.Locale.US, "%.1f", comp));
        setValue(deliveryInput, String.format(java.util.Locale.US, "%.1f", deliv));
    }

    public String getComputedScore() {
        return getText(computedScoreDisplay);
    }

    public void submitForApproval() {
        if (driver instanceof org.openqa.selenium.JavascriptExecutor) {
            ((org.openqa.selenium.JavascriptExecutor) driver).executeScript(
                "var act = document.getElementById('form_action_input'); if (act) act.value = 'submit_for_review';" +
                "var f = document.querySelector('form'); if (f) f.submit();"
            );
        } else {
            click(submitDirectBtn);
        }
    }

    public void saveDraft() {
        click(submitDraftBtn);
    }

    public void approveReviewWithRemarks(String remarks) {
        click(approveBtn);
        type(remarksInput, remarks);
        click(confirmDecisionBtn);
    }

    public String getReviewDetailOverallScore() {
        return getText(reviewOverallScoreDisplay);
    }
}
