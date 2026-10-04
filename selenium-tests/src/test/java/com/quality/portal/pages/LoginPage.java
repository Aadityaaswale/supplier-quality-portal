package com.quality.portal.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

public class LoginPage extends BasePage {
    private final By usernameInput = By.id("username");
    private final By passwordInput = By.id("password");
    private final By submitButton = By.id("btn-submit-login");

    public LoginPage(WebDriver driver) {
        super(driver);
    }

    public void login(String username, String password) {
        setValue(usernameInput, username);
        setValue(passwordInput, password);
        WebElement btn = waitForClickable(submitButton);
        if (driver instanceof org.openqa.selenium.JavascriptExecutor) {
            ((org.openqa.selenium.JavascriptExecutor) driver).executeScript("arguments[0].click();", btn);
        } else {
            btn.click();
        }
        wait.until(org.openqa.selenium.support.ui.ExpectedConditions.not(
            org.openqa.selenium.support.ui.ExpectedConditions.urlContains("/login/")
        ));
    }

    public boolean isLoginPageLoaded() {
        return isElementPresent(submitButton);
    }
}
