# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : mb.py
# Time       ：2022/4/22 9:56 下午
# Author     ：Eagle
# version    ：python 3.10
# Description：
"""
import asyncio
import json
import time
from loguru import logger

from src.base.async_http import MySession
from src.base.tools import Tools
from src.enum.mb import MBEnum
from src.sql_app.crud import get_all_bot, get_where_all, delete_task


class Tasks:
    def __init__(self):
        self._t = Tools()

    @staticmethod
    def get_time(f):
        def inner(*arg, **kwargs):
            s_time = time.time()
            res = f(*arg, **kwargs)
            e_time = time.time()
            logger.debug("耗时：{}秒".format(e_time - s_time))
            return res

        return inner

    async def login(self, captcha):
        """
        登录方法，并保存唯一有效的sessionID到缓存
        :param captcha: 手动输入验证码（需要在设备实际打开网银页面）
        :return:
        """
        login_body = {
            "userId": MBEnum.USERID.value,
            "password": MBEnum.PASSWORD.value,
            "captcha": captcha,
            "sessionId": 'null',
            "refNo": MBEnum.REFNO.value + self._t.generate_requests_time(),
            "deviceIdCommon": MBEnum.DEVICEIDCOMMON.value
        }
        up = {'captcha': captcha}
        login_body.update(up)

        res = await MySession.post(MBEnum.MB_URL.value + MBEnum.MB_ROUT_LOGIN.value,
                                   data=login_body)
        # logger.debug('获取响应：{}'.format(res))
        if res['result']['message'].__eq__('OK'):
            add_data = {'sessionId': res['sessionId']}
            # logger.debug('add_data：{}'.format(add_data))
            cache = await MySession.post(MBEnum.FAST_URL.value + MBEnum.FAST_ROUT_BOT_CREATE.value,
                                         data=add_data)
            # logger.debug('任务成功写入到缓存：{}'.format(cache))

    async def get_balance(self):
        """
        请求余额的函数方法，用于保持会话有效性
        :return:
        """
        bot_res = await get_all_bot()
        session_id = json.loads(bot_res[0].json())['sessionId']
        # logger.debug("当前登录有效session：{}".format(session_id))
        # logger.debug("当前登录有效session：{}".format(type(session_id)))

        balance_body = {
            "sessionId": session_id,
            "refNo": MBEnum.USERID.value + '-' + self._t.generate_requests_time(),
            "deviceIdCommon": MBEnum.DEVICEIDCOMMON.value
        }
        res = await MySession.post(MBEnum.MB_URL.value + MBEnum.MB_ROUT_BALANCE.value,
                                   data=balance_body)
        # logger.debug('获取响应：{}'.format(res))

    async def inquiry_account_name(self, semaphore, orderNo, payeeBankCode, payeeBankCard,
                                   payeeBankName):
        """
        校验银行卡的函数方法
        :param semaphore: 并发控制
        :param orderNo: 任务单号
        :param payeeBankCode: 待校验的收款银行编号
        :param payeeBankCard: 待校验的收款银行账号
        :param payeeBankName: 待校验的收款银行姓名
        :return:
        """
        # start_time = time.time()
        bot_res = await get_all_bot()
        session_id = json.loads(bot_res[0].json())['sessionId']
        # logger.debug("当前登录有效session：{}".format(session_id))
        # logger.debug("当前登录有效session：{}".format(type(session_id)))
        payee_code_short = self._t.get_bank_code_params('ebank', 'MBBank', payeeBankCode)
        check_body = {
            "creditAccount": payeeBankCard,
            "creditAccountType": "ACCOUNT",
            "bankCode": payee_code_short,
            "debitAccount": MBEnum.USERID.value,
            "type": MBEnum.TYPE_FAST.value,
            "remark": "",
            "sessionId": session_id,
            "refNo": MBEnum.USERID.value + '-' + self._t.generate_requests_time(),
            "deviceIdCommon": MBEnum.DEVICEIDCOMMON.value
        }
        async with semaphore:
            if payee_code_short is None or payee_code_short.__eq__('None'):
                up_task = {'orderNo': orderNo, 'runStatus': MBEnum.RUN_DONE.value,
                           'checkStatus': MBEnum.STATUS_SUCCESS.value,
                           'remark': MBEnum.MSG_404.value}
                logger.debug('up_task:{}'.format(up_task))
                cache = await MySession.post(
                    MBEnum.FAST_URL.value + MBEnum.FAST_ROUT_TASK_UPDATE.value,
                    data=up_task)
                return logger.debug('任务成功更新到缓存：{}'.format(cache))
            if payee_code_short.__eq__('970422'):
                up = {'type': MBEnum.TYPE_INHOUSE.value}
                check_body.update(up)
                # logger.debug("请求参数：{}".format(check_body))
                res = await MySession.post(
                    MBEnum.MB_URL.value + MBEnum.MB_ROUT_INQUIRYACCOUNTNAME.value,
                    data=check_body)
            else:
                # logger.debug("请求参数：{}".format(check_body))

                res = await MySession.post(
                    MBEnum.MB_URL.value + MBEnum.MB_ROUT_INQUIRYACCOUNTNAME.value,
                    data=check_body)

            logger.debug('获取响应：{}'.format(res))
            if res['benName'] is None and res['result']['responseCode'].__eq__('MC201'):
                logger.debug("银行卡校验不通过")
                up_task = {'orderNo': orderNo, 'runStatus': MBEnum.RUN_DONE.value,
                           'checkStatus': MBEnum.STATUS_FAILURE.value,
                           'remark': MBEnum.MSG_MC201.value}
                logger.debug('up_task:{}'.format(up_task))
                cache = await MySession.post(
                    MBEnum.FAST_URL.value + MBEnum.FAST_ROUT_TASK_UPDATE.value,
                    data=up_task)
                return logger.debug('任务成功更新到缓存：{}'.format(cache))
            elif res['result']['responseCode'].__eq__('00') and payeeBankName.__eq__(res['benName']):
                logger.debug("银行卡校验通过")
                up_task = {'orderNo': orderNo, 'runStatus': MBEnum.RUN_DONE.value,
                           'checkStatus': MBEnum.STATUS_SUCCESS.value,
                           'remark': MBEnum.MSG_000.value}
                logger.debug('up_task:{}'.format(up_task))
                cache = await MySession.post(
                    MBEnum.FAST_URL.value + MBEnum.FAST_ROUT_TASK_UPDATE.value,
                    data=up_task)
                return logger.debug('任务成功更新到缓存：{}'.format(cache))
            elif res['result']['responseCode'].__eq__('00') and payeeBankName != res['benName']:
                # logger.debug("银行卡姓名校验不通过")
                up_task = {'orderNo': orderNo, 'runStatus': MBEnum.RUN_DONE.value,
                           'checkStatus': MBEnum.STATUS_FAILURE.value,
                           'remark': MBEnum.MSG_400.value}
                logger.debug('up_task:{}'.format(up_task))
                cache = await MySession.post(
                    MBEnum.FAST_URL.value + MBEnum.FAST_ROUT_TASK_UPDATE.value,
                    data=up_task)
                return logger.debug('任务成功更新到缓存：{}'.format(cache))
            elif res['benName'] is None and res['result']['responseCode'].__eq__('201'):
                # logger.debug("银行卡校验不通过")
                up_task = {'orderNo': orderNo, 'runStatus': MBEnum.RUN_DONE.value,
                           'checkStatus': MBEnum.STATUS_FAILURE.value,
                           'remark': MBEnum.MSG_201.value}
                logger.debug('up_task:{}'.format(up_task))
                cache = await MySession.post(
                    MBEnum.FAST_URL.value + MBEnum.FAST_ROUT_TASK_UPDATE.value,
                    data=up_task)
                return logger.debug('任务成功更新到缓存：{}'.format(cache))
            elif res['benName'] is None and res['result']['responseCode'].__eq__('MC421'):
                # logger.debug("银行卡校验不通过")
                up_task = {'orderNo': orderNo, 'runStatus': MBEnum.RUN_DONE.value,
                           'checkStatus': MBEnum.STATUS_FAILURE.value,
                           'remark': MBEnum.MSG_MC421.value}
                logger.debug('up_task:{}'.format(up_task))
                cache = await MySession.post(
                    MBEnum.FAST_URL.value + MBEnum.FAST_ROUT_TASK_UPDATE.value,
                    data=up_task)
                return logger.debug('任务成功更新到缓存：{}'.format(cache))

        # end_time = time.time()
        # logger.debug("耗时：{}秒".format(end_time - start_time))

    async def run(self):
        """
        程序入口，没有数据时，请求余额接口保持会话，有数据时去校验银行卡（每2秒运行一次）
        :return:
        """
        tasks = []
        res = await get_where_all(MBEnum.RUN_READY.value)
        # logger.debug("当前待检测待数据：{}".format(res))
        datas = [json.loads(_.json()) for _ in res]
        # logger.debug("处理后的当前待检测待数据：{}".format(datas))
        # logger.debug('datas', datas)
        semaphore = asyncio.Semaphore(len(datas))
        if len(datas).__eq__(0):
            logger.debug("当前待检测数量：{}".format(len(datas)))
        else:
            logger.debug("当前待检测数量：{}".format(len(datas)))
            for _ in datas:
                task = asyncio.create_task(
                    self.inquiry_account_name(semaphore, _['orderNo'], _['payeeBankCode'],
                                              _['payeeBankCard'], _['payeeBankName']))
                tasks.append(task)
            results = await asyncio.gather(*tasks)
            return results

    async def task_delete(self, semaphore, orderNo):
        """
        并发删除数据
        :param semaphore: 并发控制
        :param orderNo: 要删除数据的ID
        :return:
        """
        async with semaphore:
            await delete_task(orderNo)

    async def del_done_task(self):
        """
        每天00:00:00 清除已完成的数据
        :return:
        """
        tasks = []
        search = await get_where_all(MBEnum.RUN_DONE.value)
        datas = [json.loads(_.json()) for _ in search]
        semaphore = asyncio.Semaphore(len(datas))
        if len(search).__eq__(0):
            logger.debug("不存在需要删除的数据！")
        else:
            # logger.debug('search:{}'.format(search))
            for _ in datas:
                task = asyncio.create_task(self.task_delete(semaphore, _['orderNo']))
                tasks.append(task)
            results = await asyncio.gather(*tasks)
            return results
            # res = await delete_task(MBEnum.RUN_DONE.value)
            # logger.debug("删除数据：{}".format(res))
