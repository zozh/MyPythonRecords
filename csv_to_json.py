#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time        : 2023/03/23
@Author      : ZouZhao
@Version     : 0.1.0
@Contact     : wszwc3721@163.com
@License     : Copyright (c) 2023 by zouzhao, All Rights Reserved.
@Description :  csv to json
---Version 0.2.0---
@Time           : 2024/01/22
@Description    : 添加命令行支持
'''
__Author__ = "ZouZhao"
__Version__ = "0.1.0"
__License__ = "Copyright (c) 2023 by zouzhao, All Rights Reserved."
__Name__ = "CsvToJson"
__Description__ = "csv to json"

import os
import csv
import json
import argparse


def get_version() -> str:
    """获得版本版本信息
     
    Returns:
        str: 版本版本信息
    """
    print(f"{__Author__} {__Name__} {__Version__} \n{__License__}")


def convert(in_file: str, out_file: str):
    """csv 转 json
    注：默认文件，存在不检查

    Args:
        in_file (str): csv 路径
        out_file (str): json 路径
    """
    with open(in_file, newline='', encoding='utf-8') as csv_obj:
        csv_reader = csv.DictReader(csv_obj)
        rows = list(csv_reader)

    data = {"records": rows}

    with open(out_file, 'w', encoding='utf-8') as json_obj:
        json.dump(data, json_obj, indent=4, ensure_ascii=False)

    # 输出确认信息
    print(f"CSV 文件已成功转换为 JSON 格式，并保存在 {out_file} 中。")


def get_parameter() -> argparse.Namespace:
    """
    参数解析

    Returns:
        argparse.Namespace

    """

    def check_restraint(parser: argparse.ArgumentParser,
                        args: argparse.Namespace) -> None:
        """检查约束，-t 参数可选，但如果使用必须和 -dp 搭配

        Args:
            parser (argparse.ArgumentParser)
            args (argparse.Namespace)
        Returns:
            NoReturn
        """
        if args.version:
            return

        if not os.path.exists(args.in_file) or not os.path.isfile(
                args.in_file):
            parser.error(
                "No file or does not exist,-if must be the csv file path")

        if not args.out_file:
            args.out_file = args.in_file + ".json"
        else:
            if not os.path.exists(args.out_file) or os.path.isfile(
                    args.out_file):
                parser.error(
                    "No file or does not exist,-of must be the json file path")

    parser = argparse.ArgumentParser(prog=f"{__Name__}",
                                     description=f"{__Description__}",
                                     epilog=f"{__License__}")
    parser.add_argument("-v",
                        "--version",
                        action="store_true",
                        help="increase output version")
    parser.add_argument("-if", "--in_file", help="input csv file path")
    parser.add_argument("-of", "--out_file", help="out json file path")

    args = parser.parse_args()
    check_restraint(parser, args)

    return args


if __name__ == '__main__':
    args = get_parameter()
    if args.version:
        get_version()
    else:
        convert(args.in_file, args.out_file)
