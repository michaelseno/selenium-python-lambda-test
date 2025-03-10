import os
import json
import time
import boto3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from pages.portfolio_page import PortfolioPage

# CloudWatch Logs client
logs_client = boto3.client("logs")


def lambda_handler(event, context):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1280x1696")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--user-data-dir=/tmp/user-data")
    chrome_options.add_argument("--data-path=/tmp/data-path")
    chrome_options.add_argument("--homedir=/tmp")
    chrome_options.add_argument("--disk-cache-dir=/tmp/cache-dir")

    # Set the binary location explicitly
    chrome_options.binary_location = "/var/task/bin/headless-chromium"
    service = Service("/var/task/bin/chromedriver")

    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
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
