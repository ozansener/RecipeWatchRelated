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
from pymongo import MongoClient
from Video import *


class StorageDelegate:


	####################################################################################################
	######################[ --- INTERNALS --- ]#########################################################
	####################################################################################################

	def __init__ (self):
		
		#=====[ Setup DB	]=====
		self.mongo_client = MongoClient()
		self.db = self.mongo_client.RecipeWatchDB
		self.videos = self.db.videos


	####################################################################################################
	######################[ --- INTERFACE --- ]#########################################################
	####################################################################################################


	def get_video(self, video_name):
		"""
			returns the named video (unloaded)
		""" 
		return Video(self.videos.find_one(spec_or_id=video_name))


	def get_random_video(self):
		"""
			returns a random video (unloaded)
		"""
		return Video(self.videos.find_one())


	def iter_videos(self):
		"""
			iterates over all videos 
		"""
		cursor = self.db.videos.find()
		for i in range(cursor.count()):
			yield Video(cursor.next())


	






