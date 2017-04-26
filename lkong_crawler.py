#! /usr/bin/env python
# -*- encoding:utf-8 -*-

import re

from bs4 import BeautifulSoup
from craw import Craw
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from orm import *

def process_post(r_post):

    bsobj = BeautifulSoup(r_post.content,'html.parser')
    #result = bsobj.find_all('div',{'id':'postlist'})

    thread_id=[]
    thread_name=[]
    post_author=[]
    post_content=[]
    post_id=[]
    post_date=[]
    post_floor=[]
    #post_trailer=[]

    #从返回的页面抓取所需的column, 处理并返回tuple
    thread_title_href = bsobj.find_all('a',{'id':'thread_subject'})
    for item in thread_title_href: # for the post content
        thread_id.append(re.search(r'tid=(\d*)&extra',item['href']).group(1))
        thread_name.append(item.text)

    #抓取数据
    auth = bsobj.find_all('a',{'class':'xw1','href':re.compile(r'uid=\d*$')})
    for item in auth: # for the post content
        post_author.append(item.text)

    content = bsobj.find_all('td',{'id':re.compile('^postmessage')})
    for item in content: # for the post content
        post_id.append(re.search(r'message_(\d*)',item['id']).group(1))
        post_content.append(re.split(r'\xa0',item.text)[0]) # split the content by \xa0 and save the real one 

    floor = bsobj.find_all('a',{'class':'brm','id':re.compile(r'^postnum')})
    for item in floor:
        post_floor.append(re.search(r'(\d*)#$',item.text).group(1))
        #post_floor.append(item.text)

    date = bsobj.find_all('em',{'id':re.compile(r'^authorposton')})
    for item in date:
        post_date.append(re.search(r'.*(\d{4}.*\s\d{2}:\d{2})$',item.text).group(1))

    return zip(post_id, post_author, post_content, post_date, post_floor)

def process_thread(r_thread):

    bsobj = BeautifulSoup(r_thread.content,'html.parser')

    thread_href=[]
    thread_name=[]
    thread_id=[]
    thread_creator=[]
    thread_create_date=[]
    thread_replies=[]
    thread_last_updator=[]
    thread_last_update_time=[]


    thread_name_href = bsobj.find_all('a',{'class':'xst','href':re.compile(r'thread-\d*-\d*-\d*.html$')})
    for item in thread_name_href: # for the post content
        thread_href.append(item['href'])
        thread_id.append(re.search(r'thread-(\d*)-',item['href']).group(1))
        thread_name.append(item.text)

    creator = bsobj.find_all('a',{'href':re.compile(r'space&uid=\d*$')})
    for item in creator:
        thread_creator.append(item.text)

    create_time = bsobj.find_all('tbody',{'id':re.compile(r'.*thread.*')})
    for item in create_time:
        thread_create_date.append(re.search(r'.*<em>(\d{4}-\d*-\d*)</em>.*',str(item)).group(1))

    replies = bsobj.find_all('a',{'class':'xi2','href':re.compile(r'thread-\d*-\d*-\d*.html$')})
    for item in replies:
        thread_replies.append(item.text)

    last_updator = bsobj.find_all('a',{'href':re.compile(r'space&username=.*$')})
    for item in last_updator:
        thread_last_updator.append(item.text)

    last_update_time = bsobj.find_all('a',{'href':re.compile('redirect.*lastpost$')},text=re.compile(r'^\d*-'))
    for item in last_update_time:
        thread_last_update_time.append(item.text)

    return zip(thread_id, thread_name, thread_href, thread_create_date,thread_creator, thread_replies,thread_last_updator, thread_last_update_time)

if __name__ == '__main__':

    post_url  = 'http://www.lkong.net/thread-1735189-1-1.html'

    threads_url  = 'http://www.lkong.net/forum.php'
    thread_info = {'mod':'forumdisplay','fid':'8','page':'1'}

    lkong = Craw()

    response_thread = lkong.get_content(threads_url, params=thread_info)
    threads_list = list(process_thread(response_thread))

    for i in threads_list:
        print(i)

    #response_post = lkong.get_content(threads_list[1][2])
    #post_info = process_post(response_thread)

    #for i in post_info:
    #   print(i)

    # 

    #for thread in threads_list:
        #process individule post

        #response_post = lkong.get_content(thread[2])
        #post_info = process_post(response_post)
        #for i in post_info:
            #print(i)
"""
    engine = create_engine('mysql+pymysql://simon:654321@localhost/crawler',encoding='utf8', convert_unicode=True)
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()
    for item in post_info:
        print(item)
        post_record = Post(post_author=item[0],post_content=item[1])
        s.add(post_record)
        s.commit()
        """