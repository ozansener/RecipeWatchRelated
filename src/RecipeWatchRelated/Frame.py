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
from skimage.segmentation import slic, find_boundaries

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
	datatypes = ['image', 'masks', 'scores', 'segments']
	loaded = {d:None for d in self.datatypes}
	paths = {d:None for d in self.datatypes}
	get_funcs = {
					'image':lambda path: imread(self.paths['image']) if self.paths['image'] else None,
					'masks':lambda path: loadmat(self.paths['masks'], variable_names=['masks'])['masks'] if self.paths['image'] else None,
					'scores':lambda path: loadmat(self.paths['scores'], variable_names=['scores'])['scores'] if self.paths['scores'] else None,
					'segments':lambda: slic(self.data['image'], n_segments=250, compactness=100) if self.loaded['image'] else None
				}
	data = {d:None for d in self.datatypes}


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






	################################################################################
	####################[ Loading 	]###############################################
	################################################################################

	def get_datatypes(self, datatypes):
		"""
			fills self.data with data of all types named in 'datatypes'
		"""
		if type(datatypes) == list:
			self.get_datatypes(d) for d in datatypes
		datatype = datatypes
		if not self.loaded[datatype]:
			self.data[datatype] = self.get_funcs(datatype)
		self.loaded[datatype] = True



	def load(self):
		"""
			loads all associated data
		"""
		self.get_datatypes(self.datatypes)






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






	################################################################################
	####################[ Masks 	]###############################################
	################################################################################

	def visualize_segment(self, seg_id):
		"""
			visualizes the ith segment
			returns the image itself 
		"""
		self.get_datatypes(['image', 'segment'])
		img = self.data['image'].copy()
		img[self.data['segments'] != seg_id] = 0
		return img


	def visualize_segments(self):
		"""
			visualizes all segments together on the image 
			returns the image itself
		"""
		self.get_datatypes(['image', 'segment'])
		img = self.data['image'].copy()
		boundaries = find_boundaries(self.data['segments'])
		img[boundaries == True] = 0
		return img


