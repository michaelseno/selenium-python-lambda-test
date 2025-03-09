import os
import json
import time
import boto3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.portfolio_page import PortfolioPage

# CloudWatch Logs client
logs_client = boto3.client("logs")


def lambda_handler():
    # Configure Headless Chrome
    chrome_options = Options()
    chrome_options.binary_location = "/opt/chrome"
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Start WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Use Page Object Model (POM)
        portfolio_page = PortfolioPage(driver)
        portfolio_page.navigate_to_landing_page()

        time.sleep(2)
        log_to_cloudwatch(f"Test Passed - {portfolio_page.navigate_to_landing_page().__name__}")

        driver.quit()
        return {"statusCode": 200, "body": json.dumps({"message": "Test successful"})}

    except Exception as e:
        error_message = f"Test Failed: {str(e)}"
        log_to_cloudwatch(error_message)
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}


def log_to_cloudwatch(message):
    logs_client.put_log_events(
        logGroupName="SeleniumLambdaLogs",
        logStreamName="TestLogs",
        logEvents=[{"timestamp": int(time.time() * 1000), "message": message}]
    )
