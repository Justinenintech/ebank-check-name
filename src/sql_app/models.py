# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : models.py
# Time       ：2022/4/18 11:28 上午
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""
from typing import Optional

from sqlmodel import SQLModel, Field


class Bot(SQLModel, table=True):
    sessionId: Optional[str] = Field(default=None, primary_key=True)


class Tasks(SQLModel, table=True):
    orderNo: Optional[str] = Field(default=None, primary_key=True)  # 唯一标识--
    payeeBankCode: str  # 收款银行编码
    runStatus: Optional[str] = Field(default='Ready')  # 运行状态，Ready:待检测，Done:已完成
    payeeBankCard: str  # 绑定的银行卡号
    payeeBankName: str  # 绑定的银行姓名
    checkStatus: Optional[str] = Field(default=None)  # 检测状态：Success:成功，Failure:银行信息不正确
    remark: Optional[str] = Field(default=None)  # 备注信息
