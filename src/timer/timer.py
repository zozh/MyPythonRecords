#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time        : 2023/06/26
@Author      : ZouZhao
@Version     : 0.1.0
@Contact     : wszwc3721@163.com
@License     : Copyright (c) 2023 by zouzhao, All Rights Reserved.
@Description : 定时提醒，并记录时间
'''

__Author__ = "ZouZhao"
__Version__ = "0.1.0"
__License__ = "Copyright (c) 2023 by zouzhao, All Rights Reserved."
__Name__ = "timer"
__Description__ = "定时提醒，并记录时间"

import sqlite3
import datetime
import traceback
import tkinter as tk
import tkinter.messagebox

import log


# 初始化
class view:
    """视图
    """

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("计时器")
        self.root.geometry('500x200+100+100')
        self.root.resizable(0, 0)
        self.root.wm_attributes("-topmost", True)
        self.logs = log.LogDoc(__file__)
        self.display_time = tk.StringVar()
        self.display_time.set("00:00:00")
        self.__only_one_is_running = False
        self.__if_update = True
        self.duration_time = None
        self.name = None
        self.label = None
        self.start_time = None
        self.end_time = None
        self.input_name = None
        self.input_label = None

    def update_time(self, end_time) -> None:
        """每帧更新时间显示

        Args:
            end_time (_type_): 结束时间
        """

        now_time = datetime.datetime.now().replace(microsecond=0)

        difference_time = end_time - now_time
        if round(difference_time.total_seconds()) == 0:
            self.end_of_the_timing()
        else:
            self.display_time.set(
                timeTool.strftime(difference_time,
                                  "{hours}:{minutes}:{seconds}"))
            if self.__if_update:
                self.root.after(1000, self.update_time, end_time)
            else:
                self.display_time.set("00:00:00")

    def end_of_the_timing(self) -> None:
        """
        计时结束，重制计时,并保存数据
        """
        now_time = datetime.datetime.now().replace(microsecond=0)
        self.duration_time = timeTool.strftime(now_time - self.start_time,
                                               "{hours}:{minutes}:{seconds}")
        data = self.export_data()
        timeTool.save_sql(data)
        name = self.name
        self.display_messagebox('{} 计时结束了，休息一下吧！'.format(name))
        self.remakes()

    def run(self) -> None:
        """运行GUI
        """
        self.root.mainloop()

    def check_is_update_time(self, duration: int) -> None:
        """时间更新前检查

        Args:
            duration (int):多长时间
        """
        if not self.__only_one_is_running:
            if self.name is not None:
                print(self.name)
                self.__only_one_is_running = True
                self.__if_update = True
                # 保存数据
                end_time = timeTool.get_time_migration(duration)
                start_time = datetime.datetime.now().replace(microsecond=0)
                self.start_time = start_time
                self.end_time = end_time
                self.update_time(end_time)
            else:
                msg = "请输入任务名"
                self.display_messagebox(msg)
        else:
            msg = "正在运行，请先重制"
            self.display_messagebox(msg)

    def remakes(self) -> None:
        """重制时间
        """
        self.__only_one_is_running = False
        self.__if_update = False
        self.display_time.set("00:00:00")
        self.input_name.configure(state='normal')
        self.input_name.delete(0, 'end')
        self.name = None
        if self.label is not None:
            self.input_label.configure(state='normal')
            self.input_label.delete(0, 'end')
            self.label = None

    # tkinter 布局结构
    # root
    #   -left
    #   -right
    #       -top
    #       -bottom
    # 图示
    # -----------right----
    # -        -   top   -
    # -  left  -----------
    # -        -  bottom -
    # --------------------

    def main_page(self) -> None:
        """主界面
        """
        frame1 = tk.Frame(self.root)
        frame1.pack()
        frame_left = tk.Frame(frame1)

        names = {"15分钟": 15, "45分钟": 45, "90分钟": 90}
        for key, value in names.items():
            tk.Button(frame_left,
                      text=key,
                      width=7,
                      height=1,
                      command=lambda value=value: self.check_is_update_time(
                          value)).pack()
        tk.Button(frame_left,
                  text="重制时间",
                  width=7,
                  height=1,
                  command=self.remakes).pack()
        tk.Button(frame_left,
                  text="提前结束",
                  width=7,
                  height=1,
                  command=self.early_termination).pack()
        tk.Button(frame_left,
                  text="终止计时",
                  width=7,
                  height=1,
                  command=self.early_termination).pack()
        frame_left.pack(side='left')

        frame_right = tk.Frame(frame1)
        frame_top = tk.Frame(frame_right)
        tk.Label(frame_top, text="名称：").grid(row=0, column=0)
        self.input_name = tk.Entry(frame_top)
        self.input_name.grid(row=0, column=1)
        tk.Label(frame_top, text="标签：").grid(row=1, column=0)
        self.input_label = tk.Entry(frame_top)
        self.input_label.grid(row=1, column=1)
        tk.Button(frame_top,
                  text="确定",
                  width=7,
                  height=1,
                  command=self.get_input()).grid(row=0,
                                                 rowspan=4,
                                                 column=2,
                                                 columnspan=4)
        frame_top.pack(side='top')

        frame_bottom = tk.Frame(frame_right)
        tk.Label(frame_bottom,
                 textvariable=self.display_time,
                 font=("微软雅黑", 20)).grid(row=1, column=1)
        frame_bottom.pack(side='bottom')
        frame_right.pack(side='right')

    def display_messagebox(self, msg: str) -> None:
        """弹窗提醒

        Args:
            msg (str): 消息
        """
        tk.messagebox.showinfo(title='消息', message=msg)

    def get_input(self) -> None:
        """获取输入并锁定输入框

        Args:
            inData (Entry):Entry 对象
        """
        self.input_name.configure(state='readonly')
        self.name = self.input_name.get()
        self.input_label.configure(state='readonly')
        self.label = self.input_label.get()

    def early_termination(self) -> None:
        """提前结束
        """
        self.end_of_the_timing()

    def export_data(self) -> tuple:
        """导出数据
        """
        return (self.name, self.label, self.start_time, self.end_time,
                self.duration_time)


class timeTool:
    """时间类
    """

    @staticmethod
    def strftime(time_delta: callable, fmt: str) -> None:
        """格式化 timedelta 对象

        Args:
            time_delta (callable): timedelta
            fmt (str): 字符串

        Returns:
            _type_: _description_
        """
        d = {}
        d["hours"], rem = divmod(time_delta.seconds, 3600)
        d["minutes"], d["seconds"] = divmod(rem, 60)
        return fmt.format(**d)

    @staticmethod
    def get_time_migration(time_len: int, start_time: list = None) -> None:
        """获取当前时间

        Args:
            time_len (int): 持续时间
            start_time (_type_, optional): 开始时间. 默认为 None.

        Returns:
            None
        """
        if start_time is None:
            start_time = datetime.datetime.now().strftime(
                '%Y %m %d %H %M %S').split(" ")
        start_time = [int(x) for x in start_time]
        year = start_time[0]
        month = start_time[1]
        day = start_time[2]
        hours = start_time[3]
        minutes = start_time[4] + time_len
        seconds = start_time[5]

        if minutes >= 60:
            carry = int(minutes / 60)
            minutes %= 60
            hours += carry

        if hours >= 24:
            carry = int(hours / 24)
            hours %= 24
            day += carry

        end_time = datetime.datetime(year, month, day, hours, minutes, seconds)
        return end_time

    @staticmethod
    def save_sql(data):
        """保存数据
        """
        sql = SQLTool()
        sql.save_sql(data)


class SQLTool:
    """Sqlite 工具类
    """

    def __init__(self) -> None:
        pass

    def save_sql(self, inData: tuple) -> bool:
        """保存到sqlite

        Args:
            inData (tuple):含有表数据的元组

        Returns:
            bool: 成功true,失败false
        """
        try:
            conn = sqlite3.connect(r'time.db')
            cur = conn.cursor()
            rowcount = 0
            rowcount = cur.execute(
                'INSERT INTO record (ID,name,label,start_time,end_time,duration_time)\
                VALUES (null,?,?,?,?,?);', inData).rowcount
            if rowcount == 1:
                conn.commit()
                return True

        except Exception:
            conn.rollback()
            traceback.print_exc()
            return False


if __name__ == '__main__':
    app = view()
    app.main_page()
    app.run()
