import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

class HeyGenDriver():
    def __init__(self):
        self.service = Service()
        self.driver = webdriver.Chrome(service=self.service)

    def chat(self, msg):
        self.chatarea = self.driver.find_elements(By.TAG_NAME, 'textarea')[0]
        self.chatarea.send_keys(msg)
        self.chatarea.send_keys(Keys.ENTER)

    
def heygenmgr(summary_q):
    heygen = HeyGenDriver()
    while True:
        while not summary_q.empty():
            question = summary_q.get()
            print(f"HEYGEN: {question}")
            heygen.chat(question)
        time.sleep(1)
