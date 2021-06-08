from os import write
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

class Scraping:
    book = px.Workbook()
    sheet = book.worksheets[0]
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
        

    def scrap(self, path):
        info = ScrapInfo(path)
        info.ready_book()        
        time.sleep(2)
        res_count = self.driver.find_element_by_id('pageListNo1')
        select = Select(res_count)
        all_options = select.options
        loop_count = 2 #len(all_options)
        for i in range(1, loop_count):
            for j in range(2, 52):
                #InfoScrap here
                company = self.driver.find_element_by_css_selector('#container_cont > table > tbody > tr:nth-child(' + str(j) +  ') > td:nth-child(4) > a')
                company.click()
                html = self.driver.page_source
                info.scrap(html)                        
                self.driver.back()     
            next_btn = self.driver.find_element_by_css_selector('#container_cont > div.result.clr > div:nth-child(5) > img')
            next_btn.click()
            time.sleep(2)
        self.driver.quit()

class ScrapInfo(Scraping):
    def __init__(self, path):
        self.path = path

    def ready_book(self):
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
        self.book.save(self.path)

    def scrap(self, html):
        index = self.sheet.max_row
        print(index)
        soup = bs(html, 'lxml')
        perm_day = soup.select_one("div.scroll-pane > table.re_summ_4 > tbody > tr > td > a").get_text()
        self.sheet.cell(row=index, column=1, value=perm_day)
        perm_num = soup.select_one("#input > div.clr > table > tbody > tr > td").get_text()
        self.sheet.cell(row=index, column=2, value=perm_num)
        name_kana = soup.select_one("#input > div:nth-child(1) > table > tbody > tr:nth-child(2) > td > p").get_text()
        self.sheet.cell(row=index, column=3, value=name_kana)
        com_name = soup.select_one("#input > div:nth-child(1) > table > tbody > tr:nth-child(2) > td").get_text()
        self.sheet.cell(row=index, column=4, value=com_name)
        ceo_kana = soup.select_one("#input > div:nth-child(1) > table > tbody > tr:nth-child(3) > td > p").get_text()
        self.sheet.cell(row=index, column=5, value=ceo_kana)
        ceo_name = soup.select_one("#input > div:nth-child(1) > table > tbody > tr:nth-child(3) > td").get_text()
        self.sheet.cell(row=index, column=6, value=ceo_name)
        #add other list.

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

    def convert_year(self, R_year): #和暦記号を西暦へ変換し返す
        dictionary = {
            
        }


def main(path, area):
    scrap = Scraping()
    scrap.search(area)
    scrap.scrap(path)

if __name__ == "__main__":
    main("./test.xlsx", "01 北海道")



