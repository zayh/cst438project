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
    self.assertEqual(object.getItem('album_id'), '')
    self.assertEqual(object.getItem('album_name'), '')
    self.assertEqual(object.getItem('release_date'), '')
    self.assertEqual(object.getItem('genre'), '')
    self.assertEqual(object.getItem('url_to_buy'), '')
    self.assertEqual(object.getItem('band_id'), '')
    
    
  def test_new(self):
    object = Album(self.data1)
    self.assertEqual(object.getItem('album_id'), '')
    self.assertEqual(object.getItem('album_name'), 'This is Spinal Tap')
    self.assertEqual(object.getItem('release_date'), '1984-03-02')
    self.assertEqual(object.getItem('genre'), 'comedy')
    self.assertEqual(object.getItem('url_to_buy'), 'none')
    self.assertEqual(object.getItem('band_id'), 4)
    
  def test_JSON(self):
    object1 = Album(self.data1)
    jsonStr = object1.toJSON()
    
    object2 = Album()
    self.assertEqual(object2.getItem('album_name'), '')
    self.assertEqual(object2.getItem('genre'), '')
    self.assertEqual(object2.getItem('band_id'), '')
    object2.fromJSON(jsonStr)
    self.assertEqual(object2.getItem('album_name'), 'This is Spinal Tap')
    self.assertEqual(object2.getItem('genre'), 'comedy')   
    self.assertEqual(object2.getItem('band_id'), 4)    
    
  def test_mutators_and_accessors(self):
    object1 = Album()
    self.assertTrue(object1.setItem('album_name','This is Spinal Tap'))
    self.assertTrue(object1.setItem('release_date','1984-03-02'))
    self.assertTrue(object1.setItem('genre','comedy'))
    self.assertTrue(object1.setItem('url_to_buy', 'none'))
    self.assertTrue(object1.setItem('band_id',4))
    
    self.assertEqual(object1.getItem('album_name'), 'This is Spinal Tap')
    self.assertEqual(object1.getItem('release_date'), '1984-03-02')
    self.assertEqual(object1.getItem('genre'), 'comedy')
    self.assertEqual(object1.getItem('url_to_buy'), 'none')
    self.assertEqual(object1.getItem('band_id'), 4)
    
  def test_getByAlbumID(self):
    object = Album()
    self.assertTrue(object.getRow(2))
    self.assertNotEqual(object.getItem('album_id'), '')
    self.assertEqual(object.getItem('album_name'), 'Metallica')
    
  def test_getByError(self):
    object = Album()
    self.assertFalse(object.getRow('Metal'))
    self.assertEqual(object.getItem('album_id'), '')
    
  def test_SaveAndDeleteFromDatabase(self):
    object1 = Album(self.data1)
    self.assertTrue(object1.addToDatabase())
    self.assertNotEqual(object1.getItem('album_id'), '')
    album_id = object1.getItem('album_id')

    object2 = Album()
    self.assertTrue(object2.getRow(album_id))
    self.assertNotEqual(object2.getItem('album_id'), '')
    self.assertTrue(object2.deleteFromDatabase())

    object3 = Album()
    self.assertFalse(object3.getRow(album_id))
    self.assertEqual(object3.getItem('album_id'), '')
    
  def test_duplicateAlbums(self):
    object1 = Album(self.data1)
    self.assertTrue(object1.addToDatabase())
    self.assertNotEqual(object1.getItem('album_id'), '')

    object2 = Album(self.data1)
    self.assertFalse(object2.addToDatabase())
    self.assertEqual(object2.getItem('album_id'), '')
    
    self.assertTrue(object1.deleteFromDatabase())

    
  def test_notDuplicate(self):
    object1 = Album(self.data1)
    object2 = Album(self.data2)
    self.assertTrue(object1.notDuplicate())
    self.assertFalse(object2.notDuplicate())

  def test_saveToDatabase(self):
    object = Album()
    self.assertTrue(object.getRow(2))
    self.assertEqual(object.getItem('genre'), 'Metal')
    self.assertTrue(object.setItem('genre','Country'))
    self.assertTrue(object.saveToDatabase())
    self.assertEqual(object.getItem('genre'), 'Country')
    self.assertTrue(object.setItem('genre','Metal'))
    self.assertTrue(object.saveToDatabase())
    self.assertEqual(object.getItem('genre'), 'Metal')   
    