######################################################
# A generic Makefile which does dependencies         #
# automatically                                      #
#                                                    #
# Original by Kurt Rinnert                           #
# Modified by Carl Gwilliam                          #
# Modified by Jiri Kvita                             #
# 1. Place in your top dir                           #
# 2. Change HEADERPAT and SRCPAT to your extension   #
#    naming (e.g. C cpp cxx h hh)                    #
# 3. Changeg LIBNAME to the wanted library name       #
# 4. Do 'gmake setup' to make dir structure and      #
#    copy files there:                               #
#    a. headers in include/                          #
#    b. source files in src/*.cpp                    #
#    c. program files (containing main) in src/*.cxx #
#                                                    #
######################################################

#directories
LIBDIR = lib
BINDIR = bin
INCDIR = include
BOOSTDIR = $(shell echo $BOOST_ROOT)
SRCDIR = src
PRGDIR = src
TMPDIR = tmp
BINOBJSDIR = $(TMPDIR)/bin
LIBOBJSDIR = $(TMPDIR)/lib
DEPSDIR    = $(TMPDIR)/deps

#paterns
HEADERPAT = h
SOURCEPAT = cpp
EXEPAT = cxx

#source files
INCLUDEFILES = $(wildcard $(INCDIR)/*.$(HEADERPAT))
LIBCPPFILES  = $(wildcard $(SRCDIR)/*.$(SOURCEPAT))
PRGCPPFILES  = $(wildcard $(PRGDIR)/*.$(EXEPAT))

#targets
LIBNAME = MyProject
LIB     = $(LIBDIR)/lib$(LIBNAME).a
LIBOBJS = $(subst $(SRCDIR),$(LIBOBJSDIR),$(subst .$(SOURCEPAT),.o,$(LIBCPPFILES)))
BINS    = $(subst $(PRGDIR),$(BINDIR),$(subst .$(EXEPAT),,$(PRGCPPFILES)))
BINOBJS = $(subst $(PRGDIR),$(BINOBJSDIR),$(subst .$(EXEPAT),.o,$(PRGCPPFILES)))
LIBDEPS = $(subst $(SRCDIR),$(DEPSDIR),$(LIBCPPFILES:.$(SOURCEPAT)=.d))
BINDEPS = $(subst $(PRGDIR),$(DEPSDIR),$(PRGCPPFILES:.$(EXEPAT)=.d))

#tools
CPP = g++ -std=c++11
LD  = g++ -std=c++11
AR  = ar
DEP = g++ -std=c++11

#flags
#CPPBASEFLAGS = -c -Wall -Werror -ansi -pedantic -I$(INCDIR)
CPPBASEFLAGS =  -c -Wall -I$(INCDIR) -I$(BOOSTDIR) 
DEPFLAGS = -MM -I$(INCDIR) -I$(shell root-config --incdir)

DEBUG=yes

ifeq ($(DEBUG),yes)
CPPDBGFLAGS = -g
else
CPPDBGFLAGS =
endif

ifeq ($(OPTIMIZE),yes)
CPPOPTFLAGS = -O2
else
CPPOPTFLAGS =
endif

ifeq ($(PROFILING),yes)
CPPPROFLAGS = -pg
else
CPPPROFLAGS =
endif

# orig:
# ROOTCPPFLAGS = $(shell root-config --cflags) -Wno-long-long 
ROOTCPPFLAGS = $(shell root-config --cflags) -Wno-long-long 

# default:
ROOTLDFLAGS  = $(shell root-config --libs) 

EXTRALIBSPATH=
# "$(shell echo ${delphespath})/libDelphes.so"

CPPFLAGS = $(CPPDBGFLAGS) $(CPPPROFLAGS) $(CPPOPTFLAGS) $(CPPBASEFLAGS) $(ROOTCPPFLAGS) -std=c++11

ARFLAGS = -rc

LDFLAGS = $(ROOTLDFLAGS) -lEG -lMinuit

ifeq ($(DEBUG),yes)
override LDFLAGS += -g 
endif
ifeq ($(PROFILING),yes)
override LDFLAGS += -pg 
endif

LOADLIBS = -L$(LIBDIR) -l$(LIBNAME)

# All depends on bin -> will "make" it if not up-to-date
all: bin
	echo "* all done."

# bin depends on static library (.a) for classes + binary objects for prgs (.o) + binaries for prgs
bin: $(LIB) $(BINOBJS) $(BINS) $(EXTRALIBSPATH)
# lib dependes on static library for classes (LIB).  Will "make" if not up-to-date
lib: $(LIB)

$(BINS):$(BINDIR)%:$(BINOBJSDIR)/%.o $(LIB)
	echo "* linking: $(@F) with $(LDFLAGS)"
	$(LD)   $(EXTRALIBSPATH) -o $@_x $< $(LOADLIBS) $(LDFLAGS)


# Static library (LIB) depends on library objects (.o) for each class (LIBOBJS).  
$(LIB):$(LIBOBJS)
	echo "* building library: $(@F)"
	$(AR) $(ARFLAGS) $@ $(LIBOBJS)

# Library object (.o) for each class (LIBOBJS) depends on corresponding source file
# (in srcdir with .o replaced by .SOURCEPAT) and will compile if not up-to-date  
$(LIBOBJS):$(LIBOBJSDIR)/%.o:$(SRCDIR)/%.$(SOURCEPAT) 
	echo "* compiling: $(<F)"
	$(CPP) $(CPPFLAGS) -o $@ $<

# Binary object for each prg (BINOBJS) depends on corresponding main file 
# (in prgdir with .o replaced by .SOURCEPAT) and will compile if no up-to-date 
$(BINOBJS):$(BINOBJSDIR)/%.o:$(PRGDIR)/%.$(EXEPAT)
	echo "* compiling: $(<F)"
	$(CPP) $(CPPFLAGS) -o $@ $<

$(LIBDEPS):$(DEPSDIR)/%.d:$(SRCDIR)/%.$(SOURCEPAT)
	echo "* creating dependencies: $(<F)"
	set -e; $(DEP) $(DEPFLAGS) $< | sed 's!\w.*\.o[ :]*!$(LIBOBJSDIR)/$*.o $@ : !' > $@;\
	[ -s $@ ] || rm -f $@

$(BINDEPS):$(DEPSDIR)/%.d:$(PRGDIR)/%.$(EXECEPAT)
	echo "* creating dependencies: $(<F)"
	set -e; $(DEP) $(DEPFLAGS) $< | sed 's!\w.*\.o[ :]*!$(BINOBJSDIR)/$*.o $@ : !' > $@;\
	[ -s $@ ] || rm -f $@

# Clean up by removing all binaries, binary objects, libaries, library objects 
# and dependencies for both
clean:
	echo "* removing all targets"
	rm -f $(BINS) $(BINOBJS) $(LIB) $(LIBOBJS) $(BINDEPS) $(LIBDEPS)
	echo "* clean done"

# Make correct directory structure and copy files into it.  Files ending in:
# - .HEADERPAT go to INCDIR
# - .SRCPAT go to
#   - PRGDIR if contain main()
#   - SRCDIR otherwise
setup:
	echo "* creating directory structure"
	mkdir -p $(SRCDIR) $(PRGDIR) $(BINDIR) $(LIBDIR) $(INCDIR) $(TMPDIR)/deps $(TMPDIR)/lib $(TMPDIR)/bin
	echo "* Moving program files to $(PRGDIR)"
	mv $(shell grep -H "main()" *.$(EXEPAT) | cut -d : -f 1) $(PRGDIR)/.
	echo "* Moving header files to $(INDIR)"
	mv *.$(HEADERPAT) $(INCDIR)/.
	echo "* Moving source files to $(SRCDIR)"
	mv *.$(SOURCEPAT) $(SRCDIR)/.

dust:
	echo "* cough, cough"

ifneq ($(VERBOSE),yes)
.SILENT:
endif

.PHONY: all clean dust lib bin setup

# include the dependency files if the target does not contain "clean", "setup"
# the "-" suppresses warnings if files do not exist
ifeq (,$(findstring clean,$(MAKECMDGOALS)))
ifeq (,$(findstring setup,$(MAKECMDGOALS)))
-include $(BINDEPS)
-include $(LIBDEPS)
endif
endif

