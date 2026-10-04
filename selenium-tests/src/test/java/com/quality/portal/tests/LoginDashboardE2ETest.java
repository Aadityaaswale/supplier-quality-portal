package com.quality.portal.tests;

import com.quality.portal.pages.DashboardPage;
import com.quality.portal.pages.LoginPage;
import org.testng.Assert;
import org.testng.annotations.Test;

public class LoginDashboardE2ETest extends BaseTest {

    @Test(description = "Verify user can log into the portal and view Executive Dashboard KPIs")
    public void testLoginAndDashboardJourney() {
        LoginPage loginPage = new LoginPage(driver);
        Assert.assertTrue(loginPage.isLoginPageLoaded(), "Login page should be properly loaded.");

        // Authenticate as Admin
        loginPage.login("admin", "Admin@12345");

        // Verify Dashboard
        DashboardPage dashboardPage = new DashboardPage(driver);
        Assert.assertTrue(dashboardPage.isDashboardLoaded(), "Dashboard KPI cards should be visible upon login.");
    }
}
