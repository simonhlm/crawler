from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlite3
import jieba
import time

from orm import *

conn = sqlite3.connect('lkong.db')
cursor = conn.cursor()
cursor.execute('select post_content from posts')
values = cursor.fetchall()
for item in values:
    #print(item)
    print('result:','/'.join(jieba.cut(item[0])))
#cursor.execute('select * from posts')
#values = cursor.fetchone()
#print(values)
"""
engine = create_engine('sqlite:///lkong.db')
session = sessionmaker()
session.configure(bind=engine)
s = session()
print(s.query(Thread).all()[0])
print(s.query(Post).all())
"""