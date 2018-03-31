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
    object = Band()
    object.new('Spinal Tap')
    self.assertEqual(object.getBandID(), '')
    self.assertEqual(object.getBandName(), 'Spinal Tap')
    self.assertFalse(object.isSoloArtist())
    
  def test_toJSON(self):
    object = Band()
    object.new('Spinal Tap')
    self.assertEqual(object.toJSON(), "{ band_id: , band_name: 'Spinal Tap', is_solo_artist: 'False' }")
    
  def test_mutators_and_accessors(self):
    object1 = Band()
    object1.setBandName('Def Leppard')
    object1.setSoloArtist(False)

    object2 = Band()
    object2.setBandName('Prince')
    object2.setSoloArtist(True)
    
    self.assertEqual(object1.getBandName(), 'Def Leppard')
    self.assertEqual(object2.getBandName(), 'Prince')
    self.assertFalse(object1.isSoloArtist())
    self.assertTrue(object2.isSoloArtist())
    
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
    object1 = Band()
    object1.new('Spinal Tap')
    object1.addToDatabase()

    object2 = Band()
    self.assertTrue(object2.getBy('band_name', 'Spinal Tap'))
    self.assertNotEqual(object2.getBandID, '')
    object2.deleteFromDatabase()

    object3 = Band()
    self.assertFalse(object3.getBy('band_name', 'Spinal Tap'))
    self.assertEqual(object3.getBandID(), '')
    
  def test_isBandNameAvailable(self):
    object = Band()
    self.assertFalse(object.isBandNameAvailable('Metallica'))
    self.assertTrue(object.isBandNameAvailable('Spinal Tap'))

    