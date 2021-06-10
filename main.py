import PySimpleGUI as gui
import scrap


class AreaSelect:
    def lay_out(self):
        L = [
                [gui.Text("都道府県",
                        key='pref_title', size=(60, None))],
                [gui.InputText(key=('pref_name')), gui.Button('エリア選択')],
            ]


class PathSelect:


def main():
    gui.theme('BluePurple')
    width = 700
    height = 300
    """
    layout Object here
    """
    win = gui.Window('国土交通省 建設業許可 抽出ツール',
                     icon='69b54a27564218141a41104e1e345cff_xxo.ico')
    while True:
        event, value = win.read()
        # when window close
        if event in ("Quit", None):
            break
    win.close()


main()
