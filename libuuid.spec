### RPM external libuuid 2.22.2
Source: http://www.kernel.org/pub/linux/utils/util-linux/v2.22/util-linux-%{realversion}.tar.gz
Patch0: libuuid-2.22.2-disable-get_uuid_via_daemon
%define keep_archives true

%prep
%setup -n util-linux-%{realversion}
%patch0 -p1

%build
./configure $([ $(uname) == Darwin ] && echo --disable-shared) \
            --prefix="%{i}" \
            --build="%{_build}" \
            --host=%{_host} \
            --disable-silent-rules \
            --disable-tls \
            --disable-rpath \
            --disable-libblkid \
            --disable-libmount \
            --disable-mount \
            --disable-losetup \
            --disable-fsck \
            --disable-partx \
            --disable-mountpoint \
            --disable-fallocate \
            --disable-unshare \
            --disable-eject \
            --disable-agetty \
            --disable-cramfs \
            --disable-wdctl \
            --disable-switch_root \
            --disable-pivot_root \
            --disable-kill \
            --disable-utmpdump \
            --disable-rename \
            --disable-login \
            --disable-sulogin \
            --disable-su \
            --disable-schedutils \
            --disable-wall \
            --disable-makeinstall-setuid \
            --without-ncurses \
            --enable-libuuid

make %{makeprocesses} uuidd

%install
# There is no make install action for the libuuid libraries only
mkdir -p %{i}/lib
cp -p %{_builddir}/util-linux-%{realversion}/.libs/libuuid.[as]* %{i}/lib
mkdir -p %{i}/include
make install-uuidincHEADERS

%define drop_files %{i}/man
