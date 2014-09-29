####################
# Class: Video
# ------------
# used to contain all information relevant to a single video
# contains the frames data in a pandas dataframe
import os
import itertools
import random
import numpy as np
import pandas as pd
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
		#=====[ Get filestructure	]=====
		self.name = name
		data_dir = os.path.join(video_dir, 'data')
		self.data_dirs = {
			'jpeg':{'path':os.path.join(data_dir, 'JPEGImages'), 'ext':'.jpg'},
			'masks':{'path':os.path.join(data_dir, 'Masks'), 'ext':'.mat'},
			'cscores':{'path':os.path.join(data_dir, 'ClusterScores'), 'ext':'.pkl'},
			'cmasks':{'path':os.path.join(data_dir, 'ClusterMasks'), 'ext':'.pkl'},
			'cids':{'path':os.path.join(data_dir, 'ClusterIds'), 'ext':'.pkl'}
		}
		self.ensure_filesystem_structure()

		#=====[ Get names/paths	]=====
		self.frame_names = self.get_frame_names()
		self.data_paths = self.get_data_paths()

		#=====[ Get frames	]=====
		self.frames = self.get_frames()


	################################################################################
	####################[ Setup	]###################################################
	################################################################################

	def ensure_filesystem_structure(self):
		"""
			makes sure that all the necessary directories contained in 
			self.data_dirs exist 
		"""
		for datatype, d in self.data_dirs.items():
			if not os.path.exists(d['path']):
				os.mkdir(d['path'])


	def get_frame_names(self):
		"""
			analyzes the jpeg directory to find the frame names
		"""
		jd = self.data_dirs['jpeg']['path']
		jpeg_paths = sorted([os.path.join(jd, name) for name in os.listdir(jd) if name.endswith('.jpg')])
		return [os.path.split(p)[-1].split('.')[0] for p in jpeg_paths]


	def get_data_paths(self):
		"""
			sets self.frame_datapaths
		"""
		path_list = []
		for frame_name in self.frame_names:
			paths = {datatype:os.path.join(d['path'], frame_name + d['ext']) for datatype, d in self.data_dirs.items()}
			paths['name'] = frame_name
			path_list.append(paths)
		self.frame_datapaths = pd.DataFrame(path_list)
		self.frame_datapaths['clusters_exist'] = self.frame_datapaths['masks'].apply(os.path.exists)
		self.frame_datapaths['decoupled'] = self.frame_datapaths['cscores'].apply(os.path.exists)


	def get_frames(self):
		"""
			sets self.frames to a list of Frame objects with associated data 
		"""
		self.frames = [Frame(row) for ix, row in self.frame_datapaths.iterrows()] 






	################################################################################
	####################[ Frame Data	]###########################################
	################################################################################

	def get_num_frames(self):
		"""
			returns number of frames
		"""
		return len(self.frame_datapaths)


	def get_num_clustered_frames(self):
		"""
			returns number of frames that are complete 
			(i.e. they have both a 'jpeg' and a 'mask')
		"""
		return sum(self.frame_datapaths['clusters_exist'])


	def get_num_decoupled_frames(self):
		"""
			returns the number of frames that are 'decoupled' (i.e. masks and clusters)
			reside in separate files 
		"""
		return sum(self.frame_datapaths['decoupled'])


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
		return self.get_frame(random.choice(range(self.get_num_clustered_frames())))


	def iter_frames(self):
		"""
			iterates over all frames and *loads* them
		"""
		for t in range(len(self.frames)):
			return self.get_frame(t)







	################################################################################
	####################[ Interface 	]###########################################
	################################################################################

	def __str__(self):
		"""
			prints out stats on contained frames
		"""
		return """
=====[ Video: %s ]=====
# Frames: %d
# Complete Frames: %d
""" % (self.name, self.get_num_frames(), self.get_num_complete_frames())






