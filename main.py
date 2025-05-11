from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.ie.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import random

def consume_compare(current_city,expect_city,year_of_working,edu_experience,
                    institutional_requirement,current_industry,current_title,
                    age,liveness,sex,hopping_freq):
    s = Service("chrome/chromedriver-win64/chromedriver.exe")
    chrome_options = Options()
    chrome_options.binary_location = "chrome/chrome-win64/chrome.exe"
    driver = webdriver.Chrome(service=s, options=chrome_options)

    driver.maximize_window()
    driver.get("https://h.liepin.com/im/showmsgnewpage?tab=message")
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

        current_city_tag = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//label[@class='tag-item' and text()='{current_city}']"))
        )
        current_city_tag.click()

        expect_city_tag = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f'//*[@id="main-container"]/div[1]/div/div[2]/div/div/div[1]/form/section/div/'
                                                  f'div[1]/div[2]/div/div[1]/label[@class="tag-item" and text()="{expect_city}"]'))
        )
        expect_city_tag.click()

        year_of_working_tag = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, f'//*[@id="main-container"]/div[1]/div/div[2]/div/div/div[1]/form/section/div/div[1]'
                           f'/div[3]/div/div/div[1]label[@class="tag-item" and text()="{year_of_working}"]'))
        )
        year_of_working_tag.click()
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
                random_wait = random.uniform(8, 10)
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
                    # 简历编号
                    try:
                        driver.implicitly_wait(5)
                        index_of_people = driver.find_element(by=By.XPATH,
                                                              value='/html/body/div[1]/div[1]/div/div/div/div/section[1]/div[1]/div/div[1]/div[3]/div/span[1]')
                        print(index_of_people.text)
                    except NoSuchElementException:
                        print("未找到简历编号")
                    print("\n")

                    # 最后登陆时间
                    try:
                        last_login_time = driver.find_element(by=By.XPATH,
                                                              value='//*[@id="resume-detail-single"]/div[1]/div/div[1]/div[3]/div/span[2]')
                        print(last_login_time.text)
                    except NoSuchElementException:
                        print("未找到最后一次登陆时间")
                    print("\n")

                    # 状态
                    try:
                        status = driver.find_element(by=By.XPATH,
                                                     value='//*[@id="resume-detail-basic-info"]/div[3]/div[1]/span')
                        print("状态：", end="")
                        print(status.text)
                    except NoSuchElementException:
                        print("未找到状态")
                    print("\n")

                    # 个人信息
                    try:
                        personal_message_1 = driver.find_element(by=By.XPATH,
                                                                 value='//*[@id="resume-detail-basic-info"]/div[3]/div[2]')
                        personal_message_2 = driver.find_element(by=By.XPATH,
                                                                 value='//*[@id="resume-detail-basic-info"]/div[3]/div[3]')
                        print("个人信息：")
                        print(f"{personal_message_1.text}\n{personal_message_2.text}")
                    except NoSuchElementException:
                        print("未找到个人信息")
                    print("\n")

                    # 求职意向
                    try:
                        job_intention_1 = driver.find_element(by=By.XPATH,
                                                              value='//*[@id="resume-detail-job-exp-info"]/div[1]/div[1]/span[1]')
                        job_intention_2 = driver.find_element(by=By.XPATH,
                                                              value='//*[@id="resume-detail-job-exp-info"]/div[1]/div[1]/span[2]')
                        job_intention_3 = driver.find_element(by=By.XPATH,
                                                              value='//*[@id="resume-detail-job-exp-info"]/div[1]/div[1]/span[3]')
                        print(f"求职意向：{job_intention_1.text}丨{job_intention_2.text}丨{job_intention_3.text}")
                    except NoSuchElementException:
                        print("")
                    print("\n")

                    # 教育经历
                    try:
                        edu_experiences = driver.find_elements(by=By.CLASS_NAME, value='edu-school-cont')
                        print("教育经历：")
                        for items in edu_experiences:
                            item = items.find_elements(by=By.TAG_NAME, value='span')
                            for edu_experience in item:
                                print(edu_experience.text, end=' ')
                            print("\n")
                    except NoSuchElementException:
                        print("未找到教育经历")
                    print("\n")

                    # 资格证书
                    try:
                        certificates = driver.find_elements(by=By.CLASS_NAME, value='credential-tag')
                        print("资格证书：")
                        for certificate in certificates:
                            print(certificate.text, end=" ")
                    except NoSuchElementException:
                        print("未找到资格证书")
                    print("\n")

                    # 语言能力
                    try:
                        language_abilitys = driver.find_elements(by=By.CLASS_NAME, value='rd-lang-item')
                        print("语言能力：")
                        for language in language_abilitys:
                            lang_type = language.find_element(by=By.CLASS_NAME, value='lang-name')
                            print(lang_type.text, end=" ")
                            lang_levels = language.find_elements(by=By.CLASS_NAME, value="lang-level")
                            for lang_level in lang_levels:
                                print(lang_level.text, end=" ")
                            print("\n")
                    except NoSuchElementException:
                        print("未找到语言能力")
                    print("\n")

                    # 技能
                    try:
                        abilities = driver.find_elements(by=By.CLASS_NAME, value='skill-tag')
                        print("技能：")
                        for ability in abilities:
                            print(ability.text, end=" ")
                    except NoSuchElementException:
                        print("未找到技能")
                    print("\n")

                    # 自我评价
                    try:
                        self_assessment = driver.find_element(by=By.XPATH,
                                                              value='//*[@id="resume-detail-self-eva-info"]/div/div')
                        print("自我评价：")
                        print(self_assessment.text)
                    except NoSuchElementException:
                        print("未找到自我评价")
                    print("\n")

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

consume_compare("上海","北京","1-3年","","","","","","","","")