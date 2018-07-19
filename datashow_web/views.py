# coding:utf-8
from django.shortcuts import render
from datashow_web.models import Position
from django.core.paginator import Paginator
from datetime import timedelta, date
from mongoengine import *


# get series of chart line
def get_all_dates(date1, date2):
    """The date of a string is converted to an identifiable date of a program"""
    start_date = date(int(date1.split('.')[0]), int(date1.split('.')[1]), int(date1.split('.')[2]))
    end_date = date(int(date2.split('.')[0]), int(date2.split('.')[1]), int(date2.split('.')[2]))
    days = timedelta(days=1)
    while start_date <= end_date:
        # Match the string date format in the database
        yield start_date.strftime('%Y-%m-%d')
        start_date += days


def get_data_line(date1, date2, zones):
    """A data generator that generates a series of chart that needs the format of data"""
    for zone in zones:
        zone_day_posts = []
        for date in get_all_dates(date1, date2):
            a = list(Position.objects(createtime=date, zone=zone))
            each_day_post = len(a)
            zone_day_posts.append(each_day_post)
        data = {
            'name': zone,
            'data': zone_day_posts,
        }
        yield data

xAxis = [i for i in get_all_dates('2018.6.15', '2018.7.15')]
series_NS = [i for i in get_data_line('2018.6.15', '2018.7.15', [u'南山区'])]
series_FT = [i for i in get_data_line('2018.6.15', '2018.7.15', [u'福田区'])]
series_BA = [i for i in get_data_line('2018.6.15', '2018.7.15', [u'宝安区'])]
series_line = [i for i in get_data_line('2018.6.15', '2018.7.15', [u'南山区', u'龙岗区', u'龙华新区', u'福田区', u'宝安区', u'盐田区', u'罗湖区'])]


# get series of chart bar
def get_data_bar():
    zone_list = []
    for item in Position.objects:
        zone_list.append(item['zone'])
    zone_index = list(set(zone_list))

    post_times = []
    for index in zone_index:
        post_times.append(zone_list.count(index))

    length = 0
    if length <= len(zone_index):
        for zone, times in zip(zone_index, post_times):
            data = {
                'name': zone,
                'data': [times],
            }
            yield data
            length += 1
bar = 'column'
series_bar = [data for data in get_data_bar()]


# get series of chart pie1
def get_salary_pie():
    pipeline = [
        {'$group': {'_id': '$salary', 'counts': {'$sum': 1}}},
        {'$sort': {'counts': -1}},
        {'$limit': 20}
    ]
    for i in Position._get_collection().aggregate(pipeline):
        data = {
            'name': i['_id'],
            'y': i['counts'],
        }
        yield data
pie = 'pie'
series_pie1 = [i for i in get_salary_pie()]


# get series of chart pie2
def get_workyear_pie():
    pipeline = [
        {'$group': {'_id': '$workyear', 'counts': {'$sum': 1}}},
        {'$sort': {'counts': -1}},
    ]
    for i in Position._get_collection().aggregate(pipeline):
        data = {
            'name': i['_id'],
            'y': i['counts'],
        }
        yield data
series_pie2 = [i for i in get_workyear_pie()]


def index(request):
    limit = 10
    position = Position.objects
    paginator = Paginator(position, limit)
    page = request.GET.get('page', 1)
    # print(request)
    # print(request.GET)
    loaded = paginator.page(page)
    context = {
        'position': loaded,
        'counts': position.count(),
    }
    return render(request, 'index.html', context)


def chart(request):
    context = {
        'chart_NS': series_NS,
        'chart_FT': series_FT,
        'chart_BA': series_BA,
        'chart_ALL': series_line,
        'xAxis': xAxis,

        'bar': bar,
        'chart_bar': series_bar,

        'pie': pie,
        'chart_pie1': series_pie1,
        'chart_pie2': series_pie2,
    }
    return render(request, 'chart.html', context)
