#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time        : 2023/08/09
@Author      : ZouZhao
@Version     : 0.1.0
@Contact     : wszwc3721@163.com
@License     : Copyright (c) 2023 by zouzhao, All Rights Reserved.
@Description : 将 flomo 导出内容转为 md 格式保存到本地，不支持图片
---Version 0.2.0---
@Time           : 2024/01/24
@Description    : 添加命令行支持
'''

__Author__ = "ZouZhao"
__Version__ = "0.1.0"
__License__ = "Copyright (c) 2023by zouzhao, All Rights Reserved."
__Name__ = ""
__Description__= "将 flomo 导出内容转为 md 格式保存到本地，不支持图片"

import os
import argparse

import html2text
from bs4 import BeautifulSoup


def check_file(path:str, extension:str=None)->tuple:
    """检查是否为文件，是否为指定类型

    Args:
        path (str): 目标路径
        extension (str, optional): 文件扩展名.默认为 None.

    Returns:
        tuple(bool,str): 状态和消息
    """
    if not os.path.isfile(path):
        return False, "Path is not a file."

    if extension is not None:
        filename, actual_extension = os.path.splitext(path)
        if actual_extension.lower() != f".{extension.lower()}":
            return False, f"File is not of the specified extension: {extension}."

    return True, "Path exists and is a file with the specified extension (if provided)."

def convert(in_file: str, out_file: str):
    """flomo html to csv
    注：默认文件存在不检查

    Args:
        in_file (str):  目标文件路径
        out_file (str): 输出文件路径
    """
    soup = BeautifulSoup(open(in_file, encoding="utf-8"))
    memos = soup.find_all("div", "memo")
    print_log = open(out_file, 'w', encoding="utf-8")
    for memo in memos:
        if len(memo.find_all("div", "files")) == 0:
            continue
        md_text = html2text.html2text(memo.prettify())
        print(md_text, file=print_log)
        
def get_parameter() -> argparse.Namespace:
    """
    参数解析

    Returns:
        argparse.Namespace

    """
    def check_restraint(parser: argparse.ArgumentParser,
                     args: argparse.Namespace) -> None:
        """检查约束

        Args:
            parser (argparse.ArgumentParser)
            args (argparse.Namespace)
        Returns:
            None
        """
        if args.version:
            return
        
        if not args.in_file:
            parser.error(
                "No file or does not exist,-if must be the flomo html file path")
        
        if not args.out_file:
            args.out_file = args.in_file + ".md"
            
        if check_file(args.in_file,".html"):
            parser.error(
                "No file or does not exist,-if must be the flomo html file path")
        else:
            if check_file(args.out_file,".md"):
                parser.error(
                    "No file or does not exist,-of must be the md file path")


    parser = argparse.ArgumentParser(prog=f"{__Name__}",
             description=f"{__Description__}",
             epilog=f"{__License__}")
    parser.add_argument("-v",
           "--version",
           action="store_true",
           help="increase output version")
    parser.add_argument("-if", "--in_file", help="input flomo html file path")
    parser.add_argument("-of", "--out_file", help="out md file path")

    args = parser.parse_args()
    check_restraint(parser, args)

    return args

def get_version() -> str:
    """获得版本版本信息

    Returns:
        str: 版本版本信息
    """
    print(f"{__Author__} {__Name__} {__Version__} \n{__License__}")
    
if __name__ == '__main__':
    args=get_parameter()
    if args.version:
        get_version()
    else:
        print(args.in_file,args.out_file)
        convert(args.in_file,args.out_file)    
 