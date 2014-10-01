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
		self.load_funcs = 	{	
								'jpeg':imread,
								'masks':loadmat
							}
		self.loaded = {k:False for k in self.paths.keys()}
		self.data = {k:None for k in self.paths.keys()}


	################################################################################
	####################[ Loading 	]###############################################
	################################################################################

	def load_datatype(self, datatype):
		"""
			loads the specified datatype 
		"""
		if not self.loaded[datatype]:
			self.data[datatype] = self.load_funcs[datatype](self.paths[datatype])
			self.loaded[datatype] = True	


	def load(self):
		"""
			loads all associated data
		"""
		self.load_datatype('jpeg')
		self.load_datatype('masks')






	################################################################################
	####################[ Masks 	]###############################################
	################################################################################

	def get_mask(self, mask_id):
		"""
			returns the mask_id-th mask
		"""
		return self.data['masks']['masks'][:,:,mask_id]


	def apply_mask(self, jpeg, mask):
		"""
			multiplies the mask into the jpeg 
		"""
		masked = jpeg.copy()
		masked[(mask == 0)] = 0
		return masked


	def visualize_raw(self):
		"""
			returns a numpy array with no masks 
			applied 
		"""
		if not self.loaded['jpeg']:
			self.load_datatype['jpeg']
		return self.data['jpeg']


	def visualize_mask(self, mask_id):
		"""
			returns a numpy array with the ith mask
			applied 
		"""
		if not self.loaded['jpeg'] and self.loaded['masks']:
			self.load()
		return self.apply_mask(self.data['jpeg'], self.get_mask(mask_id))


	def visualize_masks(self):
		"""
			returns a numpy array with all masks labelled
		"""
		raise NotImplementedError

