Usage:
python SmearingEffectOnRatio.py

You need ROOT compiled with python, i.e. PyROOT enabled when configuring ROOT before make from source code.
You can always easilly add this by following
http://root.cern.ch/drupal/content/pyroot

Or by setting up root e.g. on lxplus:
export PATH="/afs/cern.ch/sw/lcg/external/Python/2.6.5/x86_64-slc5-gcc43-opt/bin:$PATH"
export PYTHONDIR=/afs/cern.ch/sw/lcg/external/Python/2.6.5/x86_64-slc5-gcc43-opt/
export LD_LIBRARY_PATH="/afs/cern.ch/sw/lcg/external/Python/2.6.5/x86_64-slc5-gcc43-opt/lib:$LD_LIBRARY_PATH"
. /afs/cern.ch/sw/lcg/external/gcc/4.3.2/x86_64-slc5/setup.sh
rootversion=5.30.04
. /afs/cern.ch/sw/lcg/app/releases/ROOT/${rootversion}/x86_64-slc5-gcc43-opt/root/bin/thisroot.sh
export LD_LIBRARY_PATH="/afs/cern.ch/sw/lcg/external/Python/2.6.5/x86_64-slc5-gcc43-opt/lib/python2.6/lib-dynload/:$LD_LIBRARY_PATH"

You can also always install afs on your laptop:)
http://akorneev.web.cern.ch/akorneev/howto/openafs.txt




