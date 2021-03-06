### RPM external cherrypy38 3.8.0
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source: https://pypi.python.org/packages/source/C/CherryPy/CherryPy-%realversion.tar.gz 
Requires: python
#Patch0: cherrypy-multipart-length

%prep
%setup -n CherryPy-%realversion
##%patch0 -p0
perl -p -i -e 's/import profile/import cProfile as profile/' cherrypy/lib/profiler.py

%build
python setup.py build

%install
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
for f in %i/bin/cherryd; do perl -p -i -e 's{.*}{#!/usr/bin/env python} if $. == 1 && m{#!.*/bin/python}' $f; done
