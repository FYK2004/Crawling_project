import logging, requests, time, random
import cv2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

BG_IMAGE_PATH = "./tmp/bg_with_gap.png"
BK_IMAGE_PATH = "./tmp/slider_piece.png"


def download_captcha(
    driver: webdriver.Chrome,
    config_xpath: str = "/html/body/div/div[3]/div[2]/div[1]/div[2]/img",
    slider_xpath: str = "/html/body/div/div[3]/div[2]/div[1]/div[3]/img",
):
    # Open the page with driver
    time.sleep(3)

    # Get image elements
    bg_with_gap_elem = driver.find_element(By.XPATH, config_xpath)
    slider_piece_elem = driver.find_element(By.XPATH, slider_xpath)

    # Extract the image URLs from the XPaths
    bg_with_gap_url = driver.find_element(By.XPATH, config_xpath).get_attribute("src")
    slider_piece_url = driver.find_element(By.XPATH, slider_xpath).get_attribute("src")

    # Download the images
    bg_with_gap = requests.get(bg_with_gap_url).content
    slider_piece = requests.get(slider_piece_url).content

    with open(BG_IMAGE_PATH, "wb") as f:
        f.write(bg_with_gap)

    with open(BK_IMAGE_PATH, "wb") as f:
        f.write(slider_piece)

    logging.info("验证码图片成功下载并保存！")

    return bg_with_gap_elem, slider_piece_elem


def calculate_dist(bg_with_gap_path: str, bg_elem: WebElement):
    bg_img = cv2.imread(bg_with_gap_path, 0)

    # 得到缩放比例
    orig_h, orig_w = bg_img.shape
    rendered_size = bg_elem.size
    render_w = rendered_size["width"]
    render_h = rendered_size["height"]
    scale = render_w / orig_w

    # 轮廓边缘检测
    edges = cv2.Canny(bg_img, 100, 200)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    img_with_rectangles = bg_img.copy()
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if x > 350 and w > 50 and h > 50:
            cv2.rectangle(img_with_rectangles, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # Prepare text
            label = f"({x}, {y}, {w}, {h})"

            # Draw text at top-left corner
            cv2.putText(
                img_with_rectangles,
                label,
                (x, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 255),
                1,
                cv2.LINE_AA,
            )
    cv2.imwrite("image/rectangles.png", img_with_rectangles)

    # 判断是否为符合条件的轮廓
    target_contour = None
    subtar_contour = None
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        # logging.info(f"Find countour ==> x={x}, y={y}, w={w}, h={h}")
        if abs(w - h) < 20 and w > 80 and h > 80 and x > 450:
            logging.info(f"Target countour ==> x={x}, y={y}, w={w}, h={h}")
            target_contour = (x, y, w, h)
            break
        elif w > 85 and h > 85 and x > 450:
            logging.info(f"Subtar countour ==> x={x}, y={y}, w={w}, h={h}")
            subtar_contour = (x, y, w, h)

    # TODO: 没找到就刷新验证码
    if target_contour is None:
        if subtar_contour is None:
            logging.error("未能找到符合条件的缺块轮廓")
            return random.uniform(220, 250)
        else:
            target_contour = subtar_contour

    dx = target_contour[0]

    distance = dx * scale
    logging.info(f"滑块需要滑动到 {distance} px")
    return distance


def slide_verification(driver: webdriver.Chrome, right_position: int):
    try:
        # 等待滑块元素可见
        slider = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[@id='tcaptcha_drag_thumb']")
            )
        )

        # 获取 slider 当前位置
        slider_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "tcaptcha_drag_button"))
        )
        left_position = slider_button.value_of_css_property("left")
        left_position = float(left_position.replace("px", "").strip())
        logging.info(f"滑块当前位置为 {left_position} px")

        # 创建动作链
        action = ActionChains(driver)

        # 点击并按住滑块
        action.click_and_hold(slider).perform()

        # 模拟滑动过程
        current_position = left_position
        while current_position < right_position:
            move_distance = min(
                right_position - current_position, random.uniform(10, 30)
            )
            action.move_by_offset(xoffset=move_distance, yoffset=0).perform()
            current_position += move_distance
            time.sleep(random.uniform(0.02, 0.1))

        # 释放滑块
        action.release().perform()
        driver.save_screenshot("./image/2-slider.png")
        logging.info("滑动完成")
    except Exception as e:
        logging.info("滑动验证码失败:", e)
