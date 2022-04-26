# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : database.py
# Time       ：2022/4/18 11:25 上午
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""
import os

from sqlmodel import create_engine

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

conn_str = f"sqlite:///" + os.path.join(BASE_DIR, 'check_bank_name.db')
# print(conn_str)
#
engine = create_engine(conn_str, echo=True)
