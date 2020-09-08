from sqlalchemy import Column, String, Integer, Text
from base import Base

class Article(Base):
    __tablename__ = 'articles'
    id = Column(String(200), primary_key=True)
    body = Column(Text())
    host = Column(String(200))
    title = Column(String(2000))
    newspaper = Column(String(100))
    n_tokens_body = Column(Integer)
    n_tokens_title = Column(Integer)
    url = Column(String(300), unique=True)

    def __init__(self, uid, body, host, newspaper, n_tokens_body, n_tokens_title, title, url):
        self.id = uid
        self.body = body
        self.host = host
        self.newspaper = newspaper
        self.n_tokens_body = n_tokens_body
        self.n_tokens_title = n_tokens_title
        self.title = title
        self.url = url