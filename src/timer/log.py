#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time        : 2023/06/26
@Author      : ZouZhao
@Version     : 0.1.0
@Contact     : wszwc3721@163.com
@License     : Copyright (c) 2023 by zouzhao, All Rights Reserved.
@Description : log tool
'''

__Author__ = "ZouZhao"
__Version__ = "0.1.0"
__License__ = "Copyright (c) 2023 by zouzhao, All Rights Reserved."
__Name__ = "log"
__Description__ = "log tool"

import logging


class LogDoc:
    """
    日志
    """

    def __init__(self, filename: str, level: str = logging.DEBUG):
        self.filename = filename
        logging.basicConfig(filename=filename.split(".")[0] + 'Log.txt',
                            level=level,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        print()

    def log_to_file(self, out: str):
        """把日志输出到文件

        Args:
            out (str): 错误信息
        """
        logging.debug(out)
