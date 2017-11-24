#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import jsonpickle
import json
import requests


path, name = input().split()
with open("../../golden/" + path + "/" + name + ".html", "r") as file:
    raw_page = file.read()
obj = dict()
obj['action'] = "parse"
obj['raw_page'] = raw_page
r = requests.post('http://127.0.0.1:9876', json=obj)
