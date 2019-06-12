from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
 
# 日向坂46のメンバーとブログの更新回数のカウンター
members = {
    '井口 眞緒': 0, '潮 紗理菜': 0, '柿崎 芽実': 0, '影山 優佳': 0, \
    '加藤 史帆': 0, '齊藤 京子': 0, '佐々木 久美': 0, '佐々木 美玲': 0, \
    '高瀬 愛奈': 0, '高本 彩花': 0, '東村 芽依':0, '金村 美玖': 0, \
    '河田 陽菜': 0, '小坂 菜緒': 0, '富田 鈴花': 0, '丹生 明里': 0, \
    '濱岸 ひより': 0, '松田 好花': 0, '宮田 愛萌': 0, '渡邉 美穂': 0, \
    '上村 ひなの' : 0
    }

options = Options()

# options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'

# headlessモードで起動する
# options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# 最初に開くページ(クロールの起点となるページ, 日向坂46の個人ブログを想定)
baseUrl = 'https://www.hinatazaka46.com/s/official/diary/member/list?ima=0000'

# 日向坂ブログのトップページを開く
driver.get(baseUrl)

# タイトルに日向坂46 公式ブログが含まれていることを確認する
assert '日向坂46 公式ブログ' in driver.title

# 最大10秒待機
wait = WebDriverWait(driver, 10)
while True:
    try:
        # ブログの著作者を一つでも取得できるまで最大10秒待機
        wait.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'c-blog-article__name')))
        names = driver.find_elements_by_class_name('c-blog-article__name')
        for name in names:
            for member in members:
                if member == name.text:
                    members[member] += 1

        # ページネーションを一つでも取得できるまで最大10秒待機
        wait.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'c-pager__item--count')))
        # >ボタンを探す
        link = driver.find_element_by_css_selector('.c-pager__item--count.c-pager__item--next')
        link.click()
    except (KeyboardInterrupt, NoSuchElementException):
        # Ctrl + Cを押した時, >ボタンがない時日向坂46のメンバーとブログの更新回数のカウンターを表示する
        print(members)
        break
# ウィンドウを閉じる
driver.quit()
