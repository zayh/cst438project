import unittest
from MapSongToAlbum import MapSongToAlbum

class TestMapSongToAlbum(unittest.TestCase):

  data1 = {
    'map_song_to_album_id' : '',
    'song_id'      : 1,
    'album_id'     : 2,
    'track_number' : 1
  }
  
  data2 = {
    'song_id'      : 7,
    'album_id'     : 2,
    'track_number' : 8
  }

  def test_createEmptyMapSongToAlbum(self):
    object = MapSongToAlbum()
    self.assertIsInstance(object, MapSongToAlbum)
    self.assertEqual(object.getItem('map_song_to_album_id'), '')
    self.assertEqual(object.getItem('song_id'), '')
    self.assertEqual(object.getItem('album_id'), '')
    self.assertEqual(object.getItem('track_number'), '')
    
  def test_new(self):
    object = MapSongToAlbum(self.data1)
    self.assertEqual(object.getItem('map_song_to_album_id'), '')
    self.assertEqual(object.getItem('song_id'), 1)
    self.assertEqual(object.getItem('album_id'), 2)
    self.assertEqual(object.getItem('track_number'), 1)
    
  def test_JSON(self):
    object1 = MapSongToAlbum(self.data1)
    jsonStr = object1.toJSON()
    
    object2 = MapSongToAlbum()
    self.assertEqual(object2.getItem('song_id'), '')
    self.assertEqual(object2.getItem('album_id'), '')
    self.assertEqual(object2.getItem('track_number'), '')
    object2.fromJSON(jsonStr)
    self.assertEqual(object2.getItem('song_id'), 1)
    self.assertEqual(object2.getItem('album_id'), 2)
    self.assertEqual(object2.getItem('track_number'), 1)
    
  def test_mutators_and_accessors(self):
    object1 = MapSongToAlbum()
    self.assertTrue(object1.setItem('song_id',1))
    self.assertTrue(object1.setItem('album_id',2))
    self.assertTrue(object1.setItem('track_number',1))
    self.assertEqual(object1.getItem('song_id'), 1)
    self.assertEqual(object1.getItem('album_id'), 2)
    self.assertEqual(object1.getItem('track_number'), 1)
    
  def test_getByMapSongToAlbumID(self):
    object = MapSongToAlbum()
    self.assertTrue(object.getRow(1))
    self.assertNotEqual(object.getItem('map_song_to_album_id'), '')
    self.assertEqual(object.getItem('song_id'), 1)
    self.assertEqual(object.getItem('album_id'), 2)
    self.assertEqual(object.getItem('track_number'), 1)
    
  def test_SaveAndDeleteFromDatabase(self):
    object1 = MapSongToAlbum(self.data2)
    self.assertTrue(object1.addToDatabase())
    self.assertNotEqual(object1.getItem('map_song_to_album_id'), '')
    map_song_to_album_id = object1.getItem('map_song_to_album_id')

    object2 = MapSongToAlbum()
    self.assertTrue(object2.getRow(map_song_to_album_id))
    self.assertNotEqual(object2.getItem('map_song_to_album_id'), '')
    self.assertTrue(object2.deleteFromDatabase())

    object3 = MapSongToAlbum()
    self.assertFalse(object3.getRow(map_song_to_album_id))
    self.assertEqual(object3.getItem('map_song_to_album_id'), '')
    
  def test_duplicateMapSongToAlbums(self):
    object1 = MapSongToAlbum(self.data2)
    self.assertTrue(object1.addToDatabase())
    self.assertNotEqual(object1.getItem('map_song_to_album_id'), '')

    object2 = MapSongToAlbum(self.data2)
    self.assertFalse(object2.addToDatabase())
    self.assertEqual(object2.getItem('map_song_to_album_id'), '')
    
    self.assertTrue(object1.deleteFromDatabase())

  def test_saveToDatabase(self):
    object1 = MapSongToAlbum()
    self.assertTrue(object1.getRow(1))
    self.assertEqual(object1.getItem('album_id'), 2)
    self.assertEqual(object1.getItem('track_number'), 1)
    self.assertTrue(object1.setItem('track_number',4))
    self.assertTrue(object1.saveToDatabase())
    
    object2 = MapSongToAlbum()
    self.assertTrue(object2.getRow(1))
    self.assertEqual(object2.getItem('album_id'), 2)
    self.assertEqual(object2.getItem('track_number'), 4)
    self.assertTrue(object2.setItem('track_number',1))
    self.assertTrue(object2.saveToDatabase())
       