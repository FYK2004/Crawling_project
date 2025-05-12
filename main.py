import sys, time, json, random, tempfile, logging, platform
from typing import Final, List, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.ie.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


CONFIG_PATH: Final = "./config/chrome.json"


def setup_logger(debug: bool = False):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG if debug else logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    logger.handlers = []
    logger.addHandler(handler)


def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def init_driver() -> webdriver.Chrome:
    system_platform = platform.system().lower()
    config = load_config()

    if system_platform not in config:
        raise EnvironmentError(f"Platform '{system_platform}' not found in config")

    platform_config = config[system_platform]
    chromedriver_path = platform_config.get("chromedriver_path")
    chrome_binary_path = platform_config.get("chrome_binary_path")

    if not chromedriver_path:
        raise ValueError("chromedriver_path not specified for this platform in config")

    chrome_options = Options()

    if system_platform == "windows":
        if not chrome_binary_path:
            raise ValueError("chrome_binary_path not specified for Windows in config")
        chrome_options.binary_location = chrome_binary_path

    elif system_platform == "linux":
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"--user-data-dir={tempfile.mkdtemp()}")

    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def slide_verification(driver):
    try:
        # 等待 iframe 加载并切换到 iframe
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "tcaptcha_iframe"))
        )
        driver.switch_to.frame("tcaptcha_iframe")

        # 等待滑块元素可见
        slider = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[@id='tcaptcha_drag_thumb']")
            )
        )

        # 创建动作链
        action = ActionChains(driver)

        # 点击并按住滑块
        action.click_and_hold(slider).perform()

        # 模拟滑动过程
        total_distance = 222  # 滑动的总距离
        current_position = 0
        while current_position < total_distance:
            move_distance = min(
                total_distance - current_position, random.uniform(10, 30)
            )
            action.move_by_offset(xoffset=move_distance, yoffset=0).perform()
            current_position += move_distance
            time.sleep(random.uniform(0.02, 0.1))

        # 释放滑块
        action.release().perform()
        print("滑动完成")
    except Exception as e:
        print("滑动验证码失败:", e)


def create_session(
    driver: webdriver.Chrome,
    website: str = "https://h.liepin.com/account/login",
    user: str = "18116195410",
    password: str = "6913016fdu",
) -> None:
    driver.maximize_window()
    driver.get(website)

    # TODO: 自动填入账号密码，滑动滑块验证码
    st = driver.find_element(
        By.XPATH, "//*[@id='main-container']/div/div[3]/div/div/ul/li[2]"
    )
    st.click()
    time.sleep(1)
    st = driver.find_element(
        By.XPATH, "//*[@id='main-container']/div/div[3]/div/div/div/div[1]/div[1]/input"
    )
    st.send_keys(user)
    time.sleep(1)
    st = driver.find_element(
        By.XPATH, "//*[@id='main-container']/div/div[3]/div/div/div/div[1]/div[2]/input"
    )
    st.send_keys(password)
    st.send_keys(Keys.ENTER)
    slide_verification(driver)


# TODO: 根据传入参数点击筛选
def click_params(driver,current_cities,expect_cities:[],years_of_working:[],edu_experiences:[],
                    institutional_requirements:[],current_industries:[],current_titles:[],
                    age_low,age_high,liveness,sex,hopping_freq):
    # 工作城市
    if current_cities[0] == "不限":
        current_city_tag = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="main-container"]/div[1]/div/div[2]/div/div/div[1]'
                           '/form/section/div/div[1]/div[1]/div/span[1]')
            )
        )
        current_city_tag.click()
    else:
        for city in current_cities:
            current_city_tag = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, f"//label[@class='tag-item' and text()='{city}']")
                )
            )
            current_city_tag.click()
    time.sleep(3)

    # 期望城市
    if expect_cities[0] == "不限":
        expect_city_tag = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="main-container"]/div[1]/div/div[2]/div/div/div[1]'
                           '/form/section/div/div[1]/div[2]/div/span[1]')
            )
        )
        expect_city_tag.click()
    else:
        for city in expect_cities:
            expect_city_tag = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        f'//*[@id="main-container"]/div[1]/div/div[2]/div/div/div[1]/form/section/div/'
                        f'div[1]/div[2]/div/div[1]/label[@class="tag-item" and text()="{city}"]',
                    )
                )
            )
            expect_city_tag.click()
    time.sleep(3)

    # 工作经验
    if years_of_working[0] == "不限":
        year_of_working_tag = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//*[@id="main-container"]/div[1]/div/div[2]/div/div/div[1]'
                    '/form/section/div/div[1]/div[3]/div/div/div[1]/label[1]',
                )
            )
        )
        year_of_working_tag.click()
    elif years_of_working[0] == "应届生":
        year_of_working_tag = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//*[@id="main-container"]/div[1]/div/div[2]/div/div/div[1]'
                    '/form/section/div/div[1]/div[3]/div/div/div[1]/label[2]',
                )
            )
        )
        year_of_working_tag.click()
    elif years_of_working[0] == "10年以上":
        year_of_working_tag = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//*[@id="main-container"]/div[1]/div/div[2]/div/div/div[1]/'
                    'form/section/div/div[1]/div[3]/div/div/div[1]/label[6]',
                )
            )
        )
        year_of_working_tag.click()
    else:
        year_of_working_tag = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f'//*[@id="main-container"]/div[1]/div/div[2]/div/div/div[1]/form/section/div/div[1]'
                    f'/div[3]/div/div/div[1]/label[@class="tag-item"]/em[text()="{years_of_working[0][:-1]}"]',
                )
            )
        )
        year_of_working_tag.click()
    time.sleep(3)

    # 教育经历
    if edu_experiences[0] == "不限":
        edu_experience_tag = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="main-container"]/div[1]/div/div[2]/div/div/div[1]'
                           '/form/section/div/div[1]/section[1]/div/div/div/div[1]/label[1]')
            )
        )
        edu_experience_tag.click()
    else:
        for ex in edu_experiences:
            edu_experience_tag = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        f'//*[@id="main-container"]/div[1]/div/div[2]/div/div/div[1]'
                        f'/form/section/div/div[1]/section[1]/div/div/div/div[1]/label'
                        f'[@class="tag-item" and text()="{ex}"]',
                    )
                )
            )
            edu_experience_tag.click()
    time.sleep(3)

    # 院校要求
    if institutional_requirements[0] == "不限":
        institutional_requirement_tag = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="main-container"]/div[1]/div/div[2]/div/div/div[1]'
                           '/form/section/div/div[1]/section[2]/div/div/div/label[1]')
            )
        )
        institutional_requirement_tag.click()
    else:
        for re in institutional_requirements:
            institutional_requirement_tag = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        f'//*[@id="main-container"]/div[1]/div/div[2]/div/div/div[1]'
                        f'/form/section/div/div[1]/section[2]/div/div/div/label'
                        f'[@class="tag-item" and text()="{re}"]',
                    )
                )
            )
            institutional_requirement_tag.click()
    time.sleep(3)

    # 当前行业
    # 当前职位
    # 年龄
    age_low_tag = driver.find_element(By.XPATH, '//*[@id="ageLow"]')
    age_low_tag.clear()
    age_low_tag.send_keys(age_low)
    age_high_tag = driver.find_element(By.XPATH, '//*[@id="ageHigh"]')
    age_high_tag.clear()
    age_high_tag.send_keys(age_high)
    above_1 = driver.find_element(By.XPATH, '//*[@id="main-container"]/div[1]/div/div[2]/div/div/div[1]'
                                            '/form/section/div/div[1]/div[4]/div[1]/div/div/div')
    ActionChains(driver).move_to_element(above_1).perform()
    select_tag_1 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="main-container"]/div[1]/div/div[2]/div/div/div[1]'
                '/form/section/div/div[1]/div[4]/div[1]/div/div/div/button/span'
            )
        )
    )
    select_tag_1.click()
    time.sleep(3)

    # 活跃度
    # 性别
    # sex_button=driver.find_element(By.XPATH,'//*[@id="main-container"]/div[1]/div/div[2]/div/div/div[1]'
    #                                         '/form/section/div/div[1]/div[4]/div[3]/div/div/div')
    # sex_button.click()
    # if sex[0]=="不限":
    #     index_of_sex=1
    # elif sex[0]=="男":
    #     index_of_sex = 2
    # else:
    #     index_of_sex = 3
    # sex_tag=WebDriverWait(driver,10).until(
    #     EC.element_to_be_clickable(
    #         (
    #         By.XPATH,
    #         f'/html/body/div[11]/div/div/div/div[2]/div/div/div[{index_of_sex}]'
    #         )
    #     )
    # )
    # sex_tag.click()
    # 跳槽频率
    raise NotImplementedError()




def consume_compare(current_cities,expect_cities:[],years_of_working:[],edu_experiences:[],
                    institutional_requirements:[],current_industries:[],current_titles:[],
                    age_low,age_high,liveness,sex,hopping_freq):
    s = Service("chrome/chromedriver-win64/chromedriver.exe")
    chrome_options = Options()
    chrome_options.binary_location = "chrome/chrome-win64/chrome.exe"
    driver = webdriver.Chrome(service=s, options=chrome_options)
    create_session(driver)
    time.sleep(10)
    #driver.maximize_window()
    #driver.get("https://h.liepin.com/im/showmsgnewpage?tab=message")
    #    18116195410
    #    6913016fdu
    #time.sleep(30)
    try:
        # 显式等待元素可点击
        wait = WebDriverWait(driver, 10)
        # 通过XPath定位（推荐：结合父元素的data-bar属性）
        # people_link = wait.until(EC.element_to_be_clickable(
        #     (By.XPATH, '//*[@id="main-container"]/header/div[1]/div/ul/li[3]/a')
        # ))
        # 点击链接
        #people_link.click()
        driver.get("https://h.liepin.com/search/getConditionItem")
        wait.until(EC.url_to_be("https://h.liepin.com/search/getConditionItem"))

        #-----------------筛选开始-------------------
        click_params(driver,current_cities,expect_cities,years_of_working,
                edu_experiences,institutional_requirements,current_industries,
                current_titles,age_low,age_high,liveness,sex,hopping_freq)
        #--------------筛选结束-----------------------
        time.sleep(3)
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


        data_list = []

        for index, tr in enumerate(all_trs):
            data_dict = {}  # 每个<tr>初始化一个独立字典
            try:
                random_wait = random.uniform(8, 10)
                main_window = driver.current_window_handle

                # 显式等待并点击<tr>
                clickable_tr = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(tr))
                clickable_tr.click()
                print(f"已点击第 {index + 1} 个<tr>")

                if len(driver.window_handles) > 1:
                    driver.switch_to.window(driver.window_handles[-1])

                    # 使用显式等待确保元素加载
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//body'))
                    )

                    # 提取数据字段（带异常处理和默认值）
                    # 简历编号
                    driver.implicitly_wait(5)
                    data_dict['index_of_people'] = driver.find_element(
                        By.XPATH,
                        '/html/body/div[1]/div[1]/div/div/div/div/section[1]/div[1]/div/div[1]/div[3]/div/span[1]'
                    ).text.strip()[5:] if driver.find_elements(
                        By.XPATH,
                        '/html/body/div[1]/div[1]/div/div/div/div/section[1]/div[1]/div/div[1]/div[3]/div/span[1]'
                    ) else ""


                    # 最后登陆时间
                    data_dict['last_login_time'] = driver.find_element(
                        By.XPATH, '//*[@id="resume-detail-single"]/div[1]/div/div[1]/div[3]/div/span[2]'
                    ).text.strip()[9:] if driver.find_elements(
                        By.XPATH, '//*[@id="resume-detail-single"]/div[1]/div/div[1]/div[3]/div/span[2]'
                    ) else ""

                    # 状态
                    data_dict['status'] = driver.find_element(
                        By.XPATH, '//*[@id="resume-detail-basic-info"]/div[3]/div[1]/span'
                    ).text.strip() if driver.find_elements(
                        By.XPATH, '//*[@id="resume-detail-basic-info"]/div[3]/div[1]/span'
                    ) else ""

                    # 个人信息
                    personal_message = []
                    elements = driver.find_elements(
                        By.XPATH, '//*[@id="resume-detail-basic-info"]/div[3]/div[position()>1]'
                    )
                    for el in elements:
                        text_nodes = driver.execute_script("""
                            const parent = arguments[0];
                            const texts = [];
                            for (const node of parent.childNodes) {
                                if (node.nodeType === Node.TEXT_NODE && node.textContent.trim()) {
                                    texts.push(node.textContent.trim());
                                }
                            }
                            return texts;
                        """, el)

                        # 用空格连接并去除引号
                        personal_message.append(" ".join([text.replace('"', '') for text in text_nodes]))
                    data_dict['personal_message'] = " ".join(personal_message)

                    # 求职意向
                    job_intention = []
                    for i in range(1, 4):
                        xpath = f'//*[@id="resume-detail-job-exp-info"]/div[1]/div[1]/span[{i}]'
                        if driver.find_elements(By.XPATH, xpath):
                            job_intention.append(driver.find_element(By.XPATH, xpath).text.strip())
                    data_dict['job_intention'] = " | ".join(job_intention)

                    # 教育经历（结构化数据）
                    data_dict['edu_experiences'] = []
                    for edu in driver.find_elements(By.CLASS_NAME, 'edu-school-cont'):
                        data_dict['edu_experiences'].append(edu.text.replace('\n', ' ').strip())

                    # 资格证书
                    data_dict['certificates'] = [
                        cert.text.strip()
                        for cert in driver.find_elements(By.CLASS_NAME, 'credential-tag')
                    ]

                    # 语言能力（结构化处理）
                    data_dict['languages'] = []
                    for lang in driver.find_elements(By.CLASS_NAME, 'rd-lang-item'):
                        lang_data = {
                            'type': lang.find_element(By.CLASS_NAME, 'lang-name').text.strip(),
                            'level': [level.text.strip() for level in lang.find_elements(By.CLASS_NAME, 'lang-level')]
                        }
                        data_dict['languages'].append(lang_data)

                    # 技能
                    data_dict['skills'] = [
                        skill.text.strip()
                        for skill in driver.find_elements(By.CLASS_NAME, 'skill-tag')
                    ]

                    # 自我评价
                    data_dict['self_assessment'] = driver.find_element(
                        By.XPATH, '//*[@id="resume-detail-self-eva-info"]/div/div'
                    ).text.strip() if driver.find_elements(
                        By.XPATH, '//*[@id="resume-detail-self-eva-info"]/div/div'
                    ) else ""

                    # 将完整字典加入列表
                    data_list.append(data_dict)
                    print(f"第 {index + 1} 条数据已存储")

                    # 关闭新标签页并切回主窗口
                    driver.close()
                    driver.switch_to.window(main_window)

                    # 每5条打印进度
                    if (index + 1) % 3 == 0:
                        print(f"\n=== 已处理 {index + 1} 条数据 ===")
                        print(json.dumps(data_list[-3:], indent=2, ensure_ascii=False))

                        # 追加写入文件
                        with open('output.json', 'a', encoding='utf-8') as f:
                            json.dump({"batch": (index + 1) // 3, "data": data_list[-3:]},
                                      f, ensure_ascii=False)
                            f.write('\n')

                time.sleep(random_wait)

            except Exception as e:
                print(f"第 {index + 1} 条数据处理失败: {str(e)}")
                # 即使出错也保存已收集的数据
                if data_dict:
                    data_list.append(data_dict)
                continue

        # 最终保存剩余数据
        if data_list:
            with open('output.json', 'a', encoding='utf-8') as f:
                json.dump({"final_batch": data_list}, f, ensure_ascii=False)
                time.sleep(5)
    finally:
        # 保持浏览器打开（根据需求决定是否关闭）
        # driver.quit()
        pass


if __name__ == "__main__":
    # Global variables
    RESUME_LISTS: List[Dict] = []
    RESUME_COUNT: int = 0
    DEBUG: Final[bool] = True

    # Initialization
    setup_logger(DEBUG)
    driver = init_driver()
    create_session(driver)

    # Scraper
    param_list = ["上海", "北京", "1-3年", "", "", "", "", "", "", "", ""]
    conduct_scrape(driver, *param_list)

    print(RESUME_LISTS)
