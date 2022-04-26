# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : create_db.py
# Time       ：2022/4/18 11:27 上午
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""
from sqlmodel import SQLModel

from .database import engine


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
