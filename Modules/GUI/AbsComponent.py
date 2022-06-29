from __future__ import annotations
from typing import Any, Final as const, Callable
from abc import ABCMeta, abstractmethod
from PySimpleGUI.PySimpleGUI import Window

class AbsGUIComponent(object, metaclass=ABCMeta):
    """[summary]\n
    各GUIコンポーネントの基底抽象クラス定義。
    """
    def __init__(self, layout:list[list[Any]]) -> None:
        self.layout:list[list[Any]] = layout
    
    
