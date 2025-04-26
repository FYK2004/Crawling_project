import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.ie.service import Service

s=Service("chrome/chromedriver-win64/chromedriver.exe")
chrome_options=Options()
chrome_options.binary_location="chrome/chrome-win64/chrome.exe"
driver=webdriver.Chrome(service=s,options=chrome_options)

driver.get("https://www.liepin.com/zhaopin/?inputFrom=head_navigation&scene=init&workYearCode=1&ckId=q8gfbiydbq6bn3i1vcl5elnmhwcr84n8")
#print(driver.title)
elements=driver.find_elements(By.)

time.sleep(10)
#driver.close()