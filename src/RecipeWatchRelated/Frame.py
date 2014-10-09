####################
# Class: Frame
# ------------
# used to contain all information relevant to a single frame
# (includes masks, etc.)
####################
import os
import numpy as np
import scipy as sp
from scipy.ndimage import imread
from scipy.io import loadmat
from skimage.segmentation import slic

class Frame:
	"""
		Ideal Usage:
		------------

			f = Frame(frame_dict)
			f.load()
			plt.imshow(f.visualize_mask(i))
				...
			plt.imshow(f.visualize_masks())
				...
	"""
	data_types = ['image', 'masks', 'scores', 'segments']
	load_funcs = {
					'image':lambda path: imread(path) if path else None,
					'masks':lambda path: loadmat(path, variable_names=['masks'])['masks'] if path else None,
					'scores':lambda path: loadmat(path, variable_names=['scores'])['scores'] if path else None,
				}


	def __init__(self, frame_dict):
		"""
			given a frame as represented in frame_dict, this will 
		"""
		self.index = frame_dict['_id']
		self.paths = {	
						'image':frame_dict['image_path'], 
						'masks':frame_dict['masks_and_scores_path'],
						'scores':frame_dict['masks_and_scores_path']
					}
		self.loaded = {k:False for k in self.data_types}
		self.data = {k:None for k in self.data_types}






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
		for datatype in self.data_types:
			self.load_datatype(datatype)



	def get_segments(self):
		"""
			finds segments 
		"""
		# assert self.loaded['image']
		self.data['segments'] = slic(self.data['image'], n_segments=250, compactness=100)



	################################################################################
	####################[ Masks 	]###############################################
	################################################################################

	def get_mask(self, mask_id):
		"""
			returns the mask_id-th mask
		"""
		return self.data['masks'][:,:,mask_id]


	def apply_mask(self, image, mask):
		"""
			multiplies the mask into the image 
		"""
		masked = self.data['image'].copy()
		masked[(mask == 0)] = 0
		return masked


	def visualize_raw(self):
		"""
			returns a numpy array with no masks 
			applied 
		"""
		if not self.loaded['image']:
			self.load_datatype('image')
		return self.data['image']


	def visualize_mask(self, mask_id):
		"""
			returns a numpy array with the ith mask
			applied 
		"""
		if not self.loaded['image']:
			self.load_datatype('image')
		if not self.loaded['masks']:
			self.load_datatype('masks')
		return self.apply_mask(self.data['image'], self.get_mask(mask_id))


	def visualize_masks(self):
		"""
			returns a numpy array with all masks labelled
		"""
		raise NotImplementedError


	def visualize_segment(self, seg_id):
		"""
			visualizes the ith segment 
		"""
		img = self.data['image'].copy()
		img[self.data['segments'] != seg_id] = 0
		return img

