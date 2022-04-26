# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : tasks.py
# Time       ：2022/4/18 2:59 下午
# Author     ：Eagle
# version    ：python 3.10
# Description：
"""
from fastapi import FastAPI
from loguru import logger
from starlette import status
from starlette.responses import JSONResponse

from . import crud, schemas
from .create_db import create_db_and_tables

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    create_db_and_tables()


@app.post("/bot/create", response_model=schemas.BotCreate, status_code=status.HTTP_200_OK,
          response_class=JSONResponse)
async def fast_create_bot(bot: schemas.BotCreate):
    bot_id = await crud.get_all_bot()
    logger.debug('bot_id:{}'.format(len(bot_id)))
    if len(bot_id).__eq__(0):
        result = await crud.create_bot(bot)
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"code": '0000', "data": result.json(),
                                     "msg": 'Bot successfully inserted into cache'})
    elif len(bot_id).__eq__(1):
        bot_id = await crud.get_bot_by_id(bot.sessionId)
        logger.debug('bot_id:{}'.format(bot_id))
        if bot_id is None:
            result = await crud.update_bot(bot)
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content={"code": '0000', "data": result.json(),
                                         "msg": 'Task successfully updated into cache'})


@app.post("/task/create", response_model=schemas.TasksCreate, status_code=status.HTTP_200_OK,
          response_class=JSONResponse)
async def fast_create_task(task: schemas.TasksCreate):
    task_id = await crud.get_task_by_id(task.orderNo)
    if task_id:
        # error_str = traceback.format_exc()
        res = {"code": '4000', "data": task_id.json(),
               "msg": 'task already registered'
               }
        # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=res)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=res)
    result = await crud.create_task(task)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"code": '0000', "data": result.json(),
                                 "msg": 'Task successfully inserted into cache'})


#
@app.post("/task/update", response_model=schemas.TasksCreate, status_code=status.HTTP_200_OK,
          response_class=JSONResponse)
async def fast_update_task(task: schemas.TasksUpdate):
    task_id = await crud.get_task_by_id(task.orderNo)
    if task_id is None:
        # error_str = traceback.format_exc()
        res = {"code": '4004', "data": task_id,
               "msg": 'task not found'
               }
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res)
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=res)
    result = await crud.update_task(task)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"code": '0000', "data": result.json(),
                                 "msg": 'Task successfully updated into cache'})


@app.post("/task/search", status_code=status.HTTP_200_OK,
          response_class=JSONResponse)
async def fast_read_task(task: schemas.TasksSearch):
    result = await crud.get_task_by_id(task.orderNo)
    print('result', result)
    if result is None:
        # error_str = traceback.format_exc()
        res = {"code": '4004', "data": 'None', "msg": 'Task not found'}
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res)
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=res)
    return JSONResponse(
        {"code": '0000', "data": result.json(),
         "msg": 'Records were successfully queried'})


# @app.post("/task/delete", status_code=status.HTTP_200_OK,
#           response_class=JSONResponse)
# async def fast_delete_task(task: schemas.TasksDelete):
#     result = await crud.delete_task(task.runStatus)
#     print('result', result)
#     if result is None:
#         # error_str = traceback.format_exc()
#         res = {"code": '4004', "data": 'None', "msg": 'Task not found'}
#         # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res)
#         return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
#                             content=res)
#     return JSONResponse(
#         {"code": '0000', "data": result[0].json(),
#          "msg": 'Records were successfully queried'})
