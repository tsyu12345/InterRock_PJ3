import openpyxl as px 
import requests as rq
from requests import exceptions as RqExceptions
import threading 
import re 
import time
import sys
from selenium import webdriver
import selenium
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup as bs

class ScrapUrl:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("start-maximized")
        self.options.add_argument("enable-automation")
        self.options.add_argument("--headless")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-infobars")
        self.options.add_argument('--disable-extensions')
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--disable-browser-side-navigation")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--ignore-ssl-errors')
        prefs = {"profile.default_content_setting_values.notifications": 2}
        self.options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(executable_path='./chromedriver.exe')

    def search(self, area):
        def select_choice(select_text, element_id):
            chroice = self.driver.find_element_by_id(element_id)
            select = Select(chroice)
            return select.select_by_visible_text(select_text)

        self.driver.get('https://etsuran.mlit.go.jp/TAKKEN/kensetuKensaku.do')
        select_choice('本店', 'choice')
        select_choice(area, 'kenCode')
        select_choice('50', 'dispCount')
        search_btn = self.driver.find_element_by_css_selector('#input > div:nth-child(6) > div:nth-child(5)')
        search_btn.click()
        

    def scrap_url(self):
        def get_href(a_tag_list):
            url_list = []
            for a in a_tag_list:
                url_list.append(a.get('href'))
            return url_list
        
        time.sleep(2)
        res_count = self.driver.find_element_by_id('pageListNo1')
        select = Select(res_count)
        all_options = select.options
        loop_count = len(all_options)
        url_list = []
        for i in range(loop_count):
            html = self.driver.page_source
            soup = bs(html, 'lxml')
            list = soup.select('table.re_disp > tbody > tr > td > a')
            url_list.append(get_href(list)) #結果1ページ分のURLを取得。
            next_btn = self.driver.find_element_by_css_selector('#container_cont > div.result.clr > div:nth-child(5) > img')
            next_btn.click()
            time.sleep(2)
        return url_list


class ScrapInfo:
    
    def scrap(self, url):
        respons = rq.get(url)
        print(url, end = "")
        print(respons.status_code)
        try:
            #Scraiping Process here
            soup = bs(respons, 'lxml')

        except RqExceptions.RequestException as Error:
            print("Exception Occured")
            sys.exit(1)
    
    def call_jis_code(self, key):
        pref_jiscode = {
            "北海道": '01',
            "青森県": '02',
            "岩手県": '03',
            "宮城県": '04',
            "秋田県": '05',
            "山形県": '06',
            "福島県": '07',
            "茨城県": '08',
            "栃木県": '09',
            "群馬県": 10,
            "埼玉県": 11,
            "千葉県": 12,
            "東京都": 13,
            "神奈川県": 14,
            "新潟県": 15,
            "富山県": 16,
            "石川県": 17,
            "福井県": 18,
            "山梨県": 19,
            "長野県": 20,
            "岐阜県": 21,
            "静岡県": 22,
            "愛知県": 23,
            "三重県": 24,
            "滋賀県": 25,
            "京都府": 26,
            "大阪府": 27,
            "兵庫県": 28,
            "奈良県": 29,
            "和歌山県": 30,
            "鳥取県": 31,
            "島根県": 32,
            "岡山県": 33,
            "広島県": 34,
            "山口県": 35,
            "徳島県": 36,
            "香川県": 37,
            "愛媛県": 38,
            "高知県": 39,
            "福岡県": 40,
            "佐賀県": 41,
            "長崎県": 42,
            "熊本県": 43,
            "大分県": 44,
            "宮崎県": 45,
            "鹿児島県": 46,
            "沖縄県": 47
        }
        code = pref_jiscode[key]
        print(code)
        return code




class WriteExcel:
    book = px.Workbook()
    sheet = book.worksheets[0]
    def __init__(self):
        col_list = [
            "許可年月", 
            "許可番号簡易",
            "商号又は名称（カナ）",
            "商号又は名称（詳細）",	
            "代表者の氏名（カナ）",	
            "代表者の氏名（漢字）",
            "郵便番号",
            "都道府県コード",
            "都道府県",
            "市区町村・番地・建物",	
            "電話番号",
            "法人・個人区分",
            "資本金額",	
            "建設業以外の兼業の有無",	
            "土木工事業",
            "建築工事業",
            "大工工事業",
            "左官工事業",
            "とび・土工工事業",
            "石工事業",
            "屋根工事業",
            "電気工事業",
            "管工事業",	
            "タイル・れんが・ブロツク工事業",
            "鋼構造物工事業", 
            "鉄筋工事業",
            "舗装工事業",
            "しゆんせつ工事業",
            "板金工事業",
            "ガラス工事業",
            "塗装工事業",
            "防水工事業",
            "内装仕上工事業",
            "機械器具設置工事業",
            "熱絶縁工事業",
            "電気通信工事業",
            "造園工事業",
            "さく井工事業",
            "建具工事業",
            "水道施設工事業",
            "消防施設工事業",
            "清掃施設工事業",
            "許可の有効期間",
        ]
        for c in range(1, len(col_list)):
            self.sheet.cell(row=1, column=c, value=col_list[c])

    def write_data(self, index, col, write_data):
        self.sheet.cell(row=index, column=col, value=write_data)
    
    def save_book(self, save_path):
        self.book.save(save_path)


def main(save_path, area):
    excel = WriteExcel()
    scrap_url = ScrapUrl()
    scrap_url.search(area)
    url_list = scrap_url.scrap_url()
    print(url_list)

if __name__ == "__main__":
    main("./test.xlsx", "01 北海道")



