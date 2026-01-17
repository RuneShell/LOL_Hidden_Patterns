from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import pandas as pd
import time


#==========  project vars ===========
_URL = r"https://op.gg/ko/lol/leaderboards/tier"

#### 자유 랭크 게임
# [ 등수, 이름, 랭크, LP, 모스트 1, 모스트 2, 모스트 3, 레벨, 승리 수, 패배 수, 승률 ]
RANKS = ['Challenger', 'Grandmaster', 'Master', 'Diamond', 'Emerald', 'Platinum', 'Gold', 'Silver', 'Bronze', 'Iron']



# Init Driver
options = Options()
user_agent = r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
options.add_argument("--window-size=1920,1080") # hidden class가 생기지 않도록
options.add_argument(f'user-agent={user_agent}')

driver = webdriver.Chrome(options=options)

def getDriver(driver, url):
    print("접속 시도: ", url)
    driver.get(url)
    driver.implicitly_wait(2)
    time.sleep(10)
    print('\n', driver.title)
    return driver




# Get Elements
def getDataFromTable(driver):
    if len(names) >= 1000:
        return False

    try:
        table = driver.find_element(By.TAG_NAME, 'table')
        print(">> Table 로드 완료")
    except:
        print(">> Table을 찾을 수 없습니다.")
        return
    rows = table.find_elements(By.CSS_SELECTOR, 'tbody tr')
    
    for row in rows:
        tds = row.find_elements('tag name', 'td') # length 7

        if(len(tds) == 1):
            continue 
        elif(len(tds) < 7):
            print("Err: ", len(tds), end="")
            for i in range(len(tds)):
                print(tds[i].text, end=",")
            print()

        # ranking
        rank_num.append(tds[0].text)
        print(rank_num[-1])

        # name & tag
        full_name = tds[1].text.split('\n')

        names.append(full_name[-2]) # length가 3이고 'P'로 시작하는 경우가 있음
        tags.append(full_name[-1])

        # LP
        LP.append(tds[3].text)

        # most 1 2 3
        mosts = tds[4].find_elements(By.TAG_NAME, 'a')
        try:
            most1.append(mosts[0].get_attribute('data-tooltip-content'))
        except:
            most1.append("")
        try:
            most2.append(mosts[1].get_attribute('data-tooltip-content'))
        except:
            most2.append("")
        try:
            most3.append(mosts[2].get_attribute('data-tooltip-content'))
        except:
            most3.append("")
        
        # level
        lvl.append(tds[5].text)

        # wins / lose / winning rate
        win_spans = tds[6].find_elements(By.TAG_NAME, 'span')
        if(len(win_spans) != 3):
            print("win_span Err: ", len(win_spans), win_spans[0].text, win_spans[1].text, win_spans[2].text)
        wins.append(win_spans[0].text[:-1]) # '203승' -> '203'
        loses.append(win_spans[1].text[:-1])
        winning_rate.append(win_spans[2].text)

    return True





for rank in RANKS[7:]:
    rank_num = []
    names = []
    tags = []
    ranks = []  
    LP = []
    most1 = []
    most2 = []
    most3 = []
    lvl = []
    wins = []
    loses = []
    winning_rate = []

    for page in range(1, 11):
        driver = getDriver(driver, f"{_URL}?tier={rank.lower()}&region=kr&page={page}")
        WebDriverWait(driver, 30).until( # 드라이버가 로드될 때까지 대기
            lambda driver: driver.execute_script('return document.readyState') == 'complete'
        )
        getDataFromTable(driver)


    print("excel 작성 준비")
    df = pd.DataFrame({
            'ranking': rank_num,
            'name': names,
            'tag': tags,
            'tier': rank,
            'LP': LP,
            'most1': most1,
            'most2': most2,
            'most3': most3,
            'level': lvl,
            'win': wins,
            'lose': loses,
            'win_rate': winning_rate
        })

    print("excel 작성 시작: ", rank)
    with pd.ExcelWriter('output.xlsx', engine='openpyxl', mode='a') as writer:
        df.to_excel(writer, sheet_name=rank, index=False)

print("프로그램 정상 종료")
