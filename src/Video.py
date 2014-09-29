####################
# Class: Video
# ------------
# used to contain all information relevant to a single video
import os
import itertools
import random
import numpy as np
from Frame import *

class Video:
	"""
		Ideal Usage:
		------------

			video = Video('video_1', '//path/to/video/data')
			for frame in video.iter_frames():
				...
			frame_000 = video.get_frame(0)
			frame_xxx = video.get_random_frame()
			print frame
	"""


	def __init__(self, name, video_dir):
		"""
			sets self.frames to a list of Frame objects, as defined in Frame.py;
			does not load in any data, however
		"""
		self.name = name
		self.video_dir = video_dir
		self.data_dir = os.path.join(video_dir, 'data')
		self.jpeg_dir = os.path.join(self.data_dir, 'JPEGImages')
		self.mask_dir = os.path.join(self.data_dir, 'Masks')

		self.jpeg_paths = sorted([os.path.join(self.jpeg_dir, name) for name in os.listdir(self.jpeg_dir) if name.endswith('.jpg')])
		self.mask_paths = sorted([os.path.join(self.mask_dir, name) for name in os.listdir(self.mask_dir) if name.endswith('.mat')])
		self.frames = [Frame(jp, mp) for jp, mp in itertools.izip_longest(self.jpeg_paths, self.mask_paths)]


	def get_num_frames(self):
		"""
			returns number of frames
		"""
		return len(self.frames)


	def get_num_complete_frames(self):
		"""
			returns number of frames that are complete 
			(i.e. they have both a 'jpeg' and a 'mask')
		"""
		return sum([f.is_complete() for f in self.frames])


	def get_frame(self, t):
		"""
			returns Frame object occurring at timestep t, loaded
			returns None if t is too large.
		"""
		if t > len(self.frames):
			return None
		else:
			frame = self.frames[t]
			frame.load()
			return frame


	def get_random_frame(self):
		"""
			returns random Frame object from this video, with the 
			requirement that it's 'complete'
		"""
		return self.get_frame(random.choice(range(self.get_num_complete_frames())))


	def iter_frames(self):
		"""
			iterates over all frames and *loads* them
		"""
		for t in range(len(self.frames)):
			return self.get_frame(t)



	def __str__(self):
		"""
			prints out stats on contained frames
		"""
		return """
=====[ Video: %s ]=====
# Frames: %d
# Complete Frames: %d
""" % (self.name, self.get_num_frames(), self.get_num_complete_frames())






