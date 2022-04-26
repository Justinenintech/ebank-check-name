# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : mb.py
# Time       ：2022/4/22 9:58 下午
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""
from enum import Enum, unique


@unique
class MBEnum(Enum):
    MB_URL = 'https://online.mbbank.com.vn'
    MB_ROUT_LOGIN = '/retail_web/internetbanking/doLogin'
    MB_ROUT_BALANCE = '/retail-web-accountms/getBalance'
    MB_ROUT_INQUIRYACCOUNTNAME = '/retail_web/transfer/inquiryAccountName'

    FAST_URL = 'http://127.0.0.1:8000'
    FAST_ROUT_BOT_CREATE = '/bot/create'
    FAST_ROUT_TASK_UPDATE = '/task/update'
    USERID = '0374299563'
    TYPE_FAST = 'FAST'
    TYPE_INHOUSE = 'INHOUSE'
    PASSWORD = '3898a0e322ef8d62ccdc4b61ca776df6'
    REFNO = '98c01e0ad0bc034368ae50a16fb26818-'
    DEVICEIDCOMMON = 'le04rfyl-mbib-0000-0000-2022030323312318'
    MSG_MC421 = 'MC421-Giao dịch không thực hiện được do ngân hàng thụ hưởng đang có lỗi!'
    MSG_MC201 = 'MC201-Tài khoản hoặc thẻ thụ hưởng không tồn tại.'
    MSG_201 = '201-Số tài khoản không hợp lệ.'
    MSG_000 = 'OK'
    MSG_400 = '400-Tên không khớp với số tài khoản'
    MSG_404 = '404-Mã ngân hàng không được hỗ trợ'

    STATUS_SUCCESS = 'Success'
    STATUS_FAILURE = 'Failure'
    RUN_DONE = 'Done'
    RUN_READY = 'Ready'
