####################
# Class: Video
# ------------
# used to contain all information relevant to a single video
import os
import itertools
from scipy.ndimage import imread
from scipy.io import loadmat
import numpy as np

class Video:

	def __init__(self, name, video_dir):
		self.name = name
		self.video_dir = video_dir
		self.data_dir = os.path.join(video_dir, 'data')
		self.frames_dir = os.path.join(self.data_dir, 'JPEGImages')
		self.masks_dir = os.path.join(self.data_dir, 'Masks')

		self.frame_paths = sorted([os.path.join(self.frames_dir, name) for name in os.listdir(self.frames_dir) if name.endswith('.jpg')])
		self.mask_paths = sorted([os.path.join(self.masks_dir, name) for name in os.listdir(self.masks_dir) if name.endswith('.mat')])



	def load_all(self):
		"""
			Loads video data into memory
			sets self.frames, self.masks to lists of numpy matrices
			Warning: takes time and memory
		"""
		if len(self.frame_paths) != len(self.mask_paths):
			print "Warning: in video %s, # frames != # masks (%d and %d)" % (self.name, len(self.frame_paths, len(self.mask_paths)))
		self.frames = [imread(p) for p in self.frame_paths]
		self.masks = [loadmat(p) for p in self.mask_paths]


	def names_match(self, frame_path, mask_path):
		"""
			returns true if the frame and the mask refer to the same timestep
			also returns true if either is None
		"""
		def get_name(p):
			return os.path.split(p)[-1].split('.')[0]
		return (get_name(frame_path) == get_name(mask_path)) or (frame_path == None) or (mask_path == None)


	def get_frame_mask(self, t):
		"""
			given timestep t, returns frame, mask as numpy arrays
			returns None if t is longer than either
		"""
		#====[ Step 1: get names ]=====
		frame_path = self.frame_paths[t] if t < len(self.frame_paths) else None
		mask_path = self.mask_paths[t] if t < len(self.mask_paths) else None
		assert self.names_match(frame_path, mask_path)

		#=====[ Step 2: load and return (if they exist) ]=====
		frame = imread(frame_path) if frame_path else None
		mask = loadmat(mask_path) if mask_path else None 
		return frame, mask


	def iter_frames(self):
		"""
			iterates over all (frame, mask) pairs available
		"""
		for t in range(min(len(self.frame_paths), len(self.mask_paths))):
			yield self.get_frame_mask(t)




