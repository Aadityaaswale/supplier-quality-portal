@echo off
REM ==============================================================================
REM Run Maven Selenium Test Suite
REM Student: AADITYA ASWALE (23102B0044)
REM ==============================================================================

cd /d "%~dp0..\selenium-tests"
echo Running Selenium Tests via Apache Maven...
mvn clean test -Dheadless=true
pause
