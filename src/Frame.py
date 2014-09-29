####################
# Class: Frame
# ------------
# used to contain all information relevant to a single frame
# (includes masks, etc.)
import os
from scipy.ndimage import imread
from scipy.io import loadmat

class Frame:
	"""
		Ideal Usage:
		------------

			f = Frame(jpg_path, mask_path)
			f.load()
			plt.imshow(f.visualize_mask(i))
				...
			plt.imshow(f.visualize_masks())
				...
	"""
	def __init__(self, jpeg_path, mask_path):
		"""
			either jpeg_path or mask_path can be None if they don't exist
		"""
		assert self.names_match(jpeg_path, mask_path)
		self.jpeg_path = jpeg_path
		self.mask_path = mask_path
		self.is_loaded = False
	

	def names_match(self, jpeg_path, mask_path):
		"""
			returns true if the frame and the mask refer to the same timestep
			also returns true if either is None
		"""
		if (jpeg_path == None) or (mask_path == None):
			return True
		else:
			def get_name(p):
				return os.path.split(p)[-1].split('.')[0]
			return (get_name(jpeg_path) == get_name(mask_path))


	def is_complete(self):
		"""
			returns True if both jpeg_path and mask_path exist 
		"""
		return (self.jpeg_path != None) and (self.mask_path != None)


	def load(self):
		"""
			loads self.jpen and self.mask
		"""
		if not self.is_loaded:			
			self.jpeg = imread(self.jpeg_path) if self.jpeg_path else None
			self.masks = loadmat(self.mask_path) if self.mask_path else None
			self.is_loaded = True


	def visualize_mask(self, mask_id):
		"""
			returns a numpy array with the ith mask
			applied 
		"""
		raise NotImplementedError


	def visualize_masks(self):
		"""
			returns a numpy array with all masks labelled
		"""
		raise NotImplementedError

