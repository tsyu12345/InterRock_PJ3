from __future__ import annotations
from typing import Any, Final as const
import PySimpleGUI as gui

from AbsWindow import AbsWindowComponent
from ..Scraping.Jiscode import JisCode

class AreaSelectWindow(AbsWindowComponent):
    """_summary_\n
    都道府県選択のウィンドウ
    """
    WINDOW_NAME:const[str] = "都道府県選択"
    
    def __init__(self) -> None:
        layout: const[list[list[Any]]] = [
            #ここにウィンドウのレイアウトを記述する。
        ]
        super().__init__(layout, self.WINDOW_NAME)
        
    
    def __layout(self) -> list[Any]:
        
        pref_list:const[list[str]] = list(JisCode.JISCODE_DICT.keys())
        
        