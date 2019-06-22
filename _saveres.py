#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# @Author : Jingze Lu
# @Created Time : 2019-06-21 22:01:10
# @Description : 
"""

def save_res(path, target):
    with open(path, 'w') as f:
        f.write(str(target))
