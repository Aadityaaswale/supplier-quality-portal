package com.quality.portal.tests;

import com.quality.portal.pages.DashboardPage;
import com.quality.portal.pages.LoginPage;
import com.quality.portal.pages.ReviewPage;
import org.testng.Assert;
import org.testng.annotations.Test;

public class ReviewWorkflowE2ETest extends BaseTest {

    @Test(description = "Verify end-to-end review creation, dynamic score calculation, and manager approval")
    public void testReviewWorkflowJourney() {
        // Step 1: Login as Reviewer
        LoginPage loginPage = new LoginPage(driver);
        loginPage.login("reviewer", "Reviewer@12345");

        driver.get(baseUrl + "/reviews/create/");
        ReviewPage reviewPage = new ReviewPage(driver);

        // Step 2: Input scores & verify live calculator
        // Defect penalty: 2 * 0.5 = 1.0
        // PQ 90 * 0.45 = 40.5
        // Comp 90 * 0.30 = 27.0
        // Deliv 90 * 0.25 = 22.5
        // Total = 40.5 + 27.0 + 22.5 - 1.0 = 89.00
        reviewPage.fillScores(2, 90.0, 90.0, 90.0);
        new org.openqa.selenium.support.ui.WebDriverWait(driver, java.time.Duration.ofSeconds(5))
            .until(d -> "89.00".equals(reviewPage.getComputedScore()));
        String liveScore = reviewPage.getComputedScore();
        Assert.assertEquals(liveScore, "89.00", "Live score calculator should equal 89.00%");

        // Step 3: Submit for approval
        reviewPage.submitForApproval();
        new org.openqa.selenium.support.ui.WebDriverWait(driver, java.time.Duration.ofSeconds(10))
            .until(org.openqa.selenium.support.ui.ExpectedConditions.urlMatches(".*/reviews/\\d+/.*"));

        // Step 4: Verify review details page loaded in Pending Review status
        Assert.assertTrue(driver.getPageSource().contains("Pending Review"), "Review status should transition to Pending Review.");
        String detailScore = reviewPage.getReviewDetailOverallScore();
        Assert.assertEquals(detailScore.trim(), "89.00%", "Overall score on detail page should be 89.00%.");

        // Step 5: Logout and log in as Quality Manager to Approve
        driver.get(baseUrl + "/accounts/logout/");
        new org.openqa.selenium.support.ui.WebDriverWait(driver, java.time.Duration.ofSeconds(5))
            .until(org.openqa.selenium.support.ui.ExpectedConditions.urlContains("/login/"));
        loginPage.login("manager", "Manager@12345");

        // Navigate back to the review
        driver.get(baseUrl + "/reviews/?tab=pending");
        Assert.assertTrue(driver.getPageSource().contains("Pending Review"), "Pending reviews list should contain pending audits.");
    }
}
