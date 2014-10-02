'''
Script: make_mongodb_database.py
================================

Description:
------------
	
	This script allows one to convert data as it appears in its processed form (after format_data.py)
	to a mongodb database accessible by the StorageDelegate class. This provides a significant speedup 
	and flexible schema for storing data.


Usage: 
------

	python make_mongodb_database.py -i [input_directory]

	i.e.

	python format_data.py 	-i ~/data/robobrain/recipewatch/data \


Args:
-----

	-i (--input_dir): path to source data directory on local filesystem


##############
Jay Hack
Fall 2014
jhack@stanford.edu
##############
'''
import os
import shutil
import sys
import argparse
from pprint import pprint
from scipy.io import loadmat
import numpy as np
from pymongo import MongoClient


if __name__ == '__main__':

	#==========[ ARGPARSING	]==========
	parser = argparse.ArgumentParser(description="Parse format_data.py arguments")
	parser.add_argument(	'-i', '--input_dir',
							metavar='I', type=str, nargs=1, dest='input_dir', required=True,
							help='path to source data (local filesystem)', 
							action='store')
	args = parser.parse_args ()
	input_dir = args.input_dir[0]
	if not os.path.exists(input_dir):
		raise Exception("make sure that input and output directories are actual paths")
	input_dir = os.path.join(input_dir, 'videos')


	#=====[ Setup MongoDB	]=====
	client = MongoClient()
	db = client.RecipeWatchDB
	videos = db.videos


	#=====[ Insert Videos ]===
	for video_name in [v for v in os.listdir(input_dir) if not v.startswith('.')]:
		video = {'name':video_name, '_id':video_name}
		video['root_dir'] = os.path.join(input_dir, video_name)
		video['frames_dir'] = os.path.join(input_dir, video_name, 'frames')
		video['frames'] = []
		pprint(video)
		for frame_name in sorted(os.listdir(video['frames_dir'])):
			frame_dir = os.path.join(video['frames_dir'], frame_name)
			image_path = os.path.join(frame_dir, 'image.jpg')
			masks_path = os.path.join(frame_dir, 'masks.npy')
			scores_path = os.path.join(frame_dir, 'scores.npy')
			scores = np.load(open(scores_path, 'r'))
			frame = {'root_dir':frame_dir, 'image_path':image_path, 'masks_path':masks_path, 'scores':scores, 'name':frame_name, '_id':frame_name}
			pprint(frame)
			video['frames'].append(frame)
		db.videos.insert(video)









