#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 19:46:44 2021

@author: djoghurt
"""
import time
import json

data = {}
data["name"]="testPrinter"
for i in range(10):
    data["value"] = i
    json_data = json.dumps(data, indent = 4)
    print("jkljl<data>", flush=True)
    print(json_data, flush=True)
    print("</data>lkj", flush=True)
    print("", flush=True)
    print("test"+str(i), flush=True)
    time.sleep(3)