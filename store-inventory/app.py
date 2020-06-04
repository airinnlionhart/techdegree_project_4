#!/usr/bin/env python3
from collections import OrderedDict
import datetime
import sys
import os
from peewee import *

db = SqliteDataBase('inventory.db')

class Product(Model):
    product_id = IntegerField(primary_key=True)
    product_name = TextField()
    product_quantity = IntegerField()
    product_price = DecimalField()
    date_updated = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

def initialize():
    db.connect()
    db.create_tables([Product], safe=True)