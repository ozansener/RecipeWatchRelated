####################
# Class: Frame
# ------------
# used to contain all information relevant to a single frame
# (includes masks, etc.)
####################
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
	def __init__(self, path_row):
		"""
			given a pandas series containing paths to data elements, creates 
			the frame
		"""
		self.paths = dict(path_row)
		self.loaded = {k:False for k in self.paths.keys()}


	################################################################################
	####################[ Loading 	]###############################################
	################################################################################

	def load_jpeg(self):
		"""
			loads the jpeg portion 
		"""
		if not self.loaded['jpeg']:
			self.jpeg = imread(self.jpeg_path) if self.jpeg_path else None
			self.loaded['jpeg'] = True

	def load_mask(self):
		"""
			loads the jpeg portion 
		"""
		if not self.loaded['mask']:
			self.mask = imread(self.mask_path) if self.mask_path else None
			self.loaded['mask'] = True

	def load_pkl(self, datatype):
		"""
			loads any of the pickled datatypes
		"""
		if not self.loaded['datatype']:
			self.loaded['datatype'] = True
			return pickle.load(open(self.paths['cscores'], 'r'))

	def load_cscores(self):
		self.cscores = self.load_pkl('cscores')

	def load_cmasks(self):
		self.cmasks = self.load_pkl('cmasks')

	def load_cids(self):
		self.cids =  self.load_pkl('cids')				


	def load(self):
		"""
			loads all associated data
		"""
		self.load_mask()
		self.load_pkl()
		self.load_cscores()
		self.load_cmasks()
		self.load_cids()






	################################################################################
	####################[ Masks 	]###############################################
	################################################################################

	def get_mask(self, mask_id):
		"""
			returns the mask_id-th mask
		"""
		return self.masks['masks'][:,:,mask_id]


	def apply_mask(self, jpeg, mask):
		"""
			multiplies the mask into the jpeg 
		"""
		masked = jpeg.copy()
		masked[(mask == 0)] = 0
		return masked


	def visualize_mask(self, mask_id):
		"""
			returns a numpy array with the ith mask
			applied 
		"""
		if not self.is_loaded:
			self.load()
		return self.apply_mask(self.jpeg, self.get_mask(mask_id))


	def visualize_masks(self):
		"""
			returns a numpy array with all masks labelled
		"""
		raise NotImplementedError

