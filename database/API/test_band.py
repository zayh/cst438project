import unittest
from Band import Band

class TestBand(unittest.TestCase):

  def test_createEmptyBand(self):
    object = Band()
    self.assertIsInstance(object, Band)
    self.assertEqual(object.getBandID(), '')
    self.assertFalse(object.isSoloArtist(), '')
    self.assertEqual(object.getBandName(), '')
    
  def test_new(self):
    object1 = Band('Spinal Tap')
    self.assertEqual(object1.getBandID(), '')
    self.assertEqual(object1.getBandName(), 'Spinal Tap')
    self.assertFalse(object1.isSoloArtist())
    
    object2 = Band('Prince', True)
    self.assertEqual(object2.getBandID(), '')
    self.assertEqual(object2.getBandName(), 'Prince')
    self.assertTrue(object2.isSoloArtist())
    
  def test_toJSON(self):
    object = Band('Spinal Tap')
    self.assertEqual(object.toJSON(), '{"band_id": "", "band_name": "Spinal Tap", "is_solo_artist": false}')
  
  def test_fromJSON(self):
    object1 = Band('Prince', True)
    dataStr = object1.toJSON()
    
    object2 = Band()
    self.assertTrue(object2.fromJSON(dataStr))
    self.assertEqual(object2.getBandName(), 'Prince')
    
  def test_mutators_and_accessors(self):
    object1 = Band('Def Leppard')
    object1.setSoloArtist(True)

    object2 = Band('Prince', True)
    object2.setSoloArtist(False)
    
    self.assertEqual(object1.getBandName(), 'Def Leppard')
    self.assertEqual(object2.getBandName(), 'Prince')
    self.assertTrue(object1.isSoloArtist())
    self.assertFalse(object2.isSoloArtist())
    
  def test_getByBandName(self):
    object = Band()
    self.assertTrue(object.getBy('band_name','Metallica'))
    self.assertNotEqual(object.getBandID(), '')
    self.assertEqual(object.getBandID(), 1)
    
  def test_getByBandID(self):
    object = Band()
    self.assertTrue(object.getBy('band_id', 1))
    self.assertNotEqual(object.getBandID(), '')
    self.assertEqual(object.getBandName(), 'Metallica')
    
  def test_getByError(self):
    object = Band()
    self.assertFalse(object.getBy('is_solo_artist', '1'))
    self.assertEqual(object.getBandID(), '')
    
  def test_SaveAndDeleteFromDatabase(self):
    object1 = Band('Spinal Tap')
    object1.addToDatabase()

    object2 = Band()
    self.assertTrue(object2.getBy('band_name', 'Spinal Tap'))
    self.assertNotEqual(object2.getBandID, '')
    object2.deleteFromDatabase()

    object3 = Band()
    self.assertFalse(object3.getBy('band_name', 'Spinal Tap'))
    self.assertEqual(object3.getBandID(), '')
    
  def test_isBandNameAvailable(self):
    object1 = Band('Metallica')
    object2 = Band('Spinal Tap Test')
    self.assertFalse(object1.isBandNameAvailable())
    self.assertTrue(object2.isBandNameAvailable())

  def test_saveToDatabase(self):
    object = Band()
    self.assertTrue(object.getBy('band_id', 4))
    self.assertFalse(object.isSoloArtist())
    self.assertTrue(object.setSoloArtist(True))
    self.assertTrue(object.saveToDatabase())
    self.assertTrue(object.isSoloArtist())
    self.assertTrue(object.setSoloArtist(False))
    self.assertTrue(object.saveToDatabase())
    self.assertFalse(object.isSoloArtist())   
    