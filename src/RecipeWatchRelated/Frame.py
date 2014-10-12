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
from skimage.segmentation import slic, find_boundaries, mark_boundaries

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
			plt.imshow(f.visualize_superpixel())
	"""
	datatypes = ['image', 'masks', 'scores', 'superpixels']
	loaded = {d:None for d in datatypes}
	paths = {d:None for d in datatypes}
	data = {d:None for d in datatypes}


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
		self.get_funcs = {
				'image':self.get_image,
				'masks':self.get_masks,
				'scores':self.get_scores,
				'superpixels':self.get_superpixels
			}

	def get_image(self):
		return imread(self.paths['image']) if self.paths['image'] else None

	def get_masks(self):
		return loadmat(self.paths['masks'], variable_names=['masks'])['masks'] if self.paths['masks'] else None

	def get_scores(self):
		return loadmat(self.paths['scores'], variable_names=['scores'])['scores'] if self.paths['scores'] else None

	def get_superpixels(self):
		return slic(self.data['image'], n_segments=250, compactness=10) if self.loaded['image'] else None





	################################################################################
	####################[ Loading 	]###############################################
	################################################################################

	def get_datatypes(self, datatypes):
		"""
			fills self.data with data of all types named in 'datatypes'
		"""
		if type(datatypes) == list:
			for d in datatypes:
				self.get_datatypes(d)
			return
		datatype = datatypes
		if not self.loaded[datatype]:
			self.data[datatype] = self.get_funcs[datatype]()
		self.loaded[datatype] = True


	def get_all_datatypes(self):
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






	################################################################################
	####################[ Visualzation 	]###########################################
	################################################################################

	def visualize_raw(self):
		"""
			returns the raw image as numpy array
		"""
		self.get_datatypes(['image'])
		return self.data['image']


	def visualize_mask(self, mask_id):
		"""
			visualizes only the 'mask_id'th mask
		"""
		self.get_datatypes(['image', 'masks'])
		return self.apply_mask(self.data['image'], self.get_mask(mask_id))


	def visualize_superpixel(self, superpix_id):
		"""
			visualizes 'superpix_id'th superpixel
		"""
		self.get_datatypes(['image', 'superpixels'])
		img = self.data['image'].copy()
		img[self.data['superpixels'] != superpix_id] = 0
		return img


	def visualize_superpixels(self):
		"""
			visualizes all superpixels together on the image 
			returns the image itself
		"""
		self.get_datatypes(['image', 'superpixels'])
		return mark_boundaries(self.data['image'], self.data['superpixels'])


