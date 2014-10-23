####################
# Class: Video
# ------------
# used to contain all information relevant to a single video
# contains the frames data in a pandas dataframe
####################
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

			video = Video(video_dict)
			for frame in video.iter_frames():
				...
			frame_000 = video.get_frame(0)
			frame_xxx = video.get_random_frame()
			print frame
	"""

	def __init__(self, video_dict):
		"""
			video_dict = a dictionary containing video data, as contained in 
			mongodb 
		"""
		#=====[ Get filestructure	]=====
		self.name = video_dict['name']
		self.root_dir = video_dict['root_dir']
		self.frames_dir = video_dict['frames_dir']
		self.frames_df = self.get_frames_df(video_dict['frames'])


	def get_frames_df(self, frames_list):
		"""
			returns a dataframe containing sorted frames and paths to their respective 
			data
		"""
		df = pd.DataFrame(frames_list)
		df['_id'] = df['_id'].astype(int)
		df.index = df['_id']
		df.sort(inplace=True)
		df['processed'] = df['masks_and_scores_path'].notnull()
		return df



	################################################################################
	####################[ Frame Data	]###########################################
	################################################################################

	def get_num_frames(self):
		"""
			returns number of frames
		"""
		return len(self.frames_df)


	def get_num_processed_frames(self):
		"""
			returns number of frames that are complete 
			(i.e. they have both a 'jpeg' and a 'mask')
		"""
		return self.frames_df['processed'].sum()


	def get_frame(self, t):
		"""
			returns Frame object occurring at timestep t, loaded
			returns None if t is too large. 
			Note: t is 1-indexed
		"""
		if t > len(self.frames_df) - 1:
			return None
		else:
			row = self.frames_df.loc[t]
			return Frame(t, row['root_dir'])


	def get_random_frame(self):
		"""
			returns random Frame object from this video, with the 
			requirement that it's 'processed'
		"""
		processed_df = self.frames_df[self.frames_df['processed']]
		return self.get_frame(random.choice(processed_df['_id']))


	def iter_frames(self):
		"""
			iterates over all frames and *loads* them
		"""
		for ix, row in self.frames_df.iterrows():
			yield self.get_frame(ix)





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
# Processed Frames: %d
""" % (self.name, self.get_num_frames(), self.get_num_processed_frames())






