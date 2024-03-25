# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
@Time           :   2023/10/12 15:36:02
@Author         :   zouzhao
@Version        :   0.1.0
@Contact        :   wszwc3721@163.com
@License        :   Copyright (c) 2023 by zouzhao, All Rights Reserved.
@Description    :  编码转换工具
---Version 0.2.0---
@Time           : 2024/01/23
@Description    : 添加命令行支持
"""

import os
import argparse

import codecs
import chardet


def is_dir(path: str) -> bool:
    """判断路径是文件还是目录

    Args:
        path (str): 路径

    Returns:
        bool: 目录 True，文件 False
    """
    if os.path.isdir(path):
        return True
    elif os.path.isfile(path):
        return False


def get_all_file_path(path: str, recursive: bool = False) -> list:
    """
    获得目录路径下所有文件路径
    Args:
        path (str): 目录路径
        recursive (bool, optional): 是否递归查找. 默认为 False.

    Returns:
        list: 包含路径地址的列表
    """
    file_list = []

    if recursive:
        for root, dirs, files in os.walk(path):
            for file in files:
                file_list.append(os.path.join(root, file))
    else:
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)):
                file_list.append(os.path.join(path, file))

    return file_list


def convert(file_path: str, out_enc="utf-8") -> None:
    """文件格式转换

    Args:
        file_path (str): 文件路径
        out_enc (str, optional):目标编码，默认为"utf-8".
    """
    try:
        content = codecs.open(file_path, "rb").read()
        src_encoding = chardet.detect(content)["encoding"]

        if src_encoding == out_enc:
            return

        content = content.decode(src_encoding).encode(out_enc)
        codecs.open(file_path, "wb").write(content)

    except Exception as err:
        raise RuntimeWarning from err


def dir_run(in_dir: str, target: list = None) -> dict:
    """
    对目录目录执行转换
    
    Args:
        in_dir (str): 目标目录路径
    """
    if target is None:
        target = []
    target = [".h", ".c", ".cpp", ".hpp", ".bat", ".java", ".md"]

    err_list = []
    succ_list = []
    all_file = get_all_file_path(in_dir)
    for file in all_file:
        filename, suffix = os.path.splitext(file)
        if suffix in target:
            status, info = file_run(file)
            if status:
                succ_list.append(file)
            else:
                err_list.append(info)

    return {"err": err_list, "succ": succ_list}


def file_run(in_file: str) -> tuple:
    """
    对目标单文件执行转换
    
    Args:
        in_file (str): 目标单文件路径
    Returns:
        tuple(bool,Warning):转换成功返回单独 True和None,否返回 False和错误信息.
    """
    try:
        convert(in_file)
    except RuntimeWarning as run_war:
        return False, run_war
    return True, None


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
        if args.target and not args.dir_path:
            parser.error("--t and -dp must be both present.")

    parser = argparse.ArgumentParser(
        prog="toUtf-8",
        description="The encoding is converted to utf-8",
        epilog="Copyright (c) 2023 by zouzhao, All Rights Reserved.")
    parser.add_argument("-v",
                        "--version",
                        action="store_true",
                        help="increase output version")
    parser.add_argument(
        "-t",
        "--target",
        action="append",
        type=list,
        default=[],
        help="target directory,If used, it must be paired with -dp",
    )
    mutex_group = parser.add_mutually_exclusive_group(required=True)
    mutex_group.add_argument("-fp", "--file_path", type=str, help="file path")
    mutex_group.add_argument("-dp", "--dir_path", type=str, help="dir path")

    args = parser.parse_args()
    check_restraint(parser, args)

    return args


def statement(info_d: dict):
    """报表输出

    Args:
        info_d (dict): 运行后信息
    """
    err = info_d["err"]
    succ = info_d["succ"]
    err_num = len(err)
    succ_num = len(succ)
    count = err_num + succ_num
    print("=" * 30 + " start " + "=" * 30)
    print(f"count:{count} err_num:{err_num} succ_num:{succ_num}")
    print("succ:")
    for item in succ_num:
        print(item)
    print("err:")
    for item in err_num:
        print(item)
    print("=" * 30 + " end " + "=" * 30)


if __name__ == "__main__":
    args = get_parameter()
    if args.dir_path:
        info_d = dir_run(args.dir_path)
        statement(info_d)
    else:
        status, info = file_run(args.file_path)
        if status:
            print(f"{args.file_path} successful conversion")
        else:
            print(f"{args.file_path} conversion failure")
