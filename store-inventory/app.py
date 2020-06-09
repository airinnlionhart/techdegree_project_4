#!/usr/bin/env python3
from collections import OrderedDict
import datetime
import sys
import os
import csv
from sqlite3 import IntegrityError

from peewee import *

db = SqliteDatabase('inventory.db')

class Product(Model):
    product_id = IntegerField(primary_key=True)
    product_name = TextField(unique=True)
    product_quantity = IntegerField()
    product_price = IntegerField()
    date_updated = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


def initialize():
    db.connect()
    db.create_tables([Product], safe=True)


def get_list_of_products():
    with open("inventory.csv", newline='') as csvfile:
        data = csv.DictReader(csvfile)
        list_of_dicts = []
        for row in data:
            list_of_dicts.append(row)
        return list_of_dicts

def clean_dictionary():
    clean_dict = get_list_of_products()
    for item in clean_dict:
        item['product_price'] = int(float(item['product_price'][1:])*100)
        item['product_quantity'] = int(item['product_quantity'])
        datetime_object = datetime.datetime.strptime(item['date_updated'], '%m/%d/%Y').date()
        item['date_updated'] = datetime_object.strftime('%m/%d/%Y')
    return(clean_dict)


def add_to_database():
    """adding csv file to database"""
    data_source = clean_dictionary()
    duplicates = []

    for data_dict in data_source:
        try:
            Product.create(**data_dict)
        except IntegrityError:
            product_duplicate = Product.get(product_name=data_dict["product_name"])
            product_duplicate.delete_instance()
            Product.create(**data_dict)



def menu_loop():
    """Show the menu options """
    choice = None

    while choice != 'q':
        print("Enter 'q' to quit")
        for key, value in menu.items():
            print('{}) {}'.format(key, value))
        choice = input('Please select a letter choice: ').lower().strip()

        if choice in menu:
            print('in menu')


def add_product():
    """Add and Entry"""

def view_products():
    """View all of the products"""
    query = Product.select()

    for entries in query:
        print(entries.product_id, entries.product_name, entries.product_quantity, entries.product_price, entries.date_updated)


def delete_an_entry():
    """Delete and entry"""



menu = OrderedDict([('a', 'add_product'),
                    ('v', 'view_products'),
                    ('d', 'delete_an_entry')
                   ])

if __name__ == "__main__":
    initialize()
    get_list_of_products()
    clean_dictionary()
    add_to_database()
    view_products()
    # menu_loop()
