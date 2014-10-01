
# coding: utf-8

## Demo 1: Visualizing Images

# This demo will walk you through how to load in relevant data and how to visualize masks on images.

# In[1]:

from pprint import pprint
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
get_ipython().magic(u'pylab inline')

from RecipeWatchRelated import *


# Loading Data:
# -------------
# You can gain access to the data in its current storage format through the *StorageDelegate* class. It takes a single, optional argument, *data_dir*, that specifies the location of the directory containing all the data. (This is, by default, $PROJECT_DIR/data/cpmc/CPMC, where $PROJECT_DIR is set in configure.sh)

# In[2]:

sd = StorageDelegate()
videos = sd.videos
print '===[ Indexed Videos: ]==='
pprint(videos.keys())


# Viewing/Visualizing Frames
# --------------------------
# you can access a given video using *sd.get_video(video_name)* or *sd.get_random_video()*; likewise, you can access frames from videos using *video.get_frame(timestep)* or *video.get_random_frame()*. Printing a video to stdout will provide some baseline statistics on it

# In[3]:

video = sd.get_video('cpmc_UMiCy8EH1go')
frame = video.get_random_frame()
print video


# In[4]:

# Visualize the raw frame:
plt.imshow(frame.visualize_raw())


# In[5]:

# Visualize the frame with the 0th mask applied
plt.imshow(frame.visualize_mask(0))


# In[5]:



