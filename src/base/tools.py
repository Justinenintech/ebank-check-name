# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : tools.py
# Time       ：2022/4/18 12:27 下午
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""
import os
import socket
import tkinter
from datetime import datetime, timezone, timedelta

import yaml

from setttings import EBANK_CODE


class Tools(object):
    def __init__(self):
        pass

    @staticmethod
    def get_ip():
        s = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip

    @staticmethod
    def get_time_now(formats: str) -> str:
        """
        获取当前日期 %Y-%m-%d %H:%M:%S
        :return: 2021-04-28 15:39:40 or 2021-04-29 ..
        """
        return (datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(
            timezone(timedelta(hours=8)))).strftime(
            formats)

    @staticmethod
    def screen_size():
        tk = tkinter.Tk()
        width = tk.winfo_screenwidth()
        height = tk.winfo_screenheight()
        tk.quit()
        return width, height

    @staticmethod
    def my_listener(event):
        if event.exception:
            print('The job crashed :(')
        else:
            print('The job worked :)')
            print("")

    def generate_requests_time(self) -> str:
        """
        生成请求时间
        :return: 2021-05-13 13:34:49.938
        """
        return self.get_time_now('%Y%m%d%H%M%S%f')[:-4]

    def get_yaml(self):
        """
        从data.yaml文件获取数据
        :return:
        """
        test_data_file = os.path.abspath(EBANK_CODE)
        file = open(test_data_file, 'r', encoding='utf-8')
        data_yaml = yaml.load(file, Loader=yaml.FullLoader)
        file.close()
        return data_yaml

    def get_bank_code_params(self, yaml_type: str, payer_code: str, payee_code: str) -> str:
        """
        从yaml文件中读取，根据转账人银行编码，获取收款人银行编码（简称）
        :param yaml_type: yaml文件的code标识
        :param payer_code: 转账人银行编码或者收款人银行编码
        :param payee_code: 收款人银行编码或者收款卡号
        :return:
        """
        # 将接收到的驱动启动银行编码，转化为大写，再去yaml文件中读取
        # print('transfer_code.upper()', transfer_code.upper())
        _yaml = self.get_yaml()
        params = _yaml[yaml_type].get(payer_code.upper())
        res = params.get(payee_code.upper())
        return res
