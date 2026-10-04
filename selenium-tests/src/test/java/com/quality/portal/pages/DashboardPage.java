package com.quality.portal.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class DashboardPage extends BasePage {
    private final By dashboardTitle = By.xpath("//h1[contains(text(), 'Executive Quality Dashboard')]");
    private final By totalSuppliersCard = By.xpath("//div[contains(@class, 'kpi-card')]//span[contains(text(), 'Total Suppliers')]");
    private final By statusChartCanvas = By.id("statusDoughnutChart");
    private final By navSuppliers = By.id("nav-suppliers");
    private final By navReviews = By.id("nav-reviews");

    public DashboardPage(WebDriver driver) {
        super(driver);
    }

    public boolean isDashboardLoaded() {
        return isElementPresent(dashboardTitle) && isElementPresent(totalSuppliersCard);
    }

    public void navigateToSuppliers() {
        click(navSuppliers);
    }

    public void navigateToReviews() {
        click(navReviews);
    }
}
