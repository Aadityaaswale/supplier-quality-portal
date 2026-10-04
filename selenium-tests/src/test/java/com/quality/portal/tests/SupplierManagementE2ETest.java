package com.quality.portal.tests;

import com.quality.portal.pages.DashboardPage;
import com.quality.portal.pages.LoginPage;
import com.quality.portal.pages.SupplierPage;
import org.testng.Assert;
import org.testng.annotations.Test;

public class SupplierManagementE2ETest extends BaseTest {

    @Test(description = "Verify supplier search, profile view, and new supplier onboarding")
    public void testSupplierSearchAndOnboardingJourney() {
        LoginPage loginPage = new LoginPage(driver);
        loginPage.login("manager", "Manager@12345");

        driver.get(baseUrl + "/suppliers/");
        SupplierPage supplierPage = new SupplierPage(driver);

        // 1. Search for existing supplier 'Apex Components'
        supplierPage.searchSupplier("Apex");
        Assert.assertTrue(supplierPage.isSupplierListed("Apex Components"), "Apex Components should appear in search results.");

        // 2. Open supplier profile
        supplierPage.openSupplierProfile("Apex Components");
        Assert.assertTrue(driver.getCurrentUrl().contains("/suppliers/"), "Should navigate to supplier 360 degree profile.");

        // 3. Onboard a new supplier
        driver.get(baseUrl + "/suppliers/");
        String uniqueId = "SUP-" + System.currentTimeMillis();
        String uniqueCode = "TITAN-" + (int)(Math.random() * 900 + 100);
        supplierPage.createSupplier(
            uniqueId,
            uniqueCode,
            "Titan Dynamics Corp",
            "Mark Vance",
            "mark@titandynamics.local",
            "+1-555-7890"
        );

        new org.openqa.selenium.support.ui.WebDriverWait(driver, java.time.Duration.ofSeconds(10))
            .until(org.openqa.selenium.support.ui.ExpectedConditions.urlMatches(".*/suppliers/\\d+/.*"));

        // Verify newly created supplier profile loaded
        Assert.assertTrue(driver.getPageSource().contains("Titan Dynamics Corp"), "New supplier name should appear on detail page.");
    }
}
