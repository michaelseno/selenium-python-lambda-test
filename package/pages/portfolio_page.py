from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class PortfolioPage(BasePage):
    PORTFOLIO_URL = 'http://aws-personal-portfolio-bucket.s3-website-us-east-1.amazonaws.com'
    HEADER_TEXT = (By.XPATH, "//header[text()='Welcome to My Cloud Portfolio']")
    ABOUT_SECTION = (By.ID, "about")
    SKILLS_SECTION = (By.ID, "skills")
    PROJECTS_SECTION = (By.ID, "projects")
    CONTACT_SECTION = (By.ID, "contact")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def open_portfolio_page(self):
        self.driver.get(*self.PORTFOLIO_URL)

    def navigate_to_landing_page(self):
        self.open_portfolio_page()
        self.wait_for_element(*self.ABOUT_SECTION)
        self.wait_for_element(*self.SKILLS_SECTION)
        self.wait_for_element(*self.PROJECTS_SECTION)
        self.wait_for_element(*self.CONTACT_SECTION)

