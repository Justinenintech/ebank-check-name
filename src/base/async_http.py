# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : async_http.py
# Time       ：2022/4/18 12:26 下午
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""
import json

import aiohttp


class MySession:
    _session = None

    @classmethod
    def session(cls):
        _headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=utf-8',
            'Authorization': 'Basic QURNSU46QURNSU4='
        }
        if not cls._session:
            conn = aiohttp.TCPConnector(verify_ssl=False)
            cls._session = aiohttp.ClientSession(headers=_headers,connector=conn)
        return cls._session

    @classmethod
    def close(cls):
        return cls._session.close()

    @classmethod
    def convert_data(cls, data):
        """
        请求数据类型转化
        :param data: 数据
        """
        param = None
        if isinstance(data, str):
            param = data
        elif isinstance(data, dict):
            param = json.dumps(data).encode('utf-8')
        elif isinstance(data, object):
            param = json.dumps(data.__dict__).encode('utf-8')
        # .info("请求参数-{} ", param)
        return param

    @staticmethod
    async def post(url, data):
        param = MySession.convert_data(data)
        r = await MySession.session().post(url, data=param)
        data = await r.read()
        # print('data',data)
        json_body = json.loads(data)
        # print('请求相应：', json_body)
        return json_body

    @staticmethod
    async def get(url, **kwargs):
        param = MySession.convert_data(kwargs)
        async with MySession.session().get(url, data=param) as r:
            data = await r.read()
            # print('data',data)
            json_body = json.loads(data)
            # print('请求相应：', json_body)
            return json_body

    @staticmethod
    async def put(url, **kwargs):
        """

        :param url:
        :param kwargs:
        :return:
        """
        param = MySession.convert_data(kwargs)
        async with MySession.session().put(url, data=param) as r:
            data = await r.read()
            json_body = json.loads(data)
            # print('请求相应：', json_body)
            return json_body

    @staticmethod
    async def close_session():
        await MySession.close()
