#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time        : 2024/03/28
@Author      : ZouZhao
@Version     : 0.1.0
@Contact     : wszwc3721@163.com
@License     : Copyright (c) 2024 by zouzhao, All Rights Reserved.
@Description : 缩短 execl 表中 url 长度
'''

__Author__ = "ZouZhao"
__Version__ = "0.1.0"
__License__ = "Copyright (c) 2024 by zouzhao, All Rights Reserved."
__Name__ = "execlUrlShort"
__Description__ = " 缩短 execl 表中 url 长度"
import os
import argparse
import urllib.parse

import pandas as pd


def check_file(path: str, extension: str = None) -> tuple:
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


def remove_useless_params(url: str,
                          useless_params: list = None,
                          remove_all: bool = False) -> str:
    """去除 url 参数，以缩短 url

    Args:
        url (str): url 字符串
        useless_params (list, optional): 被去除参数列表. 默认为 None.
        remove_all (bool, optional): 是否全部去除.默认为 False.

    Returns:
        str: 缩短后的 url
    """

    parsed_url = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(parsed_url.query)

    if remove_all:
        params = {}
    else:
        if useless_params:
            for param in useless_params:
                if param in params:
                    del params[param]

    new_query = urllib.parse.urlencode(params, doseq=True)
    if not new_query:
        new_url = urllib.parse.urlunparse(
            (parsed_url.scheme, parsed_url.netloc, parsed_url.path, None, None,
             parsed_url.fragment))
    else:
        new_url = urllib.parse.urlunparse(
            (parsed_url.scheme, parsed_url.netloc, parsed_url.path, None,
             new_query, parsed_url.fragment))

    return new_url


def run(path: str, sheet_name: str, header: int, start: int, end: int,
        column_name: str):
    """运行
    """
    df = pd.read_excel(path, sheet_name=sheet_name, header=header)
    column_data = df[column_name]
    column_data_list = column_data.astype(str).tolist()

    for url in column_data_list[start:end]:
        print(remove_useless_params(url, remove_all=True))


def get_version() -> str:
    """获得版本版本信息

    Returns:
        str: 版本版本信息
    """
    print(f"{__Author__} {__Name__} {__Version__} \n{__License__}")


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

        if not args.path:
            parser.error(
                "No file or does not exist, -p must be the execl file path")

    parser = argparse.ArgumentParser(prog=f"{__Name__}",
                                     description=f"{__Description__}",
                                     epilog=f"{__License__}")
    parser.add_argument("-v",
                        "--version",
                        action="store_true",
                        help="increase output version")
    parser.add_argument("-s", "--start", type=int, help="start page")
    parser.add_argument("-e", "--end", type=int, help="end page")
    parser.add_argument("-p", "--path", type=str, help="execl file save path")
    parser.add_argument("-c", "--column", type=str, help="column name")
    parser.add_argument("-c", "--column", type=str, help="column name")
    parser.add_argument("-h",
                        "--header",
                        type=int,
                        default=2,
                        help="which line to start with ")

    args = parser.parse_args()
    check_restraint(parser, args)

    return args


if __name__ == '__main__':
    args = get_parameter()
    if args.version:
        get_version()
    else:
        run(args.path, args.sheet_name, args.header, args, args.start,
            args.end, args.column_name)
