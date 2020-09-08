from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql://root:holywars9@localhost') # connect to server
#engine.execute("CREATE DATABASE newspaper") #create db
engine.execute("USE newspaper")
Session = sessionmaker(bind=engine)
Base= declarative_base()