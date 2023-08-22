# 더보기_대외활동

from bs4 import BeautifulSoup
from selenium import webdriver
import time

def plus_activity(start_index=0) : # 더보기_대외활동
    
    url = "https://www.campuspick.com/activity"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    chrome_options.add_argument("disable-gpu")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

    driver = webdriver.Chrome(options=chrome_options) # 드라이버 시작
    
    driver.get(url) # 캠퍼스픽 사이트 가져오기
    driver.implicitly_wait(10) # 웹 페이지가 로딩될 떄까지 최대 10초 대기
    
    result_list = []
    scroll_count = 0
    max_scroll_count = 5
    
    while scroll_count < max_scroll_count :
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # 스크롤
        time.sleep(1)  # 스크롤 한번 하고 대기시간
        scroll_count += 1
    
    html = driver.page_source # 웹페이지의 소스코드 가져오기
    soup = BeautifulSoup(html, 'html.parser') # 파싱하기
    plus_activity_list = soup.select('a.top') # 정보 있는 요소 가져오기
    
    if start_index >= len(plus_activity_list) : # 20개씩 가져오기
        driver.close()
        return result_list

    for plus_activity in plus_activity_list[start_index : start_index+20] :
        
        title = plus_activity.select_one('h2').text # 제목
        dday_element = plus_activity.select_one('p.info span.dday') # 디데이
        dday = dday_element.text.strip() if dday_element else 'No D-day' # 디데이
        if dday == '마감' : # 마감이면 안가져오기
            continue
        link = 'https://www.campuspick.com' + plus_activity['href']  # 링크
        image_url = plus_activity.select_one('figure')['data-image'] # 이미지
    
        plus_activity_info = {
            'title' : title,
            'dday' : dday,
            'link' : link,
            'image_url' : image_url,
        }
        result_list.append(plus_activity_info)

    driver.close() # 드라이버 닫기
       
    return result_list