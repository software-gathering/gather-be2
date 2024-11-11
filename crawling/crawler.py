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
    time.sleep(1)  # robots.txt 정책에 따른 딜레이
    all_data = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".ActivityInfo-desktop__StyledWrapper-sc-659c82f-0")
        )
    )
    # 전체 데이터를 저장할 리스트

    data_list2 = []
    for item in all_data:
        # href = item.find_element(By.TAG_NAME, "a").get_attribute("href")
        name = item.find_element(By.CLASS_NAME, "title").text
        opener = item.find_element(By.CLASS_NAME, "organization-name").text
        # 날짜 형식 패턴 (예: YYYY.MM.DD)
        date_pattern = r"\d{4}\.\d{2}\.\d{2}"

        # 모든 <span> 요소 가져오기
        spans = item.find_elements(By.TAG_NAME, "span")

        # 날짜 초기화
        start_date = None
        end_date = None

        # 각 <span> 요소의 텍스트 확인
        for span in spans:
            text = span.text
            # 정규 표현식을 사용하여 날짜 형식과 일치하는지 확인
            if re.match(date_pattern, text):
                if not start_date:
                    start_date = text  # 첫 번째로 찾은 날짜는 시작일로 설정
                elif not end_date:
                    end_date = text  # 두 번째로 찾은 날짜는 종료일로 설정
                    break  # 종료일을 찾으면 반복 중단

        img = item.find_element(By.TAG_NAME, "img").get_attribute("src")

        activity_data = {
            "ex_name": name,
            "ex_link": None,
            "ex_host": opener,
            "ex_image": img,
            "ex_start": start_date,
            "ex_end": end_date,
            "ex_flag": 2,
        }
        data_list2.append(activity_data)
    print(data_list2)


def main():
    driver = webdriver.Chrome()

    try:
        # driver.get("https://dev-event.vercel.app/events")
        # dev_crawling(driver)

        # driver.get(
        #     "https://linkareer.com/list/contest?filterBy_categoryIDs=35&filterType=CATEGORY&orderBy_direction=DESC&orderBy_field=CREATED_AT&page=1"
        # )
        driver.get("https://linkareer.com/activity/208528")
        link_crawling(driver)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
