#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import jsonpickle
import json
import requests


path, name = input().split()
with open("../../golden/" + path + "/" + name + "_markup.json", "r") as file:
    markup = jsonpickle.decode(file.read())
obj = dict()
obj['action'] = "add"
obj['markup'] = markup
r = requests.post('http://127.0.0.1:9876', json=obj)
