# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : schemas.py
# Time       ：2022/4/18 2:53 下午
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""
from typing import Optional

from sqlmodel import SQLModel, Field


class BotCreate(SQLModel):
    sessionId: Optional[str] = Field(description='后续接口需要用到的认证信息')


class BotRead(BotCreate):
    pass


class BotUpdate(SQLModel):
    sessionId: Optional[str] = Field(description='只存在一个sessionId，因此会更新之前的session')


class TasksCreate(SQLModel):
    orderNo: Optional[str] = Field(description='唯一标识，任务单号，必传')
    payeeBankCode: Optional[str] = Field(description='绑定银行的编码，例如：VIB，必传')
    runStatus: Optional[str] = Field(description='待执行检测状态，Ready:待检测，Done:已完成,必传"Ready"')
    payeeBankCard: Optional[str] = Field(description='绑定的银行账号,必传')
    payeeBankName: Optional[str] = Field(description='会员绑定的银行账号对应的姓名，必传')
    checkStatus: Optional[str] = Field(default=None,
                                       description='银行卡校验，检测结果，Success:校验通过，Failure:校验不通过，参数值允许为空')
    remark: Optional[str] = Field(default=None, description='备注信息，参数值允许为空')


class TasksSearch(SQLModel):
    orderNo: Optional[str] = Field(description='唯一标识，查询任务单号，必传')


class TasksUpdate(SQLModel):
    orderNo: Optional[str] = Field(description='唯一标识，任务单号，更新检测数据')
    runStatus: str
    checkStatus: str
    remark: str


class TasksDelete(SQLModel):
    orderNo: Optional[str] = Field(description='每天00:00:00 删除Done的数据')
