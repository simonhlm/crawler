# -*- encoding=utf-8 -*-
import re
import jieba
import codecs
import logging

import sqlite3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from orm import *

logging.basicConfig(level=logging.INFO)

def generate_report(report_name):
    engine = create_engine('mysql+pymysql://simon:654321@localhost/crawler',encoding='utf8', convert_unicode=True)
    #engine = create_engine('sqlite:///lkong.db')
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()
    """
        conn = sqlite3.connect('lkong.db')
        cursor = conn.cursor()
        cursor.execute('select post_content from posts')
        values = cursor.fetchall()
    """

    values = s.query(Post.post_content).filter(Post.forum_id==48).all()

    num = 1
    with codecs.open(report_name+'.csv','w','utf-8') as f:
        for item in values:
            _item = '/'.join(jieba.cut(item[0]))
            f.write(_item)
            num += 1

def analysis_report(report_name):

    words =[]
    ban_record = []
    with codecs.open('stopwords.txt','r','utf-8') as fr:
        rr = fr.readlines()
        for line in rr:
            _ban = line.split('\r\n')
            ban_record.extend(_ban)
    ban_record = set(ban_record)

    #ban_record  = set(['','，','？','！','。','-','=','(',')',\
    #            '@',':','这','的','我','了','.','!','…','是','你','但','在','-','他',\
    #            '就','也','【','：','”','《','、','】','“','...','—','；','（','）',',',\
    #            '》','→'])

    with codecs.open(report_name+'.csv','r','utf-8') as f:
        r = f.readlines()
        for line in r:
            _line = re.sub('[\s\d]','',line).split('/')
            for word in _line:
                if word not in ban_record:
                    words.append(word)

    logging.info('Total individule word: %s, Total words : %s',(len(set(words)),len(words)))

    #sort words
    words.sort()
    logging.info('Sort complete')

    n = 0
    count = 1
    word_len = len(words) - 1
    wordcount = []
    while n< word_len :
        if words[n] == words[n+1]:
            count += 1
        else:
            wordcount.append((words[n],count))
            count = 1
        n += 1

    logging.info('Count complete')
    #wordcount = [(w,words.count(w)) for w in set(words)]

    wordcount=sorted(wordcount,key=lambda l:(-l[1],l[0]))

    with codecs.open(report_name+'_result.csv','w','utf-8') as fs:
        for item in wordcount:
            fs.write(item[0]+':'+str(item[1])+'\n')
    logging.info('process completed')

def add_dict_word():
    pass

if __name__ == '__main__':
    jieba.load_userdict('userdict_rmmy.csv') 
    report_name = 'f48all'
    generate_report(report_name)
    analysis_report(report_name)