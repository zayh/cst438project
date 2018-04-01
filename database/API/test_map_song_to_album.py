import unittest
from MapSongToAlbum import MapSongToAlbum

class TestMapSongToAlbum(unittest.TestCase):

  def test_createEmptyMapSongToAlbum(self):
    object = MapSongToAlbum()
    self.assertIsInstance(object, MapSongToAlbum)
    self.assertEqual(object.getMapSongToAlbumID(), '')
    self.assertEqual(object.getSongID(), '')
    self.assertEqual(object.getAlbumID(), '')
    self.assertEqual(object.getTrackNumber(), '')
    
  def test_new(self):
    object = MapSongToAlbum()
    object.new(1, 2, 1);
    self.assertEqual(object.getMapSongToAlbumID(), '')
    self.assertEqual(object.getSongID(), 1)
    self.assertEqual(object.getAlbumID(), 2)
    
  def test_toJSON(self):
    object = MapSongToAlbum()
    object.new(1, 2, 1)
    self.assertEqual(object.toJSON(), 
      "{ map_song_to_album_id: , song_id: 1, album_id: 2, track_number: 1 }" 
    )
    
  def test_mutators_and_accessors(self):
    object1 = MapSongToAlbum()
    self.assertTrue(object1.setSongID(1))
    self.assertTrue(object1.setAlbumID(2))
    self.assertTrue(object1.setTrackNumber(1))
    self.assertEqual(object1.getSongID(), 1)
    self.assertEqual(object1.getAlbumID(), 2)
    self.assertEqual(object1.getTrackNumber(), 1)
    
  def test_getByMapSongToAlbumID(self):
    object = MapSongToAlbum()
    self.assertTrue(object.getBy('map_song_to_album_id', 1))
    self.assertNotEqual(object.getMapSongToAlbumID(), '')
    self.assertEqual(object.getSongID(), 1)
    self.assertEqual(object.getAlbumID(), 2)
    self.assertEqual(object.getTrackNumber(), 1)
    
  def test_getByError(self):
    object = MapSongToAlbum()
    self.assertFalse(object.getBy('song_id', 1))
    self.assertEqual(object.getMapSongToAlbumID(), '')
    
  def test_SaveAndDeleteFromDatabase(self):
    object1 = MapSongToAlbum()
    self.assertTrue(object1.new(7, 2, 8))
    self.assertTrue(object1.addToDatabase())
    self.assertNotEqual(object1.getMapSongToAlbumID(), '')
    map_song_to_album_id = object1.getMapSongToAlbumID()

    object2 = MapSongToAlbum()
    self.assertTrue(object2.getBy('map_song_to_album_id', map_song_to_album_id))
    self.assertNotEqual(object2.getMapSongToAlbumID(), '')
    self.assertTrue(object2.deleteFromDatabase())

    object3 = MapSongToAlbum()
    self.assertFalse(object3.getBy('map_song_to_album_id', map_song_to_album_id))
    self.assertEqual(object3.getMapSongToAlbumID(), '')
    
  def test_duplicateMapSongToAlbums(self):
    object1 = MapSongToAlbum()
    self.assertTrue(object1.new(7, 2, 8))
    self.assertTrue(object1.addToDatabase())
    self.assertNotEqual(object1.getMapSongToAlbumID(), '')

    object2 = MapSongToAlbum()
    self.assertTrue(object1.new(7, 2, 8))
    self.assertFalse(object2.addToDatabase())
    self.assertEqual(object2.getMapSongToAlbumID(), '')
    
    self.assertTrue(object1.deleteFromDatabase())

  def test_saveToDatabase(self):
    object1 = MapSongToAlbum()
    self.assertTrue(object1.getBy('map_song_to_album_id', 1))
    self.assertEqual(object1.getAlbumID(), 2)
    self.assertEqual(object1.getTrackNumber(), 1)
    self.assertTrue(object1.setTrackNumber(4))
    self.assertTrue(object1.saveToDatabase())
    
    object2 = MapSongToAlbum()
    self.assertTrue(object2.getBy('map_song_to_album_id', 1))
    self.assertEqual(object2.getAlbumID(), 2)
    self.assertEqual(object2.getTrackNumber(), 4)
    self.assertTrue(object2.setTrackNumber(1))
    self.assertTrue(object2.saveToDatabase())
       