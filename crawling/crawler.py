from selenium import webdriver  # webdriver를 이용해 해당 브라우저를 열기 위해
from selenium.webdriver.common.by import By  # html요소 탐색을 할 수 있게 하기 위해
from selenium.webdriver.support.ui import (
    WebDriverWait,
)  # 브라우저의 응답을 기다릴 수 있게 하기 위해
from selenium.webdriver.support import (
    expected_conditions as EC,
)  # html요소의 상태를 체크할 수 있게 하기 위해
from datetime import datetime, timedelta
import time
import re


def openurl():
    # 페이지
    driver_dev = webdriver.Chrome()

    driver_link = webdriver.Chrome()
    driver_dev.get("https://dev-event.vercel.app/events")
    driver_link.get(
        "https://linkareer.com/list/contest?filterBy_categoryIDs=35&filterType=CATEGORY&orderBy_direction=DESC&orderBy_field=CREATED_AT&page=1"
    )
    return driver_dev, driver_link


def dev_crawling(driver):
    wait = WebDriverWait(driver, 10)
    all_data = wait.until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "Item_item__HzT1B"))
    )
    data_list1 = []
    # 날짜 형식 YYYY.MM.DD를 찾는 정규 표현식 패턴
    date_pattern = r"\d{4}\.\d{2}\.\d{2}"

    for item in all_data:
        href = item.find_element(By.TAG_NAME, "a").get_attribute("href")
        name = item.find_element(By.CLASS_NAME, "Item_item__content__title__94_8Q").text
        opener = item.find_element(By.CLASS_NAME, "Item_host__3dy8_").text
        date = item.find_element(By.CLASS_NAME, "Item_date__date__CoMqV").text
        time.sleep(1)
        img = item.find_element(By.TAG_NAME, "img").get_attribute("src")

        dates = re.findall(date_pattern, date)
        ex_start = dates[0] if dates else None
        ex_end = dates[1] if len(dates) > 1 else None

        activity_data = {
            "ex_name": name,
            "ex_link": href,
            "ex_host": opener,
            "ex_image": img,
            "ex_start": ex_start,
            "ex_end": ex_end,
            "ex_flag": 1,
        }
        data_list1.append(activity_data)
    print(data_list1)


def link_crawling(driver):
    wait = WebDriverWait(driver, 10)
    test = wait.until(
        EC.presence_of_all_elements_located(
            (By.CLASS_NAME, "activity-list-card-item-wrapper")
        )
    )
    # 전체 데이터를 저장할 리스트
    data_list2 = []
    for item in test:
        href = item.find_element(By.TAG_NAME, "a").get_attribute("href")
        name = item.find_element(By.CLASS_NAME, "activity-title").text
        opener = item.find_element(By.CLASS_NAME, "organization-name").text
        date = item.find_element(By.CSS_SELECTOR, 'div[class^="SecondInfoText__"]').text
        time.sleep(3)  # robots.txt 정책에 따른 딜레이
        img = item.find_element(By.TAG_NAME, "img").get_attribute("src")

        days_remaining_match = re.search(r"D-\d+", date)
        days_remaining = (
            int(days_remaining_match.group(0)[2:]) if days_remaining_match else 0
        )
        current_date = datetime.now()
        deadline_date = current_date + timedelta(days=days_remaining)
        deadline_str = deadline_date.strftime("%Y-%m-%d")

        activity_data = {
            "ex_name": name,
            "ex_link": href,
            "ex_host": opener,
            "ex_image": img,
            "ex_start": current_date.strftime("%Y-%m-%d"),
            "ex_end": deadline_str,
            "ex_flag": 2,
        }
        data_list2.append(activity_data)
    print(data_list2)


def main():
    driver = webdriver.Chrome()
    today = datetime.today()
    try:
        driver.get("https://dev-event.vercel.app/events")
        dev_crawling(driver)

        driver.get(
            "https://linkareer.com/list/contest?filterBy_categoryIDs=35&filterType=CATEGORY&orderBy_direction=DESC&orderBy_field=CREATED_AT&page=1"
        )
        link_crawling(driver)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
