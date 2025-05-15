import sys, time, json, random, tempfile, logging, platform
from typing import Final, List, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.ie.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from utils import setup_logger, load_json, init_dirs
from verification import (
    download_captcha,
    calculate_dist,
    slide_verification,
    BG_IMAGE_PATH,
    BK_IMAGE_PATH,
)


CONFIG_PATH: Final = "./config/chrome.json"
TEMPLATE_PATH: Final = "./template/task.json"


def init_driver() -> webdriver.Chrome:
    system_platform = platform.system().lower()
    config = load_json(CONFIG_PATH)

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

    service = Service(chromedriver_path, verbose=True)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    logging.info("Initialize the chrom driver successfully!")
    return driver


def create_session(
    driver: webdriver.Chrome,
    website: str = "https://h.liepin.com/account/login",
    user: str = "18116195410",
    password: str = "6913016fdu",
) -> None:
    logging.info("Start creating session...")
    driver.maximize_window()
    driver.get(website)
    time.sleep(2)

    # 自动填入账号密码，滑动滑块验证码
    # Click the login page
    WebDriverWait(driver, 1).until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[@id='main-container']/div/div[3]/div/div/ul/li[2]")
        )
    ).click()

    # Fill in the username
    username_input = WebDriverWait(driver, 1).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//*[@id='main-container']/div/div[3]/div/div/div/div[1]/div[1]/input",
            )
        )
    )
    username_input.send_keys(user)

    # Fill in the password
    password_input = driver.find_element(
        By.XPATH, "//*[@id='main-container']/div/div[3]/div/div/div/div[1]/div[2]/input"
    )
    password_input.send_keys(password)

    # Submit the form
    password_input.send_keys(Keys.ENTER)

    time.sleep(2)
    driver.save_screenshot("./image/1-login.png")
    logging.info("Successfully fill the username and password...")

    # 等待滑动验证码出现，自动计算滑动距离
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "tcaptcha_iframe"))
        )
        driver.switch_to.frame("tcaptcha_iframe")
        bg_elem, _ = download_captcha(driver)
        right_position = calculate_dist(BG_IMAGE_PATH, bg_elem)
        slide_verification(driver, right_position)
    except:
        raise ValueError()

    try:
        time.sleep(10)
        # 显式等待元素可点击
        wait = WebDriverWait(driver, 10)
        # 通过XPath定位（推荐：结合父元素的data-bar属性）
        # people_link = wait.until(EC.element_to_be_clickable(
        #     (By.XPATH, '//*[@id="main-container"]/header/div[1]/div/ul/li[3]/a')
        # ))
        # 点击链接
        # people_link.click()
        driver.save_screenshot("./image/3-verify.png")
        driver.get("https://h.liepin.com/search/getConditionItem")
        wait.until(EC.url_to_be("https://h.liepin.com/search/getConditionItem"))
    except:
        driver.save_screenshot("./image/4-loginerr.png")
        logging.error("登录失败！")
        raise ValueError("登录失败！")


# TODO: 检查爬虫参数的正确性
def validate_params(data_dict: Dict) -> bool:
    raise NotImplementedError()


# TODO: 根据传入参数点击筛选
def click_params(
    driver,
    current_cities: List = [],
    expect_cities: List = [],
    years_of_working: List = [],
    education: List = [],
    edu_requirements: List = [],
    current_industries: List = [],
    current_positions: List = [],
    age_low: List = [],
    age_high: List = [],
    liveness: List = [],
    sex: List = [],
    hopping_freq: List = [],
):
    """
    根据指定的筛选条件进行候选人筛选

    参数说明：
    - `current_cities`：候选人当前所在城市列表
    - `expect_cities`：候选人期望工作城市列表
    - `years_of_working`：工作年限范围列表
    - `education`：教育学历列表
    - `edu_requirements`：院校要求列表
    - `current_industries`：候选人当前所在行业列表
    - `current_positions`：候选人当前职位列表
    - `age_low`：年龄下限
    - `age_high`：年龄上限
    - `liveness`：活跃度等级列表
    - `sex`：性别列表
    - `hopping_freq`：跳槽频率范围列表

    注意：
    - 所有传入参数应为列表形式
    - TODO：记录每个筛选条件的所有可选项，用于后续判断参数是否错误。
    """
    # 工作城市
    if current_cities[0] == "不限":
        current_city_tag = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//*[@id="main-container"]/div[1]/div/div[2]/div/div/div[1]'
                    "/form/section/div/div[1]/div[1]/div/span[1]",
                )
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
                (
                    By.XPATH,
                    '//*[@id="main-container"]/div[1]/div/div[2]/div/div/div[1]'
                    "/form/section/div/div[1]/div[2]/div/span[1]",
                )
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
                    "/form/section/div/div[1]/div[3]/div/div/div[1]/label[1]",
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
                    "/form/section/div/div[1]/div[3]/div/div/div[1]/label[2]",
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
                    "form/section/div/div[1]/div[3]/div/div/div[1]/label[6]",
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
    if education[0] == "不限":
        edu_experience_tag = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//*[@id="main-container"]/div[1]/div/div[2]/div/div/div[1]'
                    "/form/section/div/div[1]/section[1]/div/div/div/div[1]/label[1]",
                )
            )
        )
        edu_experience_tag.click()
    else:
        for ex in education:
            edu_experience_tag = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        f'//*[@id="main-container"]/div[1]/div/div[2]/div/div/div[1]'
                        f"/form/section/div/div[1]/section[1]/div/div/div/div[1]/label"
                        f'[@class="tag-item" and text()="{ex}"]',
                    )
                )
            )
            edu_experience_tag.click()
    time.sleep(3)

    # 院校要求
    if edu_requirements[0] == "不限":
        institutional_requirement_tag = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//*[@id="main-container"]/div[1]/div/div[2]/div/div/div[1]'
                    "/form/section/div/div[1]/section[2]/div/div/div/label[1]",
                )
            )
        )
        institutional_requirement_tag.click()
    else:
        for re in edu_requirements:
            institutional_requirement_tag = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        f'//*[@id="main-container"]/div[1]/div/div[2]/div/div/div[1]'
                        f"/form/section/div/div[1]/section[2]/div/div/div/label"
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
    age_low_tag.send_keys(age_low[0])
    age_high_tag = driver.find_element(By.XPATH, '//*[@id="ageHigh"]')
    age_high_tag.clear()
    age_high_tag.send_keys(age_high[0])
    above_1 = driver.find_element(
        By.XPATH,
        '//*[@id="main-container"]/div[1]/div/div[2]/div/div/div[1]'
        "/form/section/div/div[1]/div[4]/div[1]/div/div/div",
    )
    ActionChains(driver).move_to_element(above_1).perform()
    select_tag_1 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="main-container"]/div[1]/div/div[2]/div/div/div[1]'
                "/form/section/div/div[1]/div[4]/div[1]/div/div/div/button/span",
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


def single_scrape(driver: webdriver.Chrome, data_dict: Dict):
    """爬取单份简历"""
    # 使用显式等待确保元素加载
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//body"))
    )

    # 提取数据字段（带异常处理和默认值）
    # 简历编号
    driver.implicitly_wait(5)
    data_dict["index_of_people"] = (
        driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div[1]/div/div/div/div/section[1]/div[1]/div/div[1]/div[3]/div/span[1]",
        ).text.strip()[5:]
        if driver.find_elements(
            By.XPATH,
            "/html/body/div[1]/div[1]/div/div/div/div/section[1]/div[1]/div/div[1]/div[3]/div/span[1]",
        )
        else ""
    )

    # 最后登陆时间
    data_dict["last_login_time"] = (
        driver.find_element(
            By.XPATH,
            '//*[@id="resume-detail-single"]/div[1]/div/div[1]/div[3]/div/span[2]',
        ).text.strip()[9:]
        if driver.find_elements(
            By.XPATH,
            '//*[@id="resume-detail-single"]/div[1]/div/div[1]/div[3]/div/span[2]',
        )
        else ""
    )

    # 状态
    data_dict["status"] = (
        driver.find_element(
            By.XPATH,
            '//*[@id="resume-detail-basic-info"]/div[3]/div[1]/span',
        ).text.strip()
        if driver.find_elements(
            By.XPATH,
            '//*[@id="resume-detail-basic-info"]/div[3]/div[1]/span',
        )
        else ""
    )

    # 个人信息
    personal_message = []
    elements = driver.find_elements(
        By.XPATH,
        '//*[@id="resume-detail-basic-info"]/div[3]/div[position()>1]',
    )
    for el in elements:
        text_nodes = driver.execute_script(
            """
            const parent = arguments[0];
            const texts = [];
            for (const node of parent.childNodes) {
                if (node.nodeType === Node.TEXT_NODE && node.textContent.trim()) {
                    texts.push(node.textContent.trim());
                }
            }
            return texts;
            """,
            el,
        )

        # 用空格连接并去除引号
        personal_message.append(
            " ".join([text.replace('"', "") for text in text_nodes])
        )
    data_dict["personal_message"] = " ".join(personal_message)

    # 求职意向
    job_intention = []
    for i in range(1, 4):
        xpath = f'//*[@id="resume-detail-job-exp-info"]/div[1]/div[1]/span[{i}]'
        if driver.find_elements(By.XPATH, xpath):
            job_intention.append(driver.find_element(By.XPATH, xpath).text.strip())
    data_dict["job_intention"] = " | ".join(job_intention)

    # 教育经历（结构化数据）
    data_dict["education"] = []
    for edu in driver.find_elements(By.CLASS_NAME, "edu-school-cont"):
        data_dict["education"].append(edu.text.replace("\n", " ").strip())

    # 资格证书
    data_dict["certificates"] = [
        cert.text.strip()
        for cert in driver.find_elements(By.CLASS_NAME, "credential-tag")
    ]

    # 语言能力（结构化处理）
    data_dict["languages"] = []
    for lang in driver.find_elements(By.CLASS_NAME, "rd-lang-item"):
        lang_data = {
            "type": lang.find_element(By.CLASS_NAME, "lang-name").text.strip(),
            "level": [
                level.text.strip()
                for level in lang.find_elements(By.CLASS_NAME, "lang-level")
            ],
        }
        data_dict["languages"].append(lang_data)

    # 技能
    data_dict["skills"] = [
        skill.text.strip() for skill in driver.find_elements(By.CLASS_NAME, "skill-tag")
    ]

    # 自我评价
    data_dict["self_assessment"] = (
        driver.find_element(
            By.XPATH, '//*[@id="resume-detail-self-eva-info"]/div/div'
        ).text.strip()
        if driver.find_elements(
            By.XPATH, '//*[@id="resume-detail-self-eva-info"]/div/div'
        )
        else ""
    )

    # 工作经历
    data_dict['work_experience'] = []
    for work in driver.find_elements(By.CLASS_NAME, 'rd-info-tpl-item.rd-work-item-cont'):
        work_head = work.find_element(By.CSS_SELECTOR, '.rd-info-tpl-item-head')
        work_cont = work.find_element(By.CSS_SELECTOR, '.rd-info-tpl-item-cont')
        tags = work_cont.find_elements(By.CSS_SELECTOR, '.tags-box > .tag')
        work_data = {
            'company': work_head.find_element(By.CSS_SELECTOR, 'h5.ellipsis').text.strip(),
            'employment_period': work_head.find_element(By.CSS_SELECTOR, 'span.rd-work-time').text.strip(),
            'all_tags': [tag.text.strip() for tag in tags],
            'job_name': work_cont.find_element(By.CSS_SELECTOR, 'h6.job-name').text.strip(),
        }
        work_rows = work_cont.find_elements(By.CLASS_NAME, 'rd-info-row')
        for work_row in work_rows:
            work_cols = work_row.find_elements(By.CLASS_NAME, 'rd-info-col')
            for work_col in work_cols:
                try:
                    key = work_col.find_element(By.CLASS_NAME, 'rd-info-col-title').text.strip('：')
                    value = work_col.find_element(By.CLASS_NAME, 'rd-info-col-cont').text.strip().replace("\n"," ")
                    work_data[key] = value
                except:
                    continue
        data_dict['work_experience'].append(work_data)

    # 项目经历
    try:
        elem = WebDriverWait(driver, 15).until(
            lambda x: x.find_element(
                By.XPATH,
                "//span[contains(@class, 'rd-info-other-link') and contains(text(), '显示其他')]"
            )
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
        time.sleep(0.5)  # 等待滚动惯性
        driver.execute_script("arguments[0].click()", elem)
    except (NoSuchElementException, TimeoutException):
        logging.info("未找到展开按钮，已跳过")
    except Exception as e:
        logging.info(f"点击失败: {str(e)}")

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((
                By.CSS_SELECTOR,
                '.rd-info-tpl-item.rd-project-item-cont'
            ))
        )
    except TimeoutException:
        logging.info("项目加载超时")

    data_dict['project_experience'] = []
    for project in driver.find_elements(By.CSS_SELECTOR, '.rd-info-tpl-item.rd-project-item-cont'):
        project_head = project.find_element(By.CSS_SELECTOR, '.rd-info-tpl-item-head')
        project_cont = project.find_element(By.CSS_SELECTOR, '.rd-info-tpl-item-cont')
        project_data = {
            'project_name': project_head.find_element(By.CSS_SELECTOR, 'h5.ellipsis').text.strip(),
            'employment_period': project_head.find_element(By.CSS_SELECTOR, 'span.rd-project-time').text.strip(),
        }
        project_rows = project_cont.find_elements(By.CLASS_NAME, 'rd-info-row')
        for project_row in project_rows:
            project_cols = project_row.find_elements(By.CLASS_NAME, 'rd-info-col')
            for project_col in project_cols:
                try:
                    key = project_col.find_element(By.CLASS_NAME, 'rd-info-col-title').text.strip('：')
                    value = project_col.find_element(By.CLASS_NAME, 'rd-info-col-cont').text.strip().replace("\n"," ")
                    project_data[key] = value
                except:
                    continue
        data_dict['project_experience'].append(project_data)


def conduct_scrape(
    driver: webdriver.Chrome,
    current_cities: list = [],
    expect_cities: list = [],
    years_of_working: list = [],
    education: list = [],
    edu_requirements: list = [],
    current_industries: list = [],
    current_positions: list = [],
    age_low: list = [],
    age_high: list = [],
    liveness: list = [],
    sex: list = [],
    hopping_freq: list = [],
    **kwargs: Dict,
):
    try:
        # -----------------筛选开始-------------------
        click_params(
            driver,
            current_cities,
            expect_cities,
            years_of_working,
            education,
            edu_requirements,
            current_industries,
            current_positions,
            age_low,
            age_high,
            liveness,
            sex,
            hopping_freq,
        )
        # -----------------筛选结束-------------------
        time.sleep(3)
        try:
            # 使用通用定位策略（匹配所有包含 cid 标识的<tr>）
            all_trs = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//tr[contains(@data-tlg-scm, "cid")]')
                )
            )
        except TimeoutException:
            logging.info("未找到符合条件的<tr>元素")
            driver.quit()
            exit()

        data_list = []

        # TODO: 用 tqdm 展示进度条
        for index, tr in enumerate(all_trs):
            # 每个<tr>初始化一个独立字典
            data_dict = {}
            try:
                random_wait = random.uniform(8, 10)
                main_window = driver.current_window_handle

                # 显式等待并点击<tr>
                clickable_tr = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable(tr)
                )
                clickable_tr.click()
                logging.info(f"已点击第 {index + 1} 个<tr>")

                if len(driver.window_handles) > 1:
                    driver.switch_to.window(driver.window_handles[-1])

                    single_scrape(driver, data_dict)

                    # 将完整字典加入列表
                    data_list.append(data_dict)
                    logging.info(f"第 {index + 1} 条数据已存储")

                    # 关闭新标签页并切回主窗口
                    driver.close()
                    driver.switch_to.window(main_window)

                    # 每5条打印进度
                    if (index + 1) % 1 == 0:
                        logging.info(f"\n=== 已处理 {index + 1} 条数据 ===")
                        print(json.dumps(data_list[-1:], indent=2, ensure_ascii=False))

                        # 追加写入文件
                        with open("output.json", "a", encoding="utf-8") as f:
                            json.dump(
                                {"batch": (index + 1) // 1, "data": data_list[-1:]},
                                f,
                                ensure_ascii=False,
                            )
                            f.write("\n")

                time.sleep(random_wait)

            except Exception as e:
                logging.info(f"第 {index + 1} 条数据处理失败: {str(e)}")
                # 即使出错也保存已收集的数据
                if data_dict:
                    data_list.append(data_dict)
                continue

        # 最终保存剩余数据
        if data_list:
            with open("output.json", "a", encoding="utf-8") as f:
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
    DEBUG: Final[bool] = len(sys.argv) == 1

    # Initialization
    init_dirs()
    setup_logger(DEBUG)
    driver = init_driver()
    create_session(driver)

    # Scraper
    if DEBUG:
        param_dict = load_json(TEMPLATE_PATH)
    else:
        param_dict = json.loads(sys.argv[1])

    # validate_params(**param_dict)

    # Start scraping...
    conduct_scrape(driver, **param_dict)

    print(RESUME_LISTS)
