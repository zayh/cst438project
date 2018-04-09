import flask
import flask_sqlalchemy
import flask_restless

# Create the Flask application and the Flask-SQLAlchemy object

application = flask.Flask(__name__)
app = application
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://webapp:centralSolutions123@18.222.66.236/musicproject'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = flask_sqlalchemy.SQLAlchemy(app)

class Account(db.Model):
    __tablename__ = 'account'
    
    account_id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True, index=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    lyric = db.Column(db.Text)
    password = db.Column(db.String(500), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='user')

        
class Album(db.Model):
    __tablename__ = 'album'
    
    album_id = db.Column(db.BigInteger, primary_key=True)
    album_name = db.Column(db.String(50), nullable=False)
    release_date = db.Column(db.Date)
    genre = db.Column(db.String(50), nullable=True)
    url_to_buy = db.Column(db.String(500), nullable=True)
    band_id = db.Column(db.BigInteger, db.ForeignKey("band.band_id", onupdate="CASCADE", 
        ondelete="CASCADE"), nullable=False)
        
class Band(db.Model):
    __tablename__ = 'band'
    
    band_id = db.Column(db.BigInteger, primary_key=True)
    band_name = db.Column(db.String(50), unique=True, nullable=False)
   
class Favorite(db.Model):
    __tablename__ = 'favorite'
    
    favorite_id = db.Column(db.BigInteger, primary_key=True)
    account_id = db.Column(db.BigInteger, db.ForeignKey("account.account_id", 
        onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    album_id = db.Column(db.BigInteger, db.ForeignKey("album.album_id", 
        onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

class Rating(db.Model):
    __tablename__ = 'rating'
    
    rating_id = db.Column(db.BigInteger, primary_key=True)
    rating_date = db.Column(db.Date)
    account_id = db.Column(db.BigInteger, db.ForeignKey("account.account_id",
        onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    album_id = db.Column(db.BigInteger, db.ForeignKey("album.album_id", 
        onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    
        
class Song(db.Model):
    __tablename__ = 'song'
    
    song_id = db.Column(db.BigInteger, primary_key=True)
    song_name = db.Column(db.String(100), nullable=False)
    album_id = db.Column(db.BigInteger, db.ForeignKey('album.album_id'))            
    band_id = db.Column(db.BigInteger, db.ForeignKey("band.band_id", onupdate="CASCADE", 
        ondelete="CASCADE"), nullable=False)
    track_number = db.Column(db.Integer)
      
class Wishlist(db.Model):
    __tablename__ = 'wishlist'
    
    wishlist_id = db.Column(db.BigInteger, primary_key=True)
    account_id = db.Column(db.BigInteger, db.ForeignKey("account.account_id",
        onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    album_id = db.Column(db.BigInteger, db.ForeignKey("album.album_id", 
        onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

# Create the API manager
manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)

manager.create_api(Account, methods=['GET', 'POST', 'DELETE', 'PUT'])
manager.create_api(Album, methods=['GET', 'POST', 'DELETE', 'PUT'])
manager.create_api(Band, methods=['GET', 'POST', 'DELETE', 'PUT'])
manager.create_api(Favorite, methods=['GET', 'POST', 'DELETE', 'PUT'])
manager.create_api(Rating, methods=['GET', 'POST', 'DELETE', 'PUT'])
manager.create_api(Song, methods=['GET', 'POST', 'DELETE', 'PUT'])
manager.create_api(Wishlist, methods=['GET', 'POST', 'DELETE', 'PUT'])
        
@app.route('/')
def show_api():
    return flask.render_template('index.html', baseURL='http://18.219.102.221')