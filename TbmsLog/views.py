from django.views.generic.base import TemplateView
from django import forms
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http.response import HttpResponse
import os
import re
#from IPython.display import HTML
#plotly
import plotly
plotly.tools.set_credentials_file(username='taegyu', api_key='nyc1HbX2ynkigz2BMZt4')
import plotly.plotly as py
import plotly.graph_objs as go

#import cufflinks as cf
import pandas as pd
import numpy as np

import json
import collections
 
class HomeView(TemplateView):
    template_name = 'home.html'
    
class ReadFileView(TemplateView):
    template_name = 'read_file_view.html'
    
class ReadFileResultView(TemplateView):
    template_name = 'read_file_result_view2.html'
    
class LogResultView(TemplateView):
    template_name = 'read_file_result_view2.html'
    
    
@csrf_protect    
def read_file(request):
    fileName = request.POST.getlist('fileArray[]')
    rootPath = 'C:\\' + os.path.join('Users', 'SONY', 'Desktop', 'TBMS_LOG', 'tbms_logs')

    file_name_list = []
    log_dict_list = []
    exception_dict_list = []
    for i in range(len(fileName)):
        fullPath = os.path.join(rootPath, fileName[i])
        print(fullPath)
        f = open(os.path.abspath(fullPath), 'r')
        str_list = []
        for line in f:
            str_list.append(line)
        f.close()
        
        log_dict = {'INFO':0, 'WARN':0, 'ERROR':0, 'FATAL':0 }
        exception_dict = {}
        count_log(log_dict, exception_dict, str_list)
        
        file_name_list.append(fileName[i][9:19])
        log_dict_list.append(log_dict)
        exception_dict_list.append(exception_dict) 
    
    log_result = draw_stacked_bar_chart(file_name_list, log_dict_list, exception_dict_list)
        
    return HttpResponse(log_result)


def count_log(log_dict, exception_dict, str_list):
    for i in range(len(str_list)):
        count_by_logLevel(log_dict, str_list[i])
        count_by_exceptionType(exception_dict, str_list[i])

    
    
def count_by_logLevel(log_dict, line):
    log_dict['INFO'] += line.count('INFO')
    log_dict['WARN'] += line.count('WARN')
    log_dict['ERROR'] += line.count('ERROR')
    log_dict['FATAL'] += line.count('FATAL')
    
def count_by_exceptionType(exception_dict, line):

    if re.search('java.lang.\w*Exception', line):
        #exception_type = re.findall('java.lang.\w*Exception', line)
        exception_type = re.findall('\w*Exception', line)
        if exception_type[0] not in exception_dict:
            exception_dict[exception_type[0]] = 1
        else:
            exception_dict[exception_type[0]] += 1 
            
    elif re.search('org.springframework.\w*.\w*Exception', line):
        #exception_type = re.findall('org.springframework.\w*.\w*Exception', line)
        exception_type = re.findall('\w*Exception', line)
        if exception_type[0] not in exception_dict:
            exception_dict[exception_type[0]] = 1
        else:
            exception_dict[exception_type[0]] += 1 
            
    elif re.search('TbmsException', line):
        exception_type = re.findall('TbmsException', line)
        if exception_type[0] not in exception_dict:
            exception_dict[exception_type[0]] = 1
        else:
            exception_dict[exception_type[0]] += 1 


def draw_stacked_bar_chart(file_name_list, log_dict_list, exception_dict_list):
    print(file_name_list)
    print(log_dict_list)
    print(exception_dict_list)

    INFO_list = []
    WARN_list = []
    ERROR_list = []
    FATAL_list = []

    log_sum = {'INFO':0, 'WARN':0, 'ERROR':0, 'FATAL':0 }

    for i in range(len(file_name_list)):
        log_dict = log_dict_list[i] # info, warn, error, fatal
        INFO_list.append(log_dict['INFO'])
        WARN_list.append(log_dict['WARN'])
        ERROR_list.append(log_dict['ERROR'])
        FATAL_list.append(log_dict['FATAL'])
        
        log_sum['INFO'] += log_dict['INFO']
        log_sum['WARN'] += log_dict['WARN']
        log_sum['ERROR'] += log_dict['ERROR']
        log_sum['FATAL'] += log_dict['FATAL']
        #exception_dict = exception_dict_list[i] 
        
        
    trace1 = go.Bar(
        x=file_name_list,
        y=INFO_list,
        name='INFO',
        marker=dict(color='green')
    )
    trace2 = go.Bar(
        x=file_name_list,
        y=WARN_list,
        name='WARN',
        marker=dict(color='orange')
    )
    trace3 = go.Bar(
        x=file_name_list,
        y=ERROR_list,
        name='ERROR',
        marker=dict(color='red')
    )
    trace4 = go.Bar(
        x=file_name_list,
        y=FATAL_list,
        name='FATAL',
        marker=dict(color='black')
    )
    

    data = [trace1, trace2, trace3, trace4]
    
    layout = {
      'xaxis': {'title': 'log_date'},
      'yaxis': {'title': 'log_count'},
      'barmode': 'stack',
      'title': 'Log Level'
    };
    # stacked_bar
    plot = py.plot({'data': data, 'layout': layout}, filename='barmode-stack', auto_open=False)
    

    # pie_chart    
    labels = ['INFO','WARN','ERROR','FATAL']
    values = [log_sum['INFO'], log_sum['WARN'], log_sum['ERROR'], log_sum['FATAL']]
    marker = {'colors':['green','orange','red','black']}
    trace = go.Pie(labels=labels, values=values, marker=marker)
    chart = py.plot([trace], filename='basic_pie_chart', auto_open=False)
    
    # return plot, chart
    data = collections.namedtuple('data', ['plot', 'chart'])
    return_data = data(plot, chart)
    
    return return_data
    

