### RPM external git 1.8.3.1
## INITENV +PATH PATH %{i}/bin
## INITENV +PATH PATH %{i}/libexec/git-core
## INITENV SET GIT_TEMPLATE_DIR %{i}/share/git-core/templates
## INITENV SET GIT_SSL_CAINFO %{i}/share/ssl/certs/ca-bundle.crt
## INITENV SET GIT_EXEC_PATH %{i}/libexec/git-core

%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%define isDarwin %(case %{cmsos} in (osx*) echo 1 ;; (*) echo 0 ;; esac)

Source0: https://github.com/git/git/archive/v%{realversion}.tar.gz
Patch1: git-1.8.3.1-no-symlink
Patch2: git-1.8.3.1-runtime

%define curl_tag curl-7_31_0
Source1: https://raw.github.com/bagder/curl/%{curl_tag}/lib/mk-ca-bundle.pl


%if "%mic" == "true"
Requires: curl-host expat-host openssl-bootstrap zlib-bootstrap pcre-host
%else
Requires: curl expat openssl zlib pcre
%endif

# Fake provides for git add --interactive
# The following are not avaialble on SLC and Darwin platforms by default
Provides: perl(DBI)
Provides: perl(Error)
Provides: perl(SVN::Client)
Provides: perl(SVN::Core)
Provides: perl(SVN::Delta)
Provides: perl(SVN::Ra)
Provides: perl(YAML::Any)
Provides: perl(CGI)
Provides: perl(CGI::Carp)
Provides: perl(CGI::Util)
Provides: perl(Time::HiRes)

%define drop_files %{i}/share/man

%prep
%setup -b 0 -n %{n}-%{realversion}
%patch1 -p1
%patch2 -p1

%build
%if "%mic" == "true"
CURL_ROOT=$CURL_HOST_ROOT
EXPAT_ROOT=$EXPAT_HOST_ROOT
PCRE_ROOT=$PCRE_HOST_ROOT
OPENSSL_ROOT=$OPENSSL_BOOTSTRAP_ROOT
ZLIB_ROOT=$ZLIB_BOOTSTRAP_ROOT
%endif
make prefix=%{i} \
%if %isDarwin
     NO_DARWIN_PORTS=1 \
     NO_FINK=1 \
%endif
     CURLDIR="${CURL_ROOT}" \
     OPENSSLDIR="${OPENSSL_ROOT}" \
     EXPATDIR="${EXPAT_ROOT}" \
     ZLIB_PATH="${ZLIB_ROOT}" \
     USE_LIBPCRE=1 \
     NO_GETTEXT=1 \
     NO_R_TO_GCC_LINKER=1 \
     LIBPCREDIR="${PCRE_ROOT}" \
     NO_PYTHON=1 \
     RUNTIME_PREFIX=1 \
     V=1 \
     %{makeprocesses} \
     all

# Generate ca-bundle.crt (Certification Authority certificates)
mkdir ./ca-bundle
pushd ./ca-bundle
cp %{SOURCE1} ./mk-ca-bundle.pl
chmod +x ./mk-ca-bundle.pl
./mk-ca-bundle.pl
popd

%install
%if "%mic" == "true"
CURL_ROOT=$CURL_HOST_ROOT
EXPAT_ROOT=$EXPAT_HOST_ROOT
PCRE_ROOT=$PCRE_HOST_ROOT
OPENSSL_ROOT=$OPENSSL_BOOTSTRAP_ROOT
ZLIB_ROOT=$ZLIB_BOOTSTRAP_ROOT
%endif
make prefix=%{i} \
%if %isDarwin
     NO_DARWIN_PORTS=1 \
     NO_FINK=1 \
%endif
     CURLDIR="${CURL_ROOT}" \
     OPENSSLDIR="${OPENSSL_ROOT}" \
     EXPATDIR="${EXPAT_ROOT}" \
     ZLIB_PATH="${ZLIB_ROOT}" \
     USE_LIBPCRE=1 \
     NO_GETTEXT=1 \
     NO_R_TO_GCC_LINKER=1 \
     LIBPCREDIR="${PCRE_ROOT}" \
     NO_PYTHON=1 \
     RUNTIME_PREFIX=1 \
     V=1 \
     %{makeprocesses} \
     install

# Install ca-bundle.crt (Certification Authority certificates)
mkdir -p %{i}/share/ssl/certs
cp ./ca-bundle/ca-bundle.crt %{i}/share/ssl/certs/ca-bundle.crt

%post
%{relocateConfig}bin/git-cvsserver
%{relocateConfig}libexec/git-core/git-sh-i18n
%{relocateConfig}libexec/git-core/git-citool
%{relocateConfig}libexec/git-core/git-gui
%{relocateConfig}libexec/git-core/git-add--interactive
%{relocateConfig}libexec/git-core/git-archimport
%{relocateConfig}libexec/git-core/git-cvsexportcommit
%{relocateConfig}libexec/git-core/git-cvsimport
%{relocateConfig}libexec/git-core/git-cvsserver
%{relocateConfig}libexec/git-core/git-difftool
%{relocateConfig}libexec/git-core/git-instaweb
%{relocateConfig}libexec/git-core/git-relink
%{relocateConfig}libexec/git-core/git-send-email
%{relocateConfig}libexec/git-core/git-svn
%{relocateCmsFiles} `find $RPM_INSTALL_PREFIX/%{pkgrel}/share -name "*" -type f`
%{relocateCmsFiles} `find $RPM_INSTALL_PREFIX/%{pkgrel}/lib64/perl5 -name "*" -type f`
if [ -d $RPM_INSTALL_PREFIX/%{pkgrel}/lib/perl5 ]; then 
  %{relocateCmsFiles} `find $RPM_INSTALL_PREFIX/%{pkgrel}/lib/perl5 -name "*" -type f`
fi
