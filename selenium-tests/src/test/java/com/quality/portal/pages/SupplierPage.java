package com.quality.portal.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class SupplierPage extends BasePage {
    private final By searchInput = By.id("input-search-supplier");
    private final By filterButton = By.id("btn-filter-supplier");
    private final By suppliersTable = By.id("suppliers-table");
    private final By addSupplierBtn = By.id("btn-add-supplier");

    // Form inputs
    private final By supplierIdInput = By.id("supplier_id");
    private final By codeInput = By.id("code");
    private final By nameInput = By.id("name");
    private final By contactPersonInput = By.id("contact_person");
    private final By emailInput = By.id("email");
    private final By phoneInput = By.id("phone");
    private final By saveSupplierBtn = By.id("btn-save-supplier");

    public SupplierPage(WebDriver driver) {
        super(driver);
    }

    public void searchSupplier(String keyword) {
        driver.get(driver.getCurrentUrl().split("\\?")[0] + "?q=" + keyword);
    }

    public boolean isSupplierListed(String supplierName) {
        By rowLocator = By.xpath("//table[@id='suppliers-table']//a[contains(text(), '" + supplierName + "')]");
        return waitForVisibility(rowLocator).isDisplayed();
    }

    public void openSupplierProfile(String supplierName) {
        By rowLocator = By.xpath("//table[@id='suppliers-table']//a[contains(text(), '" + supplierName + "')]");
        org.openqa.selenium.WebElement link = waitForClickable(rowLocator);
        if (driver instanceof org.openqa.selenium.JavascriptExecutor) {
            ((org.openqa.selenium.JavascriptExecutor) driver).executeScript("arguments[0].click();", link);
        } else {
            link.click();
        }
    }

    public void createSupplier(String id, String code, String name, String contact, String email, String phone) {
        click(addSupplierBtn);
        type(supplierIdInput, id);
        type(codeInput, code);
        type(nameInput, name);
        type(contactPersonInput, contact);
        type(emailInput, email);
        type(phoneInput, phone);
        click(saveSupplierBtn);
    }
}
