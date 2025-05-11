import sys, time, random, tempfile, logging, platform
from typing import Final, List, Dict
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.ie.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def setup_logger(debug: bool = False):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG if debug else logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    logger.handlers = []
    logger.addHandler(handler)


def init_driver() -> webdriver.Chrome:
    system_platform = platform.system()
    chrome_options = Options()

    if system_platform == "Windows":
        chromedriver_path = "chrome/chromedriver-win64/chromedriver.exe"
        chrome_binary_path = "chrome/chrome-win64/chrome.exe"
        chrome_options.binary_location = chrome_binary_path
    elif system_platform == "Linux":
        chromedriver_path = "/home/resume/bin/chromedriver"
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"--user-data-dir={tempfile.mkdtemp()}")
    else:
        raise EnvironmentError("Unsupported platform")

    s = Service(chromedriver_path)
    driver = webdriver.Chrome(service=s, options=chrome_options)

    return driver


def create_session(
    driver: webdriver.Chrome,
    website: str = "https://h.liepin.com/im/showmsgnewpage?tab=message",
    user: str = "18116195410",
    password: str = "6913016fdu",
) -> None:
    driver.maximize_window()
    driver.get(website)
    # TODO: 自动填入账号密码，滑动滑块验证码
    time.sleep(30)


# TODO: 根据传入参数点击筛选
def click_params():
    raise NotImplementedError()


def single_scrape(driver: webdriver.Chrome, tr: str, index: int):
    # 显式等待元素可点击
    clickable_tr = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(tr))

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
            index_of_people = driver.find_element(
                by=By.XPATH,
                value="/html/body/div[1]/div[1]/div/div/div/div/section[1]/div[1]/div/div[1]/div[3]/div/span[1]",
            )
            print(index_of_people.text)
        except NoSuchElementException:
            print("未找到简历编号")
        print("\n")

        # 最后登陆时间
        try:
            last_login_time = driver.find_element(
                by=By.XPATH,
                value='//*[@id="resume-detail-single"]/div[1]/div/div[1]/div[3]/div/span[2]',
            )
            print(last_login_time.text)
        except NoSuchElementException:
            print("未找到最后一次登陆时间")
        print("\n")

        # 状态
        try:
            status = driver.find_element(
                by=By.XPATH,
                value='//*[@id="resume-detail-basic-info"]/div[3]/div[1]/span',
            )
            print("状态：", end="")
            print(status.text)
        except NoSuchElementException:
            print("未找到状态")
        print("\n")

        # 个人信息
        try:
            personal_message_1 = driver.find_element(
                by=By.XPATH,
                value='//*[@id="resume-detail-basic-info"]/div[3]/div[2]',
            )
            personal_message_2 = driver.find_element(
                by=By.XPATH,
                value='//*[@id="resume-detail-basic-info"]/div[3]/div[3]',
            )
            print("个人信息：")
            print(f"{personal_message_1.text}\n{personal_message_2.text}")
        except NoSuchElementException:
            print("未找到个人信息")
        print("\n")

        # 求职意向
        try:
            job_intention_1 = driver.find_element(
                by=By.XPATH,
                value='//*[@id="resume-detail-job-exp-info"]/div[1]/div[1]/span[1]',
            )
            job_intention_2 = driver.find_element(
                by=By.XPATH,
                value='//*[@id="resume-detail-job-exp-info"]/div[1]/div[1]/span[2]',
            )
            job_intention_3 = driver.find_element(
                by=By.XPATH,
                value='//*[@id="resume-detail-job-exp-info"]/div[1]/div[1]/span[3]',
            )
            print(
                f"求职意向：{job_intention_1.text}丨{job_intention_2.text}丨{job_intention_3.text}"
            )
        except NoSuchElementException:
            print("")
        print("\n")

        # 教育经历
        try:
            edu_experiences = driver.find_elements(
                by=By.CLASS_NAME, value="edu-school-cont"
            )
            print("教育经历：")
            for items in edu_experiences:
                item = items.find_elements(by=By.TAG_NAME, value="span")
                for edu_experience in item:
                    print(edu_experience.text, end=" ")
                print("\n")
        except NoSuchElementException:
            print("未找到教育经历")
        print("\n")

        # 资格证书
        try:
            certificates = driver.find_elements(
                by=By.CLASS_NAME, value="credential-tag"
            )
            print("资格证书：")
            for certificate in certificates:
                print(certificate.text, end=" ")
        except NoSuchElementException:
            print("未找到资格证书")
        print("\n")

        # 语言能力
        try:
            language_abilitys = driver.find_elements(
                by=By.CLASS_NAME, value="rd-lang-item"
            )
            print("语言能力：")
            for language in language_abilitys:
                lang_type = language.find_element(by=By.CLASS_NAME, value="lang-name")
                print(lang_type.text, end=" ")
                lang_levels = language.find_elements(
                    by=By.CLASS_NAME, value="lang-level"
                )
                for lang_level in lang_levels:
                    print(lang_level.text, end=" ")
                print("\n")
        except NoSuchElementException:
            print("未找到语言能力")
        print("\n")

        # 技能
        try:
            abilities = driver.find_elements(by=By.CLASS_NAME, value="skill-tag")
            print("技能：")
            for ability in abilities:
                print(ability.text, end=" ")
        except NoSuchElementException:
            print("未找到技能")
        print("\n")

        # 自我评价
        try:
            self_assessment = driver.find_element(
                by=By.XPATH,
                value='//*[@id="resume-detail-self-eva-info"]/div/div',
            )
            print("自我评价：")
            print(self_assessment.text)
        except NoSuchElementException:
            print("未找到自我评价")
        print("\n")


def conduct_scrape(
    driver: webdriver.Chrome,
    current_city: str,
    expect_city: str,
    year_of_working: str,
    edu_experience: str,
    institutional_requirement: str,
    current_industry: str,
    current_title: str,
    age: str,
    liveness: str,
    sex: str,
    hopping_freq: str,
):

    try:
        # 显式等待元素可点击
        wait = WebDriverWait(driver, 10)
        # 通过XPath定位（推荐：结合父元素的data-bar属性）
        people_link = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//li[@data-bar='manager-search']/a"))
        )

        # 点击链接
        people_link.click()

        wait.until(EC.url_to_be("https://h.liepin.com/search/getConditionItem"))

        # 工作城市
        current_city_tag = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//label[@class='tag-item' and text()='{current_city}']")
            )
        )
        current_city_tag.click()

        expect_city_tag = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f'//*[@id="main-container"]/div[1]/div/div[2]/div/div/div[1]/form/section/div/'
                    f'div[1]/div[2]/div/div[1]/label[@class="tag-item" and text()="{expect_city}"]',
                )
            )
        )
        expect_city_tag.click()

        # 工作经验
        year_of_working_tag = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f'//*[@id="main-container"]/div[1]/div/div[2]/div/div/div[1]/form/section/div/div[1]'
                    f'/div[3]/div/div/div[1]label[@class="tag-item" and text()="{year_of_working}"]',
                )
            )
        )
        year_of_working_tag.click()
        try:
            # 使用通用定位策略（匹配所有包含 cid 标识的<tr>）
            all_trs = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//tr[contains(@data-tlg-scm, "cid")]')
                )
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

                # 爬取单份简历
                single_scrape(driver, tr, index)
                time.sleep(random_wait)

                # 回到主窗口
                driver.close()
                driver.switch_to.window(main_window)

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
