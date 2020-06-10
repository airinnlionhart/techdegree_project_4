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


def add_to_database(a_dict):
    """adding a dictionary to the database"""

    if len(a_dict) > 6:
        for data_dict in a_dict:
            try:
                Product.create(**data_dict)
            except IntegrityError:
                product_duplicate = Product.get(product_name=data_dict["product_name"])
                product_duplicate.delete_instance()
                Product.create(**data_dict)
    else:
        try:
            Product.create(**a_dict)
        except IntegrityError:
            product_duplicate = Product.get(product_name=a_dict["product_name"])
            product_duplicate.delete_instance()
            Product.create(**a_dict)


def menu_loop():

    """Show the menu options """
    choice = None

    while choice != 'q':
        print("Enter 'q' to quit")
        for key, value in menu.items():
            print('{}) {}'.format(key, value))
        choice = input('Please select a letter choice: ').lower().strip()

        if choice == 'a':
            while True:
                product = input("Please enter a product name: ")
                quanity = int(input("Enter the number of products"))
                price = int(input("cost in cents"))
                try:
                    add_to_database({'product_name': product, "product_quantity": quanity, "product_price":price})
                    break
                except:
                    print("Something doesnt seem right please try again")
        elif choice == 'v':
            view_option = input('enter the id you would like to see or hit enter to see all: ')
            while True:
                try:
                    view_product(Product.get(product_id=int(view_option)))
                    break
                except ValueError:
                    view_all_products()
                    break
                except:
                    print("This index is not in the table")
                    view_all_products()
                    break
        elif choice == 'd':
            delete_option = input('enter the id of the item you would like to delete: ')
            while True:
                try:
                    delete_product(Product.get(product_id=int(delete_option)))
                    break
                except ValueError:
                    view_all_products()
                    break
                except:
                    print("This index is not in the table")
                    view_all_products()
                    break
        elif choice == 'b':
            results = get_all_products()
            with open("product_table_backup.csv", "a") as a_file:
                for element in results:
                    a_file.write(element+'\n')
        elif choice == 'q':
            break
        else:
            print("not a choice")

def view_product(product_id):
    query = product_id

    print(query.product_id, query.product_name, query.product_quantity, query.product_price, query.date_updated)

def view_all_products():
    """View all of the products"""
    query = Product.select()

    for entries in query:
        print(entries.product_id, entries.product_name, entries.product_quantity, entries.product_price, entries.date_updated)


def get_all_products():
    backup_database_list = []
    query = Product.select()
    for entries in query:
        backup_database_list.append(str(entries.product_id) + ', ' + str(entries.product_name) +', '+ str(entries.product_quantity) +', '+
                                    str(entries.product_price) +', ' + str(entries.date_updated))
    return backup_database_list


def delete_product(product_id):
    """Delete and entry"""
    query = product_id
    print(query.product_id, query.product_name, query.product_quantity, query.product_price, query.date_updated)
    are_you_sure = input("Press enter to confirm your sure or input anything if you do not wish to delete item")
    if are_you_sure == '':
        query.delete_instance()
    else:
        pass


menu = OrderedDict([('a', 'add_product'),
                    ('v', 'view_products'),
                    ('d', 'delete_an_entry'),
                    ('b', 'back_up')
                   ])

if __name__ == "__main__":
    initialize()
    get_list_of_products()
    clean_dictionary()
    add_to_database(clean_dictionary())
    menu_loop()
