from os import terminal_size
from concurrent.futures import ThreadPoolExecutor as TPE
from tkinter import font
import PySimpleGUI as gui
from PySimpleGUI.PySimpleGUI import popup_error
from scrap import Scraping
import time
import sys


class AreaSelect:
    def lay_out(self):
        L = [
            [gui.Text("都道府県",
                      key='pref_title', size=(60, None))],
            [gui.InputText(key=('pref_name')), gui.Button('エリア選択')],
            [gui.Checkbox('本店(本社のみの抽出。営業所の抽出無し。)', key='honten',
                          font=(terminal_size, 11))]
        ]
        return L

    def are_select(self):
        prefs = '北海道,青森県,岩手県,宮城県,秋田県,山形県,福島県,茨城県,栃木県,群馬県,埼玉県,千葉県,東京都,神奈川県,新潟県,富山県,石川県,福井県,山梨県,長野県,岐阜県,静岡県,愛知県,三重県,滋賀県,京都府,大阪府,兵庫県,奈良県,和歌山県,鳥取県,島根県,岡山県,広島県,山口県,徳島県,香川県,愛媛県,高知県,福岡県,佐賀県,長崎県,熊本県,大分県,宮崎県,鹿児島県,沖縄県'
        list_pref = prefs.split(',')
        L = []
        cnt = 0
        for i in range(8):
            add = []
            for j in range(6):
                if cnt != 47:
                    add.append(gui.Checkbox(
                        list_pref[cnt], key=list_pref[cnt]))
                    cnt += 1
            L.append(add)
        L.append([gui.Button('OK', key='OK')])
        window = gui.Window('エリア選択', layout=L)
        pref = []
        while True:
            event, value = window.read()
            print(event)
            print(value)
            for v in value.keys():
                if value[v] == True:
                    pref.append(v)
            print(pref)
            if event in ("Quit", None, 'OK'):
                break
        window.close()
        return pref


class PathSelect:

    def lay_out(self):
        L = [
            [gui.Text("フォルダ選択", key='path_title', size=(60, None))],
            [gui.InputText(key='path'), gui.SaveAs(
                "選択", file_types=([('Excelファイル', '*.xlsx')]))]
        ]
        return L

class Job():

    def __init__(self, path, areas, honten):
        self.areas = areas
        self.path = path
        self.honten = honten
        self.scrap = Scraping(self.path)
        # threading.Thread.__init__(self)

    def run(self):
        for pref in self.areas:
            self.scrap.search(pref, self.honten)
            self.scrap.scrap()
        return True

    def cancel(self):
        self.scrap.book.save(self.path)
        self.scrap.driver.quit()
        

def obj_frame(lay_out_data):
    L = [
        [gui.Frame("抽出条件", lay_out_data[0])],
        [gui.Frame("保存先", lay_out_data[1])],
        [gui.Button("抽出実行")]
    ]
    return L


def call_jis_code(key):
    pref_jiscode = {
        "北海道": "01",
        "青森県": "02",
        "岩手県": "03",
        "宮城県": "04",
        "秋田県": "05",
        "山形県": "06",
        "福島県": "07",
        "茨城県": "08",
        "栃木県": "09",
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
    return str(code)


def main():
    execuetr = TPE(max_workers=2)
    gui.theme('BluePurple')
    """
    layout Object here
    """
    area_obj = AreaSelect()
    path_obj = PathSelect()
    lay_data = [area_obj.lay_out(), path_obj.lay_out()]
    layout = obj_frame(lay_data)
    win = gui.Window('国土交通省 建設業許可 抽出ツール',
                     icon='69b54a27564218141a41104e1e345cff_xxo.ico', layout=layout)
    comp_flg = False
    detati = False
    running = False
    while comp_flg == False:
        event, value = win.read()
        print(event)
        print(value)
        if event == 'エリア選択':
            pref_list = area_obj.are_select()
            add = ""
            for i in range(len(pref_list)):
                if i == len(pref_list)-1:
                    add += pref_list[i]
                else:
                    add += pref_list[i] + ","
                win['pref_name'].update(add)

        if event == '抽出実行':
            for i, pref in enumerate(pref_list):
                # prefCode + " " + prefNameのフォーマットへ変換
                pref = call_jis_code(pref_list[i]) + " " + pref_list[i]
                pref_list[i] = pref
            job = Job(value['path'], pref_list, value['honten'])
            # try:
            future = execuetr.submit(job.run,)
            running = True
            while running:
                try:
                    cancel = gui.OneLineProgressMeter(
                        "処理中です...", job.scrap.count, job.scrap.resultcnt, 'prog', "現在抽出処理中です...。これには数時間かかることがあります。\nコンピュータの電源を切らないでください。")
                except TypeError:
                    cancel = gui.OneLineProgressMeter("処理中です...", 0, 1, 'prog', "ただいま抽出準備中です...。")
                    pass
                
                if cancel == False:
                    running = False
                    detati = True

                if event in ("Quit", None):
                    running = False
                
                if job.scrap.end_flg:
                    running = False
                    comp_flg = True

        if detati:
            try:
                job.cancel()
                execuetr.shutdown(wait=True)
                gui.popup("処理を中断しました。途中保存ファイル先は下記です。\n保存先："+value['path'])
            except TypeError:
                pass

        if comp_flg:
            execuetr.shutdown(wait=True)
            gui.popup('お疲れ様でした。抽出完了です。ファイルを確認してください。\n保存先：'+value['path'])
            break

        if event in ("Quit", None):
            break

    win.close()
    sys.exit()


if __name__ == "__main__":
    main()
