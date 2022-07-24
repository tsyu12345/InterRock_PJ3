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
        layout: const[list[list[Any]]] = [self.__layout()]
        super().__init__(layout, self.WINDOW_NAME)
        
    
    def __layout(self) -> list[Any]:
        
        pref_list:const[list[str]] = list(JisCode.JISCODE_DICT.keys())
        
        L:list[Any] = []
        for pref in pref_list:
            box:const = gui.Checkbox(pref, key=pref)
            L.append(box)
            
        return L
        
    def get_selected_pref(self) -> list[str]:
        """_summary_
        選択された都道府県を取得する。
        Returns:
            list[str]: 選択されたエリアのリスト
        """
        selected:list[str] = []
        for v in self.value.keys():
            if self.value[v] == True:
                selected.append(v) #エリアのキーを渡す。
        
        return selected