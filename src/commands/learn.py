#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import subprocess


subprocess.call("""curl -X POST -H "Content-Type: application/json" -d '{"action":"learn"}' 127.0.0.1:9876""", shell=True)
