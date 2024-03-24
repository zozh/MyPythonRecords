#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time        : 2024/03/23
@Author      : ZouZhao
@Version     : 0.1.0
@Contact     : wszwc3721@163.com
@License     : Copyright (c) 2023 by zouzhao, All Rights Reserved.
@Description : json to yaml
---Version 0.2.0---
@Time           : 2024/01/22
@Description    : 添加命令行支持
'''

__Author__ = "ZouZhao"
__Version__ = "0.1.0"
__License__ = "Copyright (c) 2023 by zouzhao, All Rights Reserved."
__Name__ = "jsonToYaml"
__Description__ = "json to yaml"

import os
import json
import argparse

import yaml


def get_version() -> str:
    """获得版本版本信息

    Returns:
        str: 版本版本信息
    """
    print(f"{__Author__} {__Name__} {__Version__} \n{__License__}")


def convert(in_file: str, out_file: str) -> None:
    """json 转 yaml
    注：默认文件，存在不检查

    Args:
        in_file (str): json 路径
        out_file (str): yaml 路径
    """

    with open(in_file, 'r', encoding="utf-8") as json_file:
        data = json.load(json_file)

    yaml_data = yaml.dump(data, sort_keys=False)

    with open(out_file, 'w', encoding="utf-8") as yaml_file:
        yaml_file.write(yaml_data)


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
