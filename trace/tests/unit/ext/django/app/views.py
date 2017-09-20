# Copyright 2017, OpenCensus Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.http import HttpResponse
from django.shortcuts import render

from .forms import HelloForm

from opencensus.trace import config_integration

import mysql.connector
import psycopg2

import time
import os
import sys

sys.path.insert(0, os.path.abspath(__file__+"/../../../.."))
from ext import config


INTEGRATIONS = ['mysql', 'postgresql']

config_integration.trace_integrations(INTEGRATIONS)


def home(request):
    time.sleep(1)
    return render(request, 'home.html')


def greetings(request):
    time.sleep(1)
    if request.method == 'POST':
        form = HelloForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['fname']
            last_name = form.cleaned_data['lname']
            return HttpResponse(
                "Hello, {} {}".format(first_name, last_name))
        else:
            return render(request, 'home.html')

    return render(request, 'home.html')


def mysql_trace(request):
    try:
        conn = mysql.connector.connect(
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD)
        cursor = conn.cursor()

        query = 'SELECT 2*3'
        cursor.execute(query)

        result = []

        for item in cursor:
            result.append(item)

        return HttpResponse(str(result))

    except Exception:
        msg = "Query failed. Check your env vars for connection settings."
        return HttpResponse(msg, status=500)


def postgresql_trace(request):
    try:
        conn = psycopg2.connect(
            host=config.POSTGRES_HOST,
            user=config.POSTGRES_USER,
            password=config.POSTGRES_PASSWORD,
            dbname=config.POSTGRES_DB)
        cursor = conn.cursor()

        query = 'SELECT * FROM company'
        cursor.execute(query)

        result = []

        for item in cursor.fetchall():
            result.append(item)

        return HttpResponse(str(result))

    except Exception:
        msg = "Query failed. Check your env vars for connection settings."
        return HttpResponse(msg, status=500)


def health_check(request):
    return HttpResponse("ok", status=200)


def get_request_header(request):
    return HttpResponse(request.META.get('HTTP_X_CLOUD_TRACE_CONTEXT'))