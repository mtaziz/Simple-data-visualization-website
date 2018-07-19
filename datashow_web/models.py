# coding:utf-8
from django.db import models
from mongoengine import *


# Inherit the document class in mongodb
class Position(Document):
    # mongodb collection[key] = datatype in class document of mongoengine
    city = StringField()
    zone = StringField()
    positionName = StringField()
    labels = ListField(StringField())
    education = StringField()
    createtime = StringField()
    workyear = StringField()
    size = StringField()
    salary = StringField()
    company = StringField()
    # mongodb db.collection existed
    meta = {'collection': 'positionY'}

# Connect mongodb database,debug in the current interface.LaGou is a database in mongodb
# from mongoengine import connect
# connect('LaGou', host='127.0.0.1', port=27017)

# for i in Position.objects:
#     print(i.zone)

# pipeline = [
#     {'$group':{'_id':'$salary','counts':{'$sum':1}}},
#     {'$sort':{'counts':-1}},
#     {'$limit':20}
# ]

# method _get_collection() in mongoengine replace method find() in mongodb.
# for i in Position._get_collection().aggregate(pipeline):
#     # print([i['_id'],i['counts']])


