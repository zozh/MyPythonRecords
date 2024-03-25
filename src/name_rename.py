#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time        : 2023/09/27 
@Author      : ZouZhao
@Version     : 0.1.0
@Contact     : wszwc3721@163.com
@License     : Copyright (c) 2023 by zouzhao, All Rights Reserved.
@Description : 文件重命名
'''

__Author__ = "ZouZhao"
__Version__ = "0.1.0"
__License__ = "Copyright (c) 2023 by zouzhao, All Rights Reserved."
__Name__ = "NameRename"
__Description__ = "文件重命名"

import os
import re
import sys
import json
import time
import argparse
from random import randint


class Utility:
    """工具类
    """

    @staticmethod
    def extraction_path(str_one: str, str_two: str) -> tuple:
        """提取两个路径的共有路径
        eg:
        str_one="asfa/sd/1.txt"
        str_two="asfa/1.txt"
        return "asfa/"
        
        Args:
            str_one (str): 路径1
            str_two (str): 路径2

        Returns:
            tuple: 共有路径
        """
        sub = os.path.commonpath([str_one, str_two])
        str_one = str_one.replace(sub, "")
        str_two = str_two.replace(sub, "")
        return (sub, str_one, str_two)

    @staticmethod
    def get_all_file_path(directory: str, is_recursion: bool = False) -> list:
        """获得目录下所有文件的路径

        Args:
            directory (str): 目标目录地址
            is_recursion (bool): 是否递归子目录，默认 False

        Returns:
            list: 所有文件路径的列表
        """
        out = []
        if is_recursion:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    out.append(os.path.join(root, file))
        else:
            for file in os.listdir(directory):
                file_path = os.path.join(directory, file)
                if os.path.isfile(file_path):
                    out.append(file_path)
        return out

    @staticmethod
    def get_all_directory_path(directory: str,
                               is_recursion: bool = False) -> list:
        """获得目录下所有目录的路径


        Args:
            directory (str): 目标目录地址
            is_recursion (bool): 是否递归子目录，默认 False

        Returns:
            list: 所有目录路径的列表
        """
        out = []
        if is_recursion:
            for root, dirs, files in os.walk(directory):
                for _dir in dirs:
                    out.append(os.path.join(root, _dir))
        else:
            for _dir in os.listdir(directory):
                _dir_path = os.path.join(directory, _dir)
                if os.path.isdir(_dir_path):
                    out.append(_dir_path)
        return out

    @staticmethod
    def chinese_and_English_with_Spaces(content: str) -> str:
        """中英文之间添加空格

        Args:
            content (str): 文本内容
        Returns:
            str: 处理后文本
        """
        content = re.sub(r"([\u4e00-\u9fa5]+)([\da-zA-Z]+)", r"\1 \2", content)
        content = re.sub(r"([\da-zA-Z]+)([\u4e00-\u9fa5]+)", r"\1 \2", content)
        return content

    @staticmethod
    def merge_dicts(*dicts: tuple) -> dict:
        """字典合并

        Raises:
            ValueError: key 冲突时抛出

        Returns:
            dict: 合并后的字典
        """
        result = {}
        for d in dicts:
            for key, value in d.items():
                if key in result:
                    raise ValueError(f"Key '{key}' conflict")
                result[key] = value
        return result

    @staticmethod
    def ignore_file(src: list, ignore_list: list) -> list:
        """
        对文件或目录路径的过滤，实现忽略效果
        输入为包含文件路径的列表，根据 ignore_list 对其进行过滤
        过滤规则：
            忽略子目录中的内容：
            - 如果想忽略某个目录下的所有内容，但不包括该目录本身，可以使用 dir_name/ 的形式。
                eg:
                src=["MyNote\\.obsn\\plns","MyNote\\dian\\plns"]
                ignore_list=[".obsn\\"]
                return ["MyNote\\dian\\plns"]
        Args:
            src (list): 待过滤的字符串列表。
            ignore_list (list): 过滤规则，字符串列表。

        Returns:
            list: 过滤后的字符串列表。
        """
        # 根据第一个列表过滤第二个列表
        filter_data = [x for x in src if all(y not in x for y in ignore_list)]
        return filter_data


def rule_match(path: str, rule_d: dict) -> dict:
    """ 规则匹配
        对目标路径进行规则匹配，返回符合规则的路径
    Args:
        path (str): 目标路径

    Returns:
        dict:预处理的结果
    """
    out_execute_dict = {}
    for subpath in path:
        old_path = subpath
        dir_name = os.path.dirname(subpath)
        new_name = os.path.basename(subpath)
        for key, value in rule_d["RULES"].items():
            new_name = new_name.replace(key, value)

        for key, value in rule_d["RE_RULES"].items():
            new_name = re.sub(key, value, new_name)

        if rule_d["IS_CHINESE_AND_ENGLISH_WITH_SPACES"]:
            new_name = Utility.chinese_and_English_with_Spaces(new_name)

        new_path = os.path.join(dir_name, new_name)
        if old_path != new_path:
            out_execute_dict[old_path] = new_path

    return out_execute_dict


def execute_rename(execute_dict: dict) -> None:
    """执行重命名

    Args:
        execute_dict (dict): 执行表， key 为旧值， value 为新值

    Returns:
        NoReturn
    """
    for old_path, new_path in execute_dict.items():
        try:
            os.rename(old_path, new_path)
            # log_obj.succeed(old_path, new_path)
        except IOError as err:
            print(err)


def preview(execute_dict: dict) -> None:
    """操作预览
    小于 128 ，输出在终端，否输出在文件

    Args:
        data (dict): 要执行的数据和预期结果
    """
    if len(execute_dict) < 128:
        for old_path, new_path in execute_dict.items():
            sub_path, old_path, new_path = Utility.extraction_path(
                old_path, new_path)
            print(f"preview sub:{sub_path} {old_path} -> {new_path}")
    else:
        now_time = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
        filename = f"{now_time}-{randint(1 , 1000)}-preview"
        while os.path.exists(filename):
            filename = f"{now_time}-{randint(1 , 1000)}-preview"
        with open(filename, "w", encoding="utf-8") as file_obj:
            for old_path, new_path in execute_dict.items():
                sub_path, old_path, new_path = Utility.extraction_path(
                    old_path, new_path)
                file_obj.write(
                    f"preview sub:{sub_path} {old_path} -> {new_path}")
        print(f"内容较多，已在同目录下生产预览文件 {filename}")


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
        """检查约束，-t 参数可选，但如果使用必须和 -dp 搭配

        Args:
            parser (argparse.ArgumentParser)
            args (argparse.Namespace)
        Returns:
            NoReturn
        """
        if args.version:
            return

        if args.rules:
            if not check_file(args.rules, ".json"):
                parser.error("rules file illegality.")

    parser = argparse.ArgumentParser(prog=f"{__Name__}",
                                     description=f"{__Description__}",
                                     epilog=f"{__License__}")
    parser.add_argument("-v",
                        "--version",
                        action="store_true",
                        help="increase output version")
    parser.add_argument("-r", "--rules", type=str, help="rules file path")
    parser.add_argument("-p", "--path", type=str, help="target path")

    args = parser.parse_args()
    check_restraint(parser, args)

    return args


def parser_rules(path: str) -> tuple:
    """解析规则文件

    Args:
        path (str): 文件路径

    Returns:
        tuple(bool,dict): 正确 True,否 False
    """
    rules_d = read_json(path)
    for item in [
            "RE_RULES", "RULES", "IS_CHINESE_AND_ENGLISH_WITH_SPACES",
            "IS_RECURSION", "LOG_PATH", "MATCH_MODE", "IGNORE_LIST"
    ]:
        if rules_d.get(item, None) is None:
            return False, f"Missing {item} attribute"
    return True, rules_d


def read_json(path: str) -> dict:
    """读取 json 文件
    Args:
        path (str): 文件路径

    Raises:
        e: Exception

    Returns:
        dict: 解析后的字典
    """
    with open(path, 'r', encoding="utf-8") as file_obj:
        content = file_obj.read()
        try:
            return json.loads(content)
        except Exception as err:
            raise RuntimeError(f"{path} 加载异常\n{err}") from err


def get_paths(directory: str, rules_d: dict) -> list:
    """根据规则从目标路径获得对应路径

    Args:
        directory (str): 目标路径
        rules_d (dict): 规则

    Raises:
        ValueError: 值错误抛出

    Returns:
        list: 包含路径的列表
    """
    match_mode_func_map = {
        1:
        Utility.get_all_file_path,
        2:
        Utility.get_all_directory_path,
        3:
        lambda dir, is_recursion: Utility.get_all_file_path(dir, is_recursion)
        + Utility.get_all_directory_path(dir, is_recursion),
    }
    if rules_d["MATCH_MODE"] not in match_mode_func_map:
        raise ValueError("请在1(文件),2(目录),3(文件＋目录)中选择")
    return match_mode_func_map[rules_d["MATCH_MODE"]](directory,
                                                      rules_d["IS_RECURSION"])


def param_map_fun(args: argparse.Namespace) -> tuple:
    """参数映射处理

    Args:
        args (argparse.Namespace)

    Returns:
        tuple(dict,Log)
    """
    if args.version:
        get_version()
        sys.exit()

    if args.rules and not args.path:
        status, rules_d = parser_rules(args.rules)
        if status:
            print("配置文件有效")
        else:
            print("无效的配置文件")
        sys.exit()

    if args.rules and args.path:
        status, rules_d = parser_rules(args.rules)
        if status:
            directory = args.path
            print("1", rules_d)

            all_path = get_paths(directory, rules_d)
            all_path = Utility.ignore_file(all_path, rules_d["IGNORE_LIST"])

            execute_dict = rule_match(all_path, rules_d)
            if not execute_dict:
                print("没有符合规则的路径")
                sys.exit()

            preview(execute_dict)
            return execute_dict
        else:
            print("无效的配置文件")
            sys.exit()


def execute_operation(execute_dict: dict, ) -> None:
    """是否执行

    Args:
        execute_dict (dict): 预处理结果
    """
    print("是否继续,Y继续,N结束")
    while True:
        in_operate = input().upper()
        if in_operate == "Y":
            execute_rename(execute_dict)
            break
        elif in_operate == "N":
            break
        else:
            print("输入不合法,请输入Y(继续),N(结束)")


if __name__ == "__main__":
    args = get_parameter()
    execute_dict = param_map_fun(args)
    execute_operation(execute_dict)
