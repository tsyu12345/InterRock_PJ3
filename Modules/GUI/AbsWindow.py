from __future__ import annotations
from typing import Any, Final as const, Callable
from abc import ABCMeta, abstractmethod
from PySimpleGUI.PySimpleGUI import Window


class AbsWindowComponent(object, metaclass=ABCMeta):
    """[summary]\n
    windowレベルの基底抽象クラス定義。
    """
    
    def __init__(self, layout:list[list[Any]], window_name=None)-> None:
        self.event_handler:dict[str, list[Callable | tuple]] = {} #TODO:EventHandlerオブジェクトの定義をつくり、それで注釈する。
        self.event:str = ""
        self.value:dict[str, str] = {}
        
        self.layout:list[list[Any]] = layout
        self.window:Window = Window(window_name)
    
    
    
    def addEventListener(self, key:str, callback:Callable, *args) -> None:
        """_summary_\n
        イベントリスナーを設定する。\n
        Args:\n
            key: イベントキー\n
            callback: イベントハンドラー\n
            args: イベントハンドラーに渡す引数\n
        """
        self.event_handler[key] = [callback, args]
        print(self.event_handler)
        
    def __catchEvent(self) -> None:
        """_summary_\n
        イベントをキャッチする。\n
        """
        if self.event in self.event_handler:
            
            callback:Callable = self.event_handler[self.event][0] #FIXME:type annotation
            args:tuple = self.event_handler[self.event][1] #FIXME:type annotation
            
            if args == ():
                callback()
            else:
                callback(args)
    
    def display(self) -> None:
        """_summary_\n
        ウィンドウを表示する.
        must use in while loop.
        """
        self.event, self.value = self.window.read()
        self.__catchEvent()
    
    @abstractmethod
    def dispose(self) -> None:
        """_summary_\n
        ウィンドウを破棄する
        """
        pass