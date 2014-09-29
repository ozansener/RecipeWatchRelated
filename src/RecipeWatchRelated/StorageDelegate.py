#####################
# Module: StorageDelegate
# =======================
# manages data input/output
#
# Ideal Usage:
# ------------
# 
# 
import os
import sys
import random
import pandas as pd
import numpy as np
from Video import *


class StorageDelegate:


	####################################################################################################
	######################[ --- INTERNALS --- ]#########################################################
	####################################################################################################

	def __init__ (self, data_dir=os.path.join(os.getcwd(), '../../data/cpmc/CPMC')):
		self.data_dir = data_dir
		self.video_dirs = self.get_video_dirs(self.data_dir)
		self.videos = self.get_videos(self.video_dirs)


	def get_video_dirs(self, data_dir):
		"""
			given cpmc_dir, returns list of full paths to individual dirs
		"""
		return {d:os.path.join(data_dir, d) for d in os.listdir(data_dir) if not d.startswith('.')}


	def get_videos(self, video_dirs):
		"""
			returns dict: VideoName -> Video
		"""
		return {name:Video(name, video_dir) for name, video_dir in video_dirs.items()}




	####################################################################################################
	######################[ --- INTERFACE --- ]#########################################################
	####################################################################################################


	def get_video(self, video_name):
		"""
			returns the named video (unloaded)
		""" 
		if not video_name in self.videos.keys():
			raise Exception("No video named %s in listed videos")
		else:
			return self.videos[video_name]


	def get_random_video(self):
		"""
			returns a random video (unloaded)
		"""
		return self.get_video(random.choice(self.videos.keys()))


	






