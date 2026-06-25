import time as t
import sqlite3 as sql

#initiation
conn = sql.connect('farm.db')

def menu():
    print("Welcome to Potato Farm!!\n=======================")
    print("1.Farm\n2.Shop\n3.Exit")
    choice = input("Enter Choice: ")
    return choice

def Farm():
    pass
#main:
menu()
