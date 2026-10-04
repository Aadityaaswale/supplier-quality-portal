package com.quality.portal.tests;

import com.quality.portal.utils.DriverManager;
import org.openqa.selenium.WebDriver;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;

public abstract class BaseTest {
    protected WebDriver driver;
    protected String baseUrl;

    @BeforeMethod
    public void setUp() {
        this.baseUrl = System.getProperty("baseUrl", System.getenv("PORTAL_URL") != null ? System.getenv("PORTAL_URL") : "http://127.0.0.1");
        DriverManager.initDriver();
        this.driver = DriverManager.getDriver();
        this.driver.get(baseUrl + "/accounts/login/");
    }

    @AfterMethod
    public void tearDown() {
        DriverManager.quitDriver();
    }
}
