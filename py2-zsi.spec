### RPM external py2-zsi 2.0
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages 
Source: http://switch.dl.sourceforge.net/sourceforge/pywebsvcs/ZSI-%{v}.tar.gz
Requires: python

%prep 
%setup -n ZSI-%v
%build
./setup.py build
%install
./setup.py install --prefix=%{i}
perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/wsdl2dispatch %{i}/bin/wsdl2py
##perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/wsdl2dispatch.py %{i}/bin/wsdl2py.py
