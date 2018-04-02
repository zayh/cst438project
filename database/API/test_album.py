import unittest
from Album import Album

class TestAlbum(unittest.TestCase):

  data1 = { 
    'album_id' : '',
    'album_name' : 'This is Spinal Tap',
    'release_date' : '1984-03-02',
    'genre' : 'comedy',
    'url_to_buy' : 'none',
    'band_id' : 4  
  }
  
  data2 = {
    'album_id' : '',
    'album_name' : 'Metallica',
    'release_date': '2018-03-04',
    'genre' : 'metal',
    'url_to_buy' : 'none',
    'band_id' : 1
  }

  def test_createEmptyAlbum(self):
    object = Album()
    self.assertIsInstance(object, Album)
    self.assertEqual(object.getAlbumID(), '')
    self.assertEqual(object.getAlbumName(), '')
    self.assertEqual(object.getReleaseDate(), '')
    self.assertEqual(object.getGenre(), '')
    self.assertEqual(object.getURLtoBuy(), '')
    self.assertEqual(object.getBandID(), '')
    
    
  def test_new(self):
    object = Album(self.data1)
    self.assertEqual(object.getAlbumID(), '')
    self.assertEqual(object.getAlbumName(), 'This is Spinal Tap')
    self.assertEqual(object.getReleaseDate(), '1984-03-02')
    self.assertEqual(object.getGenre(), 'comedy')
    self.assertEqual(object.getURLtoBuy(), 'none')
    self.assertEqual(object.getBandID(), 4)
    
  def test_toJSON(self):
    object = Album(self.data1)
    self.assertEqual(object.toJSON(), 
      '{"album_id": "", "album_name": "This is Spinal Tap", '
      '"release_date": "1984-03-02", "genre": "comedy", '
      '"url_to_buy": "none", "band_id": 4}'
    )
    
  def test_mutators_and_accessors(self):
    object1 = Album()
    self.assertTrue(object1.setAlbumName('This is Spinal Tap'))
    self.assertTrue(object1.setReleaseDate('1984-03-02'))
    self.assertTrue(object1.setGenre('comedy'))
    self.assertTrue(object1.setURLtoBuy('none'))
    self.assertTrue(object1.setBandID(4))
    
    self.assertEqual(object1.getAlbumName(), 'This is Spinal Tap')
    self.assertEqual(object1.getReleaseDate(), '1984-03-02')
    self.assertEqual(object1.getGenre(), 'comedy')
    self.assertEqual(object1.getURLtoBuy(), 'none')
    self.assertEqual(object1.getBandID(), 4)
    
  def test_getByAlbumID(self):
    object = Album()
    self.assertTrue(object.getBy('album_id', 2))
    self.assertNotEqual(object.getAlbumID(), '')
    self.assertEqual(object.getAlbumName(), 'Metallica')
    
  def test_getByError(self):
    object = Album()
    self.assertFalse(object.getBy('genre', 'Metal'))
    self.assertEqual(object.getAlbumID(), '')
    
  def test_SaveAndDeleteFromDatabase(self):
    object1 = Album(self.data1)
    self.assertTrue(object1.addToDatabase())
    self.assertNotEqual(object1.getAlbumID(), '')
    album_id = object1.getAlbumID()

    object2 = Album()
    self.assertTrue(object2.getBy('album_id', album_id))
    self.assertNotEqual(object2.getAlbumID(), '')
    self.assertTrue(object2.deleteFromDatabase())

    object3 = Album()
    self.assertFalse(object3.getBy('album_id', album_id))
    self.assertEqual(object3.getAlbumID(), '')
    
  def test_duplicateAlbums(self):
    object1 = Album(self.data1)
    self.assertTrue(object1.addToDatabase())
    self.assertNotEqual(object1.getAlbumID(), '')

    object2 = Album(self.data1)
    self.assertFalse(object2.addToDatabase())
    self.assertEqual(object2.getAlbumID(), '')
    
    self.assertTrue(object1.deleteFromDatabase())

    
  def test_isAlbumNameAvailable(self):
    object1 = Album(self.data1)
    object2 = Album(self.data2)
    self.assertTrue(object1.isAlbumNameAvailable())
    self.assertFalse(object2.isAlbumNameAvailable())

  def test_saveToDatabase(self):
    object = Album()
    self.assertTrue(object.getBy('album_id', 2))
    self.assertEqual(object.getGenre(), 'Metal')
    self.assertTrue(object.setGenre('Country'))
    self.assertTrue(object.saveToDatabase())
    self.assertEqual(object.getGenre(), 'Country')
    self.assertTrue(object.setGenre('Metal'))
    self.assertTrue(object.saveToDatabase())
    self.assertEqual(object.getGenre(), 'Metal')   
    