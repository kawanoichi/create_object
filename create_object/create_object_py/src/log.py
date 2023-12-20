"""ログを切れに出力するモジュール
    log.add(title="", log="")
"""

import os
import inspect


class Log:
    def __init__(self, log_color_code=34):
        """コンストラクタ.
        collor code:
            30: 黒 (Black)
            31: 赤 (Red)
            32: 緑 (Green)
            33: 黄 (Yellow)
            34: 青 (Blue)
            35: マゼンタ (Magenta)
            36: シアン (Cyan)
            37: 白 (White)
        """
        self.log_color_code = log_color_code
        self.locate_list = []
        self.title_list = []
        self.log_list = []

    def print_color(self, text):
        """色を指定して出力する関数."""
        print(f"\033[{self.log_color_code}m{text}\033[0m")

    def add(self, title="", log=""):
        """ログを追加する関数.
        TODO: script_nameに問題あり
        経由しているときに弱い
        """
        caller_frame = inspect.currentframe().f_back.f_back
        if caller_frame is not None: 
            script_name = os.path.basename(caller_frame.f_globals['__file__'])
            locate = f"{script_name}({inspect.currentframe().f_back.f_lineno})"
            self.locate_list.append(locate)
        else:
            self.locate_list.append("")
        self.title_list.append(str(title))
        self.log_list.append(str(log))

    def show(self):
        """ログを表示する関数."""
        max_locate_length = len(max(self.locate_list, key=len))
        max_title_length = len(max(self.title_list, key=len))
        max_log_length = len(max(self.log_list, key=len))

        for locate, title, log in zip(self.locate_list, self.title_list, self.log_list):
            text = f"Logs| {locate:>{max_locate_length}}| {title:>{max_title_length}}: {log:>{max_log_length}}"
            self.print_color(text)


def test():
    log = Log()
    log.add(title="aaa", log="bbbbb")
    log.add(title="aa", log="bb")
    log.add(title="aaaaa", log="bb")
    log.add(title="a", log="bbbbbbb")

    log.show()


if __name__ == "__main__":
    test()
