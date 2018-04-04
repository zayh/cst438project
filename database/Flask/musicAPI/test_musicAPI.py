import unittest
import application as app
import json

class TestApplication(unittest.TestCase):
  
    
    def testAccountCreate(self):
        object = app.Account(username='test1', password='testpass1', firstname='testfirst', lastname='testlast')
        self.assertIsNone(object.account_id)
        app.session.add(object)
        app.session.commit()
        self.assertIsNotNone(object.account_id)
        app.session.delete(object)
        app.session.commit()

    def testAccountPasswordHash(self):
        object = app.Account(username='test1', firstname='testfirst', lastname='testlast')
        object.password = app.Cypher.hashPassword('testpass1')
        self.assertEqual(object.password, '17406e11c3af2ba6ebb2bc008b892892b73fc3e260eb6ef202794a8e507d0c1e')
        
    def testAccount_toJSON(self):
        object = app.Account(username='test1', firstname='testfirst', lastname='testlast')
        object.password = app.Cypher.hashPassword('testpass1')
        self.assertEqual(json.dumps(object, cls=app.AlchemyEncoder), '{"account_id": null, "firstname": "testfirst", "lastname": "testlast", "lyric": null, "password": "17406e11c3af2ba6ebb2bc008b892892b73fc3e260eb6ef202794a8e507d0c1e", "role": null, "username": "test1"}')
        
    def testAlbum(self):
        object = app.Album(album_name='testAlbum1', release_date='2018-02-01', genre='pop', url_to_buy='none', band_id = 1)
        app.session.add(object)
        self.assertIsNone(object.album_id)
        self.assertEqual(json.dumps(object, cls=app.AlchemyEncoder),
            '{"album_id": null, "album_name": "testAlbum1", "band_id": 1, "genre": "pop", "release_date": "2018-02-01", "url_to_buy": "none"}')
        app.session.commit()
        self.assertIsNotNone(object.album_id)
        app.session.delete(object)
        app.session.commit()
        
    def testBand(self):
        object = app.Band(band_name='testBand1',is_solo_artist=True)
        self.assertIsNone(object.band_id)
        app.session.add(object)
        app.session.commit()
        self.assertIsNotNone(object.band_id)
        self.assertEqual(json.dumps(object, cls=app.AlchemyEncoder), '{"band_id": ' + str(object.band_id) + ', "band_name": "testBand1", "is_solo_artist": true}')
        app.session.delete(object)
        app.session.commit()
        
    def testRating(self):
        object = app.Rating(album_id=2, account_id=34, rating=3, comment="meh")
        self.assertIsNone(object.rating_id)
        app.session.add(object)
        app.session.commit()
        self.assertIsNotNone(object.rating_id)
        self.assertEqual(json.dumps(object, cls=app.AlchemyEncoder), '{"account_id": 34, "album_id": 2, "comment": "meh", "rating": 3, "rating_id": ' + str(object.rating_id) + '}')
        app.session.delete(object)
        app.session.commit()
       
    def testSong(self):
        object = app.Song(song_name='Test Song', band_id=4)
        self.assertIsNone(object.song_id)
        app.session.add(object)
        app.session.commit()
        self.assertIsNotNone(object.song_id)
        self.assertEqual(json.dumps(object, cls=app.AlchemyEncoder), '{"band_id": 4, "is_solo_release": false, "song_id": ' + str(object.song_id) + ', "song_name": "Test Song"}')
        app.session.delete(object)
        app.session.commit()

    def testWishlist(self):
        object = app.Wishlist(account_id=34, album_id=48)
        self.assertIsNone(object.wishlist_id)
        app.session.add(object)
        app.session.commit()
        self.assertIsNotNone(object.wishlist_id)
        self.assertEqual(json.dumps(object, cls=app.AlchemyEncoder),
            '{"account_id": 34, "album_id": 48, "wishlist_id": ' + str(object.wishlist_id) + '}')
        app.session.delete(object)
        app.session.commit()