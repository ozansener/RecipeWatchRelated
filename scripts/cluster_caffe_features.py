'''
Script: cluster_caffe_features.py
=================================

Description:
------------
	
	Given a matrix containing the clusters from 


Usage: 
------

	python gather_caffe_features.py


##############
Jay Hack
Fall 2014
jhack@stanford.edu
##############
'''
import os
import numpy as np
from sklearn.cluster import KMeans
from RecipeWatchRelated import *

data_dir = '/Users/jayhack/Academics/CS/RoboBrain/Code/RecipeWatchRelated/data'

if __name__ == '__main__':

	print '---> Loading feature vecs'
	X = np.load(os.path.join(data_dir, 'feature_vecs.npy'))
	print '---> Starting KMeans'
	km = KMeans(n_clusters=25, verbose=1, n_jobs=1)
	print '---> Fitting KMeans'
	cluster_ids = km.fit_predict(X)
	np.save(os.path.join(data_dir, 'cluster_ids'), cluster_ids)
