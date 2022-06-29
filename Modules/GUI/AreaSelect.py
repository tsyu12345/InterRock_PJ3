from __future__ import annotations
from typing import Any, Final as const
import PySimpleGUI as gui

from AbsComponent import AbsGUIComponent
class AreaSelect(AbsGUIComponent):
    """_summary_\n
    エリア選択オブジェクト
    """
    
    LABEL_TEXT_KEY:const[str] = 'pref_title'
    INPUT_BOX_KEY:const[str] = 'pref_name'
    BUTTON_KEY: const[str] = 'SELECT'
    BUTTON_TEXT: const[str] = "エリア選択"
    
        
    def __init__(self) -> None:
        
        layout:const[list[list[Any]]] = [
            [gui.Text("都道府県", key=self.LABEL_TEXT_KEY, size=(60, None))],
            [gui.InputText(key=(self.INPUT_BOX_KEY)), gui.Button(self.BUTTON_TEXT, key=self.BUTTON_KEY)],
        ]
        
        super().__init__(layout)
        

class AreaSelectCheckBox(AbsGUIComponent):
    """_summary_\n
    都道府県選択ウィンドウでの、エリア選択チェックボックス
    """