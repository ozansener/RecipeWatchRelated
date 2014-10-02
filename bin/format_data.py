'''
Script: format_data.py
======================

Description:
------------
	
	This script allows one to convert data as it appears in the raw (original) 'cpmc' directory 
	to the format that the RecipeWatch program will use. Concretely, it goes from the original 
	storage format:

		cpmc/CPMC/data/
			cpmc_video_name_0/
				JPEGImages/
					frame_name_0.jpg
					...
				Masks/
					mask_name_0.mat
					...
			...

	to the desired format:

		data/videos/
			video_name_0/
				frame_name_0/
					image.jpeg 
					scores.pkl
					masks.pkl
				...
			...

	This allows for easier indexing and faster loading; most notably, it decouples the masks and 
	'objectness scores' for object candidates found within the image, so that they can be loaded 
	independently.



Usage: 
------

	python format_data.py -i [input_directory] -o [output_directory]

	i.e.

	python format_data.py 	-i ~/data/robobrain/recipewatch/raw_data \
							-o ~/data/robobrain/recipewatch/data


Args:
-----

	-i (--input_dir): path to source data directory on local filesystem
	-o (--output_dir): path to output directory on local filesystem


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

def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]


def make_video_dir(videos_dir, video_name):
	"""
		given a path, makes a video directory there in the following structure:
		video_name/
			frames/
		returns path to that video dir
	"""
	video_dir = os.path.join(videos_dir, video_name)
	if not os.path.isdir(video_dir):
		os.mkdir(video_dir)
	os.mkdir(os.path.join(video_dir, 'frames'))
	return video_dir


def setup_output_dir(output_dir, video_names):
	"""
		sets up the output directory to have one directory 
		for each video; returns a dict mapping video name -> video dir 
		path 
	"""
	#=====[ Step 1: make a clean 'video' folder]=====
	videos_dir = os.path.join(output_dir, 'videos')
	if os.path.exists(videos_dir):
		shutil.rmtree(videos_dir)
	os.mkdir(videos_dir)

	#=====[ Step 2: make individual video dirs	]=====
	output_video_dirs = {}
	for video_name in video_names:
		video_dir = make_video_dir(videos_dir, video_name)
		output_video_dirs[video_name] = video_dir
	return output_video_dirs







if __name__ == '__main__':

	#==========[ ARGPARSING	]==========
	parser = argparse.ArgumentParser(description="Parse format_data.py arguments")
	parser.add_argument(	'-i', '--input_dir',
							metavar='I', type=str, nargs=1, dest='input_dir', required=True,
							help='path to source data (local filesystem)', 
							action='store')
	parser.add_argument(	'-o', '--output_dir',
							metavar='O', type=str, nargs=1, dest='output_dir', required=True,
							help='path to output directory (local filesystem)', 
							action='store')
	args = parser.parse_args ()
	input_dir,output_dir = args.input_dir[0], args.output_dir[0]
	if not os.path.exists(input_dir) and os.path.exists(output_dir):
		raise Exception("make sure that input and output directories are actual paths")
	input_dir = os.path.join(input_dir, 'CPMC')


	#=====[ Step 1: get video_dirs ]=====
	"""
		video_dirs is a dict as follows:
			video_dirs: video_names -> (input_dir, output_dir)
	"""
	video_names = os.listdir(input_dir)
	input_video_dirs = {video_name:os.path.join(input_dir, video_name, 'data') for video_name in video_names}
	output_video_dirs = setup_output_dir(output_dir, video_names)
	video_dirs = {video_name:{} for video_name in video_names}
	for video_name in video_names:
		video_dirs[video_name]['input'] = input_video_dirs[video_name]
		video_dirs[video_name]['output'] = output_video_dirs[video_name]


	pprint(video_dirs)

	#=====[ Step 2: for each frame, transfer over the information	]=====
	for name, path in video_dirs.iteritems():

		#####[ Make a 	]#####
		pass










