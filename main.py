from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.ie.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
# import pygetwindow as gw

import time
import random


s = Service("chrome/chromedriver-win64/chromedriver.exe")
chrome_options = Options()
chrome_options.binary_location = "chrome/chrome-win64/chrome.exe"
driver = webdriver.Chrome(service=s,options = chrome_options)

driver.get("https://h.liepin.com/im/showmsgnewpage?tab=message")
# https://m.anjuke.com/jn/sale/   安居客

#    18116195410
#    6913016fdu
time.sleep(30)

try:
    # 显式等待元素可点击
    wait = WebDriverWait(driver, 10)
    # 通过XPath定位（推荐：结合父元素的data-bar属性）
    people_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//li[@data-bar='manager-search']/a")
    ))
    # 点击链接
    people_link.click()

    wait.until(EC.url_to_be("https://h.liepin.com/search/getConditionItem"))

    shanghai_tag = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//label[@class='tag-item' and text()='上海']"))
    )
    shanghai_tag.click()
    try:
        # 使用通用定位策略（匹配所有包含 cid 标识的<tr>）
        all_trs = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((
                By.XPATH,
                '//tr[contains(@data-tlg-scm, "cid")]'
            ))
        )
    except TimeoutException:
        print("未找到符合条件的<tr>元素")
        driver.quit()
        exit()

    # 步骤2：循环点击每个<tr>
    for index, tr in enumerate(all_trs):
        try:
            random_wait =  random.uniform(8,10)
            # 记录当前窗口句柄
            main_window = driver.current_window_handle

            # 显式等待元素可点击
            clickable_tr = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable(tr)
            )

            # 执行点击操作
            clickable_tr.click()
            print(f"已点击第 {index + 1} 个<tr>")

            # 处理新窗口/标签页（假设每次点击都打开新标签页）
            if len(driver.window_handles) > 1:
                driver.switch_to.window(driver.window_handles[-1])
                # 在此处添加对新页面的操作（例如截图、数据抓取等）
                time.sleep(random_wait)  # 等待新页面加载
                driver.close()  # 关闭新标签页
                driver.switch_to.window(main_window)  # 切回主窗口

            # 防止快速点击导致页面未完全加载
            time.sleep(random_wait)

        except (TimeoutException, NoSuchElementException) as e:
            print(f"第 {index + 1} 个<tr>点击失败: {str(e)}")
            continue

    time.sleep(5)
finally:
    # 保持浏览器打开（根据需求决定是否关闭）
    # driver.quit()
    pass
#爬取数据
# elements = driver.find_elements(By.CLASS_NAME,"item-wrap")
# for index,element in enumerate(elements):
#     title = element.find_element(By.CLASS_NAME,"jsx-479584096 ")
#     print(f"第{index+1}个条目的标题是：{title.text}")
#     price = element.find_element(By.CLASS_NAME,"content-price")
#     print(f"第{index+1}个条目的价格是：{price.text}")
#     desc = element.find_element(By.CLASS_NAME, "desc-wrap-community")
#     print(f"第{index + 1}个条目的标签是：{desc.text}")

# #link_element = element.find_element(By.TAG_NAME,"a")
# #href = link_element.get_attribute("href")
# #print(f"第{index+1}个条目的跳转链接是：{href}")
#
#     link_element = element.find_element(By.XPATH,".//a")
#     href = link_element.get_attribute("href")
#     print(f"第{index+1}个条目的跳转链接是：{href}")


#模拟滑动翻页
# driver.execute_script("return document.body.scrollHeight")
# last_height = driver.execute_script("return document.body.scrollHeight")
# while True:
#     driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
#     time.sleep(3)
#     new_height = driver.execute_script("return document.body.scrollHeight")
#     if new_height == last_height:
#         print("翻页失败")
#         break
#     last_height = new_height

#处理点击验证 与 点击翻页
# for i in range(100):
#     body_text = driver.find_element(By.TAG_NAME,"body").text
#     if'验证码校验' in body_text:
#         input_element = driver.find_element(By.ID,"btnSubmit")
#         time.sleep(1)
#         actions = ActionChains(driver)
#         actions.move_to_element(input_element).perform()
#         time.sleep(random.uniform(0.5,1.5))
#         actions.click().perform()
#         time.sleep(random.uniform(3,6))
#     driver.find_element(By.CLASS_NAME,"next-active").click()
#     time.sleep(3)

# print(driver.title)
# driver.close()
