#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time        : 2023/03/23
@Author      : ZouZhao
@Version     : 0.1.0
@Contact     : wszwc3721@163.com
@License     : Copyright (c) 2023 by zouzhao, All Rights Reserved.
@Description : Generates Fibonacci of the specified length
---Version 0.2.0---
@Time           : 2024/01/22
@Description    : 添加命令行支持
'''

__Author__ = "ZouZhao"
__Version__ = "0.1.0"
__License__ = "Copyright (c) 2023 by zouzhao, All Rights Reserved."
__Name__ = "Fibonacci"
__Description__ = "Generates Fibonacci of the specified length"

import argparse
from typing import List


def get_version() -> str:
    """获得版本版本信息

    Returns:
        str: 版本版本信息
    """
    print(f"{__Author__} {__Name__} {__Version__} \n{__License__}")


def generate_fibonacci_numbers(num: int) -> List[int]:
    """生成斐波那契数列

    Args:
        num (int): 斐波那契数列长度

    Returns:
        List[int]: 斐波那契数列
    """
    series = [1]

    while len(series) < num:
        if len(series) == 1:
            series.append(1)
        else:
            series.append(series[-1] + series[-2])

    for i, season in enumerate(series):
        series[i] = str(season)

    return (', '.join(series))


def check_num(value: int) -> int:
    """验证值在允许范围内,要求大于0。

    Args:
        value (int): 要验证的整数。

    Raises:
        argparse.ArgumentTypeError: 如果值超出了允许范围抛出。

    Returns:
        int: 范围内的有效整数。
    """
    value = int(value)
    if value <= 0:
        raise argparse.ArgumentTypeError(
            f"{value} is an invalid value,must be greater than 0")
    return value


def get_parameter() -> argparse.Namespace:
    """
    参数解析

    Returns:
        argparse.Namespace

    """

    parser = argparse.ArgumentParser(prog=f"{__Name__}",
                                     description=f"{__Description__}",
                                     epilog=f"{__License__}")
    parser.add_argument("-v",
                        "--version",
                        action="store_true",
                        help="increase output version")
    parser.add_argument("-n",
                        "--num",
                        type=check_num,
                        help="input fibonacci num")

    args = parser.parse_args()

    return args


if __name__ == '__main__':
    args = get_parameter()
    if args.version:
        get_version()
    else:
        print(generate_fibonacci_numbers(args.num))
