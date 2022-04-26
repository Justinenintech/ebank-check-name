# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : crud.py
# Time       ：2022/4/18 3:00 下午
# Author     ：Eagle
# version    ：python 3.8
# Description：
"""
from loguru import logger
from sqlmodel import Session, select
from fastapi import Query
from . import models, schemas
from .database import engine
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

session = Session(bind=engine)


async def get_all_bot():
    return session.exec(select(models.Bot)).all()


async def get_bot_by_id(session_id: str):
    return session.exec(select(models.Bot).where(models.Bot.sessionId == session_id)).first()


async def create_bot(bot: schemas.BotCreate):
    statement = models.Bot.from_orm(bot)
    # print('statement', statement)
    session.add(statement)
    session.commit()
    session.refresh(statement)
    return statement


async def update_bot(bot: schemas.BotCreate):
    select_one = select(models.Bot)
    statement = session.exec(select_one)
    up = statement.one()
    # task.status
    # statement = models.Task.from_orm(task)
    up.sessionId = bot.sessionId
    # up.status = task.status
    session.add(up)
    session.commit()
    session.refresh(up)
    return up


async def get_task_by_id(task_order: str):
    return session.exec(select(models.Tasks).where(models.Tasks.orderNo == task_order)).first()


async def get_where_task(status: str, skip: int = 0, limit: int = Query(default=5, lte=10)):
    return session.exec(
        select(models.Tasks).where(models.Tasks.runStatus == status).offset(skip).limit(
            limit)).all()


async def get_where_all(status: str):
    return session.exec(
        select(models.Tasks).where(models.Tasks.runStatus == status)).all()


async def create_task(task: schemas.TasksCreate):
    statement = models.Tasks.from_orm(task)
    # print('statement', statement)
    session.add(statement)
    session.commit()
    session.refresh(statement)
    return statement



async def update_task(task: schemas.TasksUpdate):
    # print('schemas.TasksUpdate',schemas.TasksUpdate)
    select_one = select(models.Tasks).where(models.Tasks.orderNo == task.orderNo)
    statement = session.exec(select_one)
    up = statement.one()
    # task.status
    # statement = models.Task.from_orm(task)
    up.runStatus = task.runStatus
    up.checkStatus = task.checkStatus
    up.remark = task.remark
    # up.status = task.status
    session.add(up)
    session.commit()
    session.refresh(up)
    return up


# Code above omitted 👆

async def delete_task(order):
    statement = select(models.Tasks).where(models.Tasks.orderNo == order)
    results = session.exec(statement)
    task = results.one()
    logger.debug("Task: ", task)

    session.delete(task)
    session.commit()

    logger.debug("Deleted task:", task)

    statement = select(models.Tasks).where(models.Tasks.orderNo == order)
    results = session.exec(statement)
    task = results.first()

    if task is None:
        logger.debug("Tasks executed before 00:00:00 every day, cleared")

# Code below omitted 👇

# async def dd(task: schemas.TasksCreate):
#
#     print('schemas.TasksCreate'.schemas.TasksCreate)
