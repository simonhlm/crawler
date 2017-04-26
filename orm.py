# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Post(Base):
    __tablename__ = 'posts'

    idposts = Column(Integer, primary_key=True, default=None)
    website_id = Column(Integer)
    forum_id = Column(Integer)
    thread_id = Column(Integer)
    post_id = Column(Integer)
    post_author = Column(String(30))
    thread_name = Column(String(60))
    post_content = Column(Text(convert_unicode=True))
    post_date = Column(DateTime)
    post_floor = Column(Integer)
    post_trailer = Column(String(300))


class Thread(Base):
    __tablename__ = 'threads'

    idthreads = Column(Integer, primary_key=True, default=None)
    website_id = Column(Integer)
    forum_id = Column(Integer)
    thread_id = Column(Integer)
    thread_name = Column(String(60))
    creator = Column(String(30))
    create_date = Column(Date)
    last_updator = Column(String(45))
    last_update_time = Column(DateTime)
    replies = Column(Integer)
    views = Column(Integer)
    thread_href = Column(String(300))


class Website(Base):
    __tablename__ = 'websites'

    idwebsite = Column(Integer, primary_key=True)
    website_id = Column(Integer)
    website_name = Column(String(30))
    forum_id = Column(String(30))
    forum_name = Column(String(30))
