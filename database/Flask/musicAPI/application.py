from flask import Flask
from flask import request, render_template
from sqlalchemy import create_engine, Column, Integer, String, exc
from sqlalchemy import BigInteger, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import DeclarativeMeta
import json
import datetime
import hashlib

Base = declarative_base()
engine = create_engine("mysql://webapp:centralSolutions123@18.222.66.236/musicproject", encoding='latin1')
Session = sessionmaker(bind=engine)

application = Flask(__name__)

session = Session()

class Cypher:
   def hashPassword(passwordInText):
        return hashlib.sha256( passwordInText.encode('utf-8') ).hexdigest()

class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    # Convert dates to strings
                    if isinstance(data, datetime.date):
                        data = data.isoformat()
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)

class Account(Base):
    __tablename__ = 'account'
    
    account_id = Column(BigInteger, primary_key=True)
    username = Column(String(32), nullable=False, unique=True, index=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    lyric = Column(Text)
    password = Column(String(500), nullable=False)
    role = Column(String(10), nullable=False, default='user')

        
class Album(Base):
    __tablename__ = 'album'
    
    album_id = Column(BigInteger, primary_key=True)
    album_name = Column(String(50), nullable=False)
    release_date = Column(DateTime)
    genre = Column(String(50), nullable=True)
    url_to_buy = Column(String(500), nullable=True)
    band_id = Column(BigInteger, ForeignKey("band.band_id", onupdate="CASCADE", 
        ondelete="CASCADE"), nullable=False)
        
class Band(Base):
    __tablename__ = 'band'
    
    band_id = Column(BigInteger, primary_key=True)
    band_name = Column(String(50), nullable=False)
    is_solo_artist = Column(Boolean(), default=False)
   
class Favorite(Base):
    __tablename__ = 'favorite'
    
    favorite_id = Column(BigInteger, primary_key=True)
    account_id = Column(BigInteger, ForeignKey("account.account_id", 
        onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    album_id = Column(BigInteger, ForeignKey("album.album_id", 
        onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

class Rating(Base):
    __tablename__ = 'rating'
    
    rating_id = Column(BigInteger, primary_key=True)
    account_id = Column(BigInteger, ForeignKey("account.account_id",
        onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    album_id = Column(BigInteger, ForeignKey("album.album_id", 
        onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
        
class Song(Base):
    __tablename__ = 'song'
    
    song_id = Column(BigInteger, primary_key=True)
    song_name = Column(String(100), nullable=False)
    is_solo_release = Column(Boolean(), nullable=False, default=False)
    band_id = Column(BigInteger, ForeignKey("band.band_id", onupdate="CASCADE", 
        ondelete="CASCADE"), nullable=False)
      
class Wishlist(Base):
    __tablename__ = 'wishlist'
    
    wishlist_id = Column(BigInteger, primary_key=True)
    account_id = Column(BigInteger, ForeignKey("account.account_id",
        onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    album_id = Column(BigInteger, ForeignKey("album.album_id", 
        onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
      
if '__name__' == '__main__':
    application.run()
    
def alchemyencoder(obj):
    '''JSON encoder function'''
    if isinstance(obj, datetime.date):
        return obj.isoformat()

@application.route('/band')
def addband():
    return render_template('addband.html')
        
@application.route('/band/<data>', methods = ['GET','POST'])
def band_functions(data):
    if request.method == 'POST':
        if 'band_name' in request.form:
            session.add(Band(band_name=request.form['band_name']))
            session.commit()
        return "Band added"
            
    else:
        band_id = str(data)
        result = session.query(Band).filter(Band.band_id == band_id).first()
        if result is not None:
            output = "[" + result.toJSON() + "]"
        else:
            output = "[]"
        return output

@application.route('/albums/')
def get_albums():
    results = session.execute("select * from album")
    return json.dumps([dict(r) for r in results], default=alchemyencoder)
    
@application.route('/bands/')
def get_bands():
    results = session.execute("select * from band")
    return json.dumps([dict(r) for r in results], default=AlchemyEncoder)

@application.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            return get_role(request.form['username'])
        else:
            return '[{"role":"none"}]'
    else:
        return render_template('login.html')
        

@application.route('/adduser', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        success = False
        noSqlError = True
        if 'username' in request.form and 'password' in request.form:
            if 'firstname' in request.form and 'lastname' in request.form:
                newuser = Account(
                    username=request.form['username'],
                    password=Cypger.hashPassword(request.form['password']),
                    firstname=request.form['firstname'],
                    lastname=request.form['lastname'],
                )
                session.add(newuser)
                try:
                    session.commit()
                except exc.SQLAlchemyError:
                    noSqlError = False
                if noSqlError and newuser.account_id is not None:
                    success = True
        if success:
            return '[' + newuser.toJSON() + ']'
        else:
            return '[{"response":"failed"}]'
    else:
        return render_template('adduser.html')
    
@application.route('/ratings/')
def get_ratings():
    results = session.execute("select * from rating")
    return json.dumps([dict(r) for r in results], default=alchemyencoder)
    
@application.route('/songs/')
def get_songs():
    results = session.execute("select * from song")
    return json.dumps([dict(r) for r in results], default=AlchemyEncoder)
  
@application.route('/wishlists/')
def get_wishlists():
    results = session.execute("select * from wishlist")
    return json.dumps([dict(r) for r in results], default=alchemyencoder)
    
    
def valid_login(user, password):
    success = False
    user = session.query(Account).filter(Account.username == user).first()
    if user is not None:
        if user.password == Cypher.hashPassword(password):
            success = True
    return success
    
def get_role(username):
    user = session.query(Account).filter(Account.username == username).first()
    return '[{"role":"' + user.role + '"}]'