import inspect


class CaseInsensitiveInvokeMixin:
    """
    This MixIn allows you to call methods in a case-insensitive manner.
    Case-InsensitiveにメソッドをコールできるようにするMixIn。例えば、plug_turn_onを plugTurnOnでも呼べるようにする
    """
    def __init__(self):
        self.__routines = None
        # メソッドのリストを作成し、アンダースコアを除去、すべて小文字にしたキーで辞書を作成
        routines = filter(lambda x: not x[0].startswith('__'), inspect.getmembers(self, inspect.isroutine))
        self.__routines = {name.lower().replace('_', ''): func for name, func in routines}

    def __getattr__(self, item):
        routines_attr = self.__routines
        # 普通にメソッドが見つかったら、そのメソッドを返す
        try:
            return self.__getattribute__(item)
        except AttributeError:
            pass # fallthrough

        # そうでない場合、辞書から取得して返す
        try:
            ret = routines_attr[item.lower().replace('_', '')]
        except KeyError:
            raise AttributeError(f"AttributeError: {item} is not found")
        return ret
