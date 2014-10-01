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

	python format_data.py -s [src_directory] -d [dest_directory]

	i.e.

	python format_data.py 	-s ~/data/robobrain/recipewatch/raw_data \
							-d ~/data/robobrain/recipewatch/data


Args:
-----

	-s (--source): path to source data directory on local filesystem
	-d (--dest): path to output directory on local filesystem


##############
Jay Hack
Fall 2014
jhack@stanford.edu
##############
'''
import os
import sys
import argparse


if __name__ == '__main__':

	#==========[ ARGPARSING	]==========
	parser = argparse.ArgumentParser(description="Parse format_data.py arguments")
	parser.add_argument(	'-p', '--profile_type', 
							metavar='P', type=str, nargs=1, dest='dataset', required=True,
							help='type of social media profiles to be convered. Currently "linkedin" or "quora"')
	parser.add_argument(	'-i', '--input_dir',
							metavar='I', type=str, nargs=1, dest='input_dir', required=True,
							help='path to source data (local filesystem)')
	parser.add_argument(	'-o', '--output_dir',
							metavar='O', type=str, nargs=1, dest='output_dir', required=True,
							help='path to output directory (local filesystem)') 
	args = parser.parse_args ()


	#=====[ Deal with Source Directory	]=====
	print args



