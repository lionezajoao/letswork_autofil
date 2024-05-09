import os
import time
import pyautogui
from workadays import workdays
from dotenv import load_dotenv
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
load_dotenv()

class Browser:
    def __init__(self, start_date, end_date, start_time, end_time,project_name,today_flag=False):
        self.base_url = "https://app.letswork.com.br"
        self.username = os.environ.get("USERNAME")
        self.password = os.environ.get("PASSWORD")
        self.start_date = datetime.strptime(start_date, "%d-%m-%Y").strftime("%d/%m/%Y") if start_date else None
        self.end_date = datetime.strptime(end_date, "%d-%m-%Y").strftime("%d/%m/%Y") if end_date else None
        self.today_flag = today_flag
        self.start_time= start_time if start_time else os.environ.get("START_TIME")
        self.end_time= end_time if end_time else os.environ.get("END_TIME")
        self.project_name= project_name if project_name else os.environ.get("PROJECT_NAME")
        self.days_list = self.list_days()

    def setup(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])


        self.driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get(self.base_url)

    def wait_elem(self, elem):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, elem)))

    def login(self):
        time.sleep(2)
        # self.wait_elem('//input[@name="login"]')
        self.driver.find_element(By.NAME, "login").send_keys(self.username)
        self.driver.find_element(By.NAME, "senha").send_keys(self.password)
        self.driver.find_element(By.ID, "submit").click()

    def list_days(self):
        if self.today_flag:
            return [datetime.now().strftime("%d/%m/%Y")]
        days = []
        current_date = datetime.strptime(self.start_date, "%d/%m/%Y")
        while current_date <= datetime.strptime(self.end_date, "%d/%m/%Y"):
            if workdays.is_workday(current_date) and not workdays.is_holiday(current_date, country="BR"):
                days.append(current_date.strftime("%d/%m/%Y"))
            current_date += timedelta(days=1)
        return days
        

    def fill_missing_days(self, date):
        time.sleep(2)
        self.driver.get(f"{self.base_url}/timesheet/index")
        time.sleep(2)

        # add day
        pyautogui.click(x=342, y=402)

        pyautogui.click(x=992, y=526)

        time.sleep(1)

        # start date
        pyautogui.click(x=807, y=318)
        pyautogui.write(date)

        # start date hour
        pyautogui.click(x=1066, y=317)
        pyautogui.write(self.start_time)

        # end date
        pyautogui.click(x=814, y=366)
        pyautogui.write(date)

        # end date hour
        pyautogui.click(x=1064, y=367)
        pyautogui.write(self.end_time)

        # project
        pyautogui.click(x=1000, y=422)
        pyautogui.write(self.project_name)
        pyautogui.press("enter")

        # task        
        pyautogui.click(x=1248, y=501)

    def close(self):
        self.driver.close()