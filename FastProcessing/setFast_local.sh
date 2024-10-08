#!/bin/bash

# source ROOT
#source /home/hamal/Projects/root_v6.32.04/bin/thisroot.sh
# source /opt/ROOT/v6.32.04/bin/thisroot.sh

# set FAST framework - set FAST_SW
#export FAST_ROOT=$HOME/Projects/FAST/example/FastFramework
export FAST_ROOT=`pwd`/FastFramework
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:$FAST_ROOT/lib
