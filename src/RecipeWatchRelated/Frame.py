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

	def __init__(self, image_path=None, masks_path=None):
		"""
			given a frame as represented in frame_dict, this will 
		"""
		self.image_path = image_path
		self.masks_path = masks_path

		#=====[ Properties	]=====
		self._image = None
		self._masks = None
		self._superpixels = None 



	################################################################################
	####################[ Properties 	]###########################################
	################################################################################

	@property
	def image(self):
		"""
			Original image 
			Type: Numpy array, 2d
		"""
		if self._image is None and not self.image_path is None:
			self._image = imread(self.image_path)
		return self._image

	@property
	def masks(self):
		"""
			Masks representing object proposals 
			Type: Numpy array, 3d (3rd dimension indexes the objects)
		"""
		if self._masks is None and not self.masks_path is None:
			self._masks = loadmat(self.masks_path, variable_names=['masks'])['masks']
		return self._masks


	@property
	def superpixels(self):
		"""
			Image superpixels 
			Type: Numpy array, 3d
		"""
		if self._superpixels is None and not self.image is None:
			 self._superpixels = slic(self.image, n_segments=250, compactness=10)
		return self._superpixels






	################################################################################
	####################[ Masks 	]###############################################
	################################################################################

	def get_mask(self, mask_id):
		"""
			returns the mask_id-th mask
		"""
		return self.masks[:,:,mask_id]


	def apply_mask(self, image, mask):
		"""
			multiplies the mask into the image 
		"""
		masked = self.image.copy()
		masked[(mask == 0)] = 0
		return masked






	################################################################################
	####################[ Visualzation 	]###########################################
	################################################################################

	def visualize_raw(self):
		"""
			returns the raw image as numpy array
		"""
		return self.image


	def visualize_mask(self, mask_id):
		"""
			visualizes only the 'mask_id'th mask
		"""
		return self.apply_mask(self.image, self.get_mask(mask_id))


	def visualize_superpixel(self, superpix_id):
		"""
			visualizes 'superpix_id'th superpixel
		"""
		img = self.image.copy()
		img[self.superpixels != superpix_id] = 0
		return img


	def visualize_superpixels(self):
		"""
			visualizes all superpixels together on the image 
			returns the image itself
		"""
		return mark_boundaries(self.image, self.superpixels)


