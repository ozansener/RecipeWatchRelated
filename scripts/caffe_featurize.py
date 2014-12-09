'''
Script: caffe_featurize.py
==========================

Description:
------------
	
	Featurizes every available frame using the CaffeCNN class


Usage: 
------

	python caffe_featurize.py


##############
Jay Hack
Fall 2014
jhack@stanford.edu
##############
'''
import click
import os
import shutil
import sys
import argparse
from pprint import pprint
from scipy.io import loadmat
import numpy as np
from pymongo import MongoClient

from ModalDB import *
from RecipeWatchRelated.CaffeCNN import CaffeCNN

@click.command()
@click.option('--dbpath', help='path to directory containing data')
@click.option('--schema_file', help='import location of python dict containing schema. Ex: myproject.schema', default=None)
def caffe_featurize(dbpath, schema_file):
	"""
		Configures/initializes the mongodb database
	"""
	#=====[ Step 1: Connect to ModalDB	]=====
	click.echo("---> Connecting to DB")
	schema = __import__(schema_file).Schema
	client = ModalClient(root=dbpath, schema=schema)

	#=====[ Step 2: Create CaffeCNN 	]=====
	click.echo("---> Creating CaffeCNN")
	caffe = CaffeCNN()

	#=====[ Step 3: Featurize every video	]=====
	click.echo("---> Beginning featurization")
	for video in client.iter(Video):
		click.echo(str(video))

		for frame in video.iter_children(Frame):
			click.echo("	---> featurizing " + str(frame))
			frame['cnn_features'] = caffe.featurize_frame(frame)




if __name__ == '__main__':
	caffe_featurize()









