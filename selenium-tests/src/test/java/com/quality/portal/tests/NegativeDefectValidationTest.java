package com.quality.portal.tests;

import com.quality.portal.pages.LoginPage;
import org.testng.Assert;
import org.testng.annotations.Test;

public class NegativeDefectValidationTest extends BaseTest {

    @Test(description = "Demonstration test for Jenkins Continuous Testing quality gate failure")
    public void testDeliberateDefectInjection() {
        LoginPage loginPage = new LoginPage(driver);

        // Check if deliberate defect mode is toggled via system property
        String defectFlag = System.getProperty("injectDefect", "false");
        if ("true".equalsIgnoreCase(defectFlag)) {
            // Deliberate defect: assert that a non-existent element exists, forcing failure & screenshot
            System.out.println(">>> [DEFECT MODE ACTIVE] Injecting deliberate assertion defect for Jenkins quality gate demonstration...");
            Assert.fail("Deliberate Quality Gate Failure: Injected defect detected in Supplier Portal build verification!");
        } else {
            // Normal pass path
            Assert.assertTrue(loginPage.isLoginPageLoaded(), "Login page loaded cleanly in verified baseline.");
        }
    }
}
