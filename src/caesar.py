#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time        : 2023/03/23
@Author      : ZouZhao
@Version     : 0.1.0
@Contact     : wszwc3721@163.com
@License     : Copyright (c) 2023 by zouzhao, All Rights Reserved.
@Description : Simple Caesar Cipher [En,De]coder
---Version 0.2.0---
@Time           : 2024/01/22
@Description    : 添加命令行支持
'''

__Author__ = "ZouZhao"
__Version__ = "0.1.0"
__License__ = "Copyright (c) 2023 by zouzhao, All Rights Reserved."
__Name__ = ""
__Description__ = "Simple Caesar Cipher [En,De]coder"

import string
import argparse


def get_version() -> str:
    """获得版本版本信息

    Returns:
        str: 版本版本信息
    """
    print(f"{__Author__} {__Name__} {__Version__} \n{__License__}")


def caesar_cipher(text: str, offset: int, decode: bool = False) -> str:
    """凯撒密码实现，对输入字符串进行编码或解码。

    Args:
        text (str): 需要编码或解码的字符串
        offset (int): 字符偏移量，正数为编码，负数为解码
        decode (bool): 是否解码，默认为False（编码）
    
    return
        str: 编码或解码后的字符串
    """

    if decode:
        offset *= -1

    lower_offset_alphabet = string.ascii_lowercase[
        offset:] + string.ascii_lowercase[:offset]
    lower_translation_table = str.maketrans(string.ascii_lowercase,
                                            lower_offset_alphabet)

    upper_offset_alphabet = string.ascii_uppercase[
        offset:] + string.ascii_uppercase[:offset]
    upper_translation_table = str.maketrans(string.ascii_uppercase,
                                            upper_offset_alphabet)

    converted_string = text.translate(lower_translation_table).translate(
        upper_translation_table)

    return converted_string


def check_offset_range(value: int) -> int:
    """验证值在允许范围内(-25到25)。

    Args:
        value (int): 要验证的整数。

    Raises:
        argparse.ArgumentTypeError: 如果值超出了允许范围抛出。

    Returns:
        int: 范围内的有效整数。
    """
    if value < -25 or value > 25:
        raise argparse.ArgumentTypeError(
            f"{value} is an invalid offset,it should be at -25 to 25")
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
    parser.add_argument(
        '-d',
        '--decode',
        action='store_true',
        dest='decode',
        help='decode ciphertext (offset should equal what was used to encode)',
        default=False)
    parser.add_argument('-o',
                        '--offset',
                        dest='offset',
                        default=13,
                        type=check_offset_range,
                        help='number of characters to shift')
    parser.add_argument('-t', '--text', help='text to encode')

    args = parser.parse_args()

    return args


if __name__ == '__main__':
    args = get_parameter()
    if args.version:
        get_version()
    else:
        print(caesar_cipher(args.text, args.offset, args.decode))
