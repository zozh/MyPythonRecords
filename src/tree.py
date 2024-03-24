#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time        	: 2023/10/21
@Author         : ZouZhao
@Version        : 0.1.0
@Contact        : wszwc3721@163.com
@License		: Copyright (c) 2023 by zouzhao, All Rights Reserved.
@Description	: 打印目录结构树状图
---version 0.2.0---
@Time           : 2024/01/23
@Description    : 添加命令行支持
'''
import os
import argparse

__Author__ = "zouzhao"
__Name__ = "tree"
__Version__ = "0.1.0"
__License__ = "Copyright (c) 2023 by zouzhao, All Rights Reserved."


def get_version() -> str:
    """获得版本版本信息

    Returns:
        str: 版本版本信息
    """
    print(f"{__Author__} {__Name__} {__Version__} \n{__License__}")


def tree(directory: str, exclude_dirs: str = None):
    """遍历并打印目标目录

    Args:
        directory (str): 目标目录
        exclude_dirs (str, optional): 排除目录. 默认为 None.
    """
    if exclude_dirs is None:
        exclude_dirs = []

    def inner(dir_path: str, level: int = 0):
        """遍历并打印目标目录

        Args:
            dir_path (str): 目标目录
            level (int, optional): 缩减. 默认为 0.
        """
        # 遍历目录
        for entry in os.scandir(dir_path):
            if entry.is_dir(
                    follow_symlinks=False) and entry.name not in exclude_dirs:
                indent = "  " * level
                print(f"{indent}{entry.name}/")

                # 递归进入子目录
                inner(entry.path, level + 1)
            elif entry.is_file():
                indent = "  " * level
                print(f"{indent}{entry.name}")

    inner(directory)


def get_parameter() -> argparse.Namespace:
    """
    参数解析

    Returns:
        argparse.Namespace

    """
    parser = argparse.ArgumentParser(
        prog="tree",
        description="Print directory tree.",
        epilog="Copyright (c) 2024 by zouzhao, All Rights Reserved.")
    parser.add_argument("directory",
                        type=str,
                        help="The directory to start from")
    parser.add_argument("-v",
                        "--version",
                        action="store_true",
                        help="increase output version")
    parser.add_argument(
        "--exclude",
        "-e",
        action="append",
        default=[],
        help="Directories to exclude )",
    )

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = get_parameter()
    if args.version:
        get_version()
    else:
        tree(args.directory, exclude_dirs=args.exclude)
