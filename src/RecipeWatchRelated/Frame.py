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

	def __init__(self, image_path=None, masks_and_scores_path=None):
		"""
			given a frame as represented in frame_dict, this will 
		"""
		self.image_path = image_path
		self.masks_path = masks_and_scores_path
		self.scores_path = masks_and_scores_path

		#=====[ Properties	]=====
		self._image = None
		self._masks = None
		self._scores = None
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
	def scores(self):
		"""
			Scores representing the object-ness of the masks 
			scores[i] = objectness of masks[i]
		"""
		if self._scores is None and not self.scores_path is None:
			self._scores = loadmat(self.scores_path, variable_names=['scores'])['scores']
		return self._scores


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


	def top_n_masks(self, n):
		"""
			returns *list* of top n masks as:
				[(mask_ix, mask) ...]
		"""
		ordered_ixs = np.argsort(self.scores[:,0])[::-1]
		return [(i, self.get_mask(i)) for i in ordered_ixs[:n]]


	def extract_object(self, mask):
		"""
			given a mask representing an object, returns the region 
			of the image that contains the object 
		"""
		nonzero_ixs = np.argwhere(mask)
		min_x, max_x = np.min(nonzero_ixs[:,0]), np.max(nonzero_ixs[:,0])
		min_y, max_y = np.min(nonzero_ixs[:,1]), np.max(nonzero_ixs[:,1])		
		return self.image[min_x:max_x, min_y:max_y, :]


	def top_n_cropped_object_proposals(self, n=10):
		"""
			returns the top n object proposals, cropped 
		"""
		return [(ix, self.extract_object(m)) for ix, m in self.top_n_masks(n)]



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


