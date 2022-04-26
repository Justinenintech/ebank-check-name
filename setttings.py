# coding=utf-8
import os

_basedir = os.path.abspath(os.path.dirname(__file__))

# 每个银行内部其他银行的银行编码
EBANK_CODE = os.path.join(_basedir, 'ebank_code.yaml')
del os
