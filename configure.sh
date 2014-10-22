export PROJECT_DIR=`pwd`
export MONGODB_DBPATH=`pwd`/data/db
export JAY_DATA_PATH=/Volumes/DeepStorage/Data/Robobrain/data
export PYTHONPATH=$PYTHONPATH:`pwd`/src/

#===[ Add Caffe to Path ]===
export CAFFE_ROOT_PATH=/Users/jayhack/CS/CV/caffe
export PYTHONPATH=$PYTHONPATH:$CAFFE_ROOT_PATH/python

#===[ Add DYLD_FALLBACK_LIBRARY_PATH So Caffe can find .dyld libraries ]===
export DYLD_FALLBACK_LIBRARY_PATH=/usr/local/cuda/lib:/usr/local/Cellar/hdf5/1.8.13/lib/:/usr/local/cuda/lib:/usr/local/Cellar/hdf5/1.8.13/lib/:/usr/local/cuda/lib:/Users/jayhack/anaconda/lib:/usr/local/lib:/usr/lib