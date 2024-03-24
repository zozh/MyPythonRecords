# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
@Time           :   2023/09/18
@Author         :   zouzhao
@Version        :   0.1.0
@Contact        :   wszwc3721@163.com
@License        :   Copyright (c) 2023 by zouzhao, All Rights Reserved.
@Description    :   实现文本转 csv
文本要求以空行分割块，块内以键值对形式存在，第一行为键，其余为值
eg:
    in:
        Redis 的内存淘汰机制有哪些？
        Redis 的内存淘汰机制包括：LRU（最近最少使用）、LFU（最不经常使用）和随机。

        Redis 的连接池是什么？
        Redis 的连接池是用于管理 Redis 客户端连接的池子。
    out:
        "Redis 的内存淘汰机制有哪些？","Redis 的内存淘汰机制包括：LRU（最近最少使用）、LFU（最不经常使用）和随机。"
        "Redis 的连接池是什么？","Redis 的连接池是用于管理 Redis 客户端连接的池子。"

---Version 0.2.0---
@Time           : 2024/01/22
@Description    : 添加命令行支持
"""

import csv
import sys
import argparse

__Author__ = "zouzhao"
__Name__ = "txtToCsv"
__Version__ = "0.1.0"
__License__ = "Copyright (c) 2023 by zouzhao, All Rights Reserved."


def get_version() -> str:
    """获得版本版本信息

    Returns:
        str: 版本版本信息
    """
    print(f"{__Author__} {__Name__} {__Version__} \n{__License__}")


def parse_blocks(file_path: str) -> list:
    """解析文本，文本格式使用换行分割块

    Args:
        file_path (str): 文件路径

    Returns:
        list: 行组成的列表
    """
    blocks = []
    current_block = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line:
                # 如果不是空行，则将该行添加到当前块中
                current_block.append(line)
            elif current_block:
                # 如果是空行，并且当前块不为空，则将当前块添加到块列表中
                blocks.append(current_block)
                current_block = []

    # 添加最后一个块（如果存在）
    if current_block:
        blocks.append(current_block)

    return blocks


def get_parameter() -> argparse.Namespace:
    """参数解析

    Returns:
        argparse.Namespace
    """
    parser = argparse.ArgumentParser(prog='txtToCsv',
                                     description='txt to csv.',
                                     epilog='Copyright(r), 2023')
    parser.add_argument("-v",
                        "--version",
                        action="store_true",
                        help="increase output version")
    parser.add_argument("-ip", "--in_path", help="input file path")
    parser.add_argument("-op", "--ont_path", help="out file path")

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    csv_params = {
        "delimiter": ",",
        "quotechar": '"',
        "quoting": csv.QUOTE_ALL,
    }

    args = get_parameter()

    if args.version:
        get_version()
        sys.exit(0)

    ont_path = ''
    if not args.ont_path:
        ont_path = args.in_path + ".csv"

    parsed_blocks = parse_blocks(args.in_path)
    data = {}
    for block in parsed_blocks:
        data[block[0]] = "".join(block[1:])

    with open(ont_path, "w", encoding="utf-8") as file_obj:
        writer = csv.writer(file_obj, **csv_params)
        for row in data.items():
            writer.writerow(row)
