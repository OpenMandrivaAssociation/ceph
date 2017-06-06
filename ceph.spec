%define _disable_ld_no_undefined 1
%define _disable_rebuild_configure 1
%define _disable_lto 1

%define maj0 0
%define major 1
%define maj2 2
%define libcephfs %mklibname cephfs %{major}
%define liberasure %mklibname erasure %{major}
%define libcls %mklibname cls %{major}
%define librados %mklibname rados %{maj2}
%define libradosstriper %mklibname radosstriper %{major}
%define librbd %mklibname rbd %{major}
%define librgw %mklibname rgw %{maj2}
%define devname %mklibname ceph -d

Summary:	User space components of the Ceph file system
Name:		ceph
Version:	10.2.7
Release:	1
License:	GPLv2
Group:		System/Base
Url:		http://ceph.com
Source0:	http://download.ceph.com/tarballs/%{name}-%{version}.tar.gz
Source1:	ceph.rpmlintrc
Patch0:		ceph-9.2.1-py3.patch
Patch1:		http://pkgs.fedoraproject.org/cgit/rpms/ceph.git/plain/0001-Disable-erasure_codelib-neon-build.patch
Patch2:		http://pkgs.fedoraproject.org/cgit/rpms/ceph.git/plain/0003-librbd-Journal-include-WorkQueue-since-we-use-it.patch
BuildRequires:	boost-devel
BuildRequires:	fcgi-devel
BuildRequires:	git
BuildRequires:	keyutils-devel
BuildRequires:	libaio-devel
BuildRequires:	pkgconfig(atomic_ops)
BuildRequires:	pkgconfig(blkid)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(fuse)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libedit)
BuildRequires:	pkgconfig(nss)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(leveldb)
BuildRequires:	pkgconfig(libudev)
BuildRequires:	pkgconfig(systemd)
BuildRequires:	python-setuptools
BuildRequires:	python-cython
BuildRequires:	python-virtualenv
BuildRequires:	python-nose
BuildRequires:	python-requests
BuildRequires:	python-sphinx
BuildRequires:	python-pip
BuildRequires:	snappy-devel
BuildRequires:	yasm

%description
Ceph is a distributed network file system designed to provide excellent
performance, reliability, and scalability.

%package fuse
Summary:	Ceph fuse-based client
Group:		System/Base
Requires:	%{name} = %{version}-%{release}

%description fuse
FUSE based client for Ceph distributed network file system

%package radosgw
Summary:	Rados REST gateway
Group:		System/Base
Requires:	apache-mod_fcgid

%description radosgw
radosgw is an S3 HTTP REST gateway for the RADOS object store. It is
implemented as a FastCGI module using libfcgi, and can be used in
conjunction with any FastCGI capable web server.

%package -n %{libcephfs}
Summary:	Ceph distributed file system client library
Group:		System/Libraries
License:	LGPLv2

%description -n %{libcephfs}
Ceph is a distributed network file system designed to provide excellent
performance, reliability, and scalability. This is a shared library
allowing applications to access a Ceph distributed file system via a
POSIX-like interface.

%package -n %{liberasure}
Summary:	Ceph distributed file system client library
Group:		System/Libraries
License:	LGPLv2

%description -n %{liberasure}
Ceph is a distributed network file system designed to provide excellent
performance, reliability, and scalability. This is a shared library
allowing applications to access a Ceph distributed file system via a
POSIX-like interface.

%package -n %{libcls}
Summary:	Ceph distributed file system client library
Group:		System/Libraries
License:	LGPLv2

%description -n %{libcls}
Ceph is a distributed network file system designed to provide excellent
performance, reliability, and scalability. This is a shared library
allowing applications to access a Ceph distributed file system via a
POSIX-like interface.

%package -n %{librados}
Summary:	RADOS distributed object store client library
Group:		System/Libraries
License:	LGPLv2

%description -n %{librados}
RADOS is a reliable, autonomic distributed object storage cluster
developed as part of the Ceph distributed storage system. This is a
shared library allowing applications to access the distributed object
store using a simple file-like interface.

%package -n %{libradosstriper}
Summary:        RADOS distributed object store client library
Group:          System/Libraries
License:        LGPLv2

%description -n %{libradosstriper}
RADOS is a reliable, autonomic distributed object storage cluster
developed as part of the Ceph distributed storage system. This is a
shared library allowing applications to access the distributed object
store using a simple file-like interface.

%package -n %{librbd}
Summary:	RADOS block device client library
Group:		System/Libraries
License:	LGPLv2

%description -n %{librbd}
RBD is a block device striped across multiple distributed objects in
RADOS, a reliable, autonomic distributed object storage cluster
developed as part of the Ceph distributed storage system. This is a
shared library allowing applications to manage these block devices.

%package -n %{librgw}
Summary:        RADOS gateway client library
Group:          System/Libraries
License:        LGPLv2

%description -n %{librgw}
This package provides a library implementation of the RADOS gateway
(distributed object store with S3 and Swift personalities).

%package -n %{devname}
Summary:	Ceph headers
Group:		Development/C
License:	LGPLv2
Provides:	%{name}-devel
Requires:	%{libcephfs} = %{version}-%{release}
Requires:	%{libcls} = %{version}-%{release}
Requires:	%{librados} = %{version}-%{release}
Requires:	%{librbd} = %{version}-%{release}
Requires:	%{libradosstriper} = %{version}-%{release}
Requires:	%{librgw} = %{version}-%{release}

%description -n %{devname}
This package contains libraries and headers needed to develop programs
that use Ceph.

%package -n python-ceph
Summary:	Python libraries for the Ceph distributed filesystem
Group:		System/Libraries
License:	LGPLv2

%description -n python-ceph
This package contains Python libraries for interacting with Cephs RADOS
object storage.

%prep
%setup -q
%apply_patches

%build
# (tpg) try to reduce memory when building on arm
%ifarch %{armx}
%global optflags %optflags --param ggc-min-expand=20 --param ggc-min-heapsize=32768
%endif

# Decrease debuginfo verbosity to reduce memory consumption even more
%global optflags `echo %optflags | sed -e 's/-gdwarf-4 /-g1 /'`

export CC=gcc
export CXX=g++

sed -i 's!$(exec_prefix)!!g' src/Makefile.*
%configure \
	--disable-static \
	--with-systemdsystemunitdir=%{_systemunitdir} \
	--with-nss \
	--without-cryptopp \
	--with-radosgw \
	--without-hadoop \
	--without-tcmalloc \
	--without-libxfs \
	--enable-client \
	--enable-server \
	--enable-gitversion \
        CXXFLAGS="$CXXFLAGS -DBOOST_VARIANT_USE_RELAXED_GET_BY_DEFAULT=1" \
	LIBS=-lldap
%make

%install
%makeinstall_std
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'
find %{buildroot} -type f -name "*.a" -exec rm -f {} ';'
install -D src/init-ceph %{buildroot}%{_initrddir}/ceph
chmod 0644 %{buildroot}%{_docdir}/ceph/sample.ceph.conf
install -m 0644 -D src/logrotate.conf %{buildroot}%{_sysconfdir}/logrotate.d/ceph
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/tmp/
mkdir -p %{buildroot}%{_localstatedir}/log/ceph/
mkdir -p %{buildroot}%{_localstatedir}/log/ceph/stat
mkdir -p %{buildroot}%{_sysconfdir}/ceph
mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d

# udev rules
install -m 0644 -D udev/50-rbd.rules %{buildroot}%{_udevrulesdir}/50-rbd.rules
install -m 0644 -D udev/60-ceph-by-parttypeuuid.rules %{buildroot}%{_udevrulesdir}/60-ceph-by-parttypeuuid.rules

%files
%doc README COPYING
%dir %{_sysconfdir}/ceph
%{_udevrulesdir}/*.rules
%{_systemunitdir}/*.service
%{_systemunitdir}/*.target
%{_bindir}/ceph-objectstore-tool
%{_bindir}/cephfs-table-tool
%{_bindir}/rbd-replay
%{_bindir}/rbd-replay-many
%{_bindir}/ceph
%{_bindir}/cephfs
%{_bindir}/cephfs-data-scan
%{_bindir}/cephfs-journal-tool
%{_bindir}/ceph-conf
%{_bindir}/ceph-clsinfo
%{_bindir}/ceph-bluefs-tool
%{_bindir}/ceph-detect-init
%{_bindir}/crushtool
%{_bindir}/monmaptool
%{_bindir}/osdmaptool
%{_bindir}/ceph-authtool
%{_bindir}/ceph-syn
%{_bindir}/ceph-run
%{_bindir}/ceph-mon
%{_bindir}/ceph-mds
%{_bindir}/ceph-osd
%{_bindir}/ceph-brag
%{_bindir}/ceph-crush-location
%{_bindir}/ceph-rbdnamer
%{_bindir}/librados-config
%{_bindir}/rados
%{_bindir}/radosgw-object-expirer
%{_bindir}/radosgw-token
%{_bindir}/rbd
%{_bindir}/rbd-mirror
%{_bindir}/rbd-nbd
%{_bindir}/rbdmap
%{_bindir}/ceph-debugpack
%{_bindir}/ceph-coverage
%{_bindir}/ceph-dencoder
%{_bindir}/ceph-rest-api
%{_bindir}/ceph-post-file
%{_initrddir}/ceph
%{_sbindir}/mount.ceph
%{_sbindir}/ceph-create-keys
%{_sbindir}/ceph-disk
%{_sbindir}/ceph-disk-udev
%dir %{_libdir}/ceph
%{_libexecdir}/ceph/ceph_common.sh
%{_libdir}/ceph/ceph-monstore-update-crush.sh
%{_libexecdir}/ceph/ceph-osd-prestart.sh
%config(noreplace) %{_sysconfdir}/logrotate.d/ceph
%config(noreplace) %{_sysconfdir}/bash_completion.d/rados
%config(noreplace) %{_sysconfdir}/bash_completion.d/ceph
%config(noreplace) %{_sysconfdir}/bash_completion.d/rbd
%dir %{_localstatedir}/lib/ceph/
%dir %{_localstatedir}/lib/ceph/tmp/
%dir %{_localstatedir}/log/ceph/
%{_datadir}/ceph/id_rsa_drop.ceph.com
%{_datadir}/ceph/id_rsa_drop.ceph.com.pub
%{_datadir}/ceph/known_hosts_drop.ceph.com
%{_libdir}/ceph/compressor
%exclude %{_libdir}/ceph/compressor/*.so
%_mandir/man8/ceph-authtool.8*
%_mandir/man8/ceph-clsinfo.8*
%_mandir/man8/ceph-conf.8*
%_mandir/man8/ceph-create-keys.8*
%_mandir/man8/ceph-debugpack.8*
%_mandir/man8/ceph-dencoder.8*
%_mandir/man8/ceph-deploy.8*
%_mandir/man8/ceph-detect-init.8*
%_mandir/man8/ceph-disk.8*
%_mandir/man8/ceph-mds.8*
%_mandir/man8/ceph-mon.8*
%_mandir/man8/ceph-osd.8*
%_mandir/man8/ceph-post-file.8*
%_mandir/man8/ceph-rbdnamer.8*
%_mandir/man8/ceph-rest-api.8*
%_mandir/man8/ceph-run.8*
%_mandir/man8/ceph-syn.8*
%_mandir/man8/ceph.8*
%_mandir/man8/cephfs.8*
%_mandir/man8/crushtool.8*
%_mandir/man8/librados-config.8*
%_mandir/man8/monmaptool.8*
%_mandir/man8/mount.ceph.8*
%_mandir/man8/osdmaptool.8*
%_mandir/man8/rados.8*
%_mandir/man8/rbd-mirror.8*
%_mandir/man8/rbd-nbd.8*
%_mandir/man8/rbd-replay-many.8*
%_mandir/man8/rbd-replay-prep.8*
%_mandir/man8/rbd-replay.8*
%_mandir/man8/rbd.8*
%_mandir/man8/rbdmap.8*

%files -n %{liberasure}
%{_libdir}/ceph/erasure-code
%exclude %{_libdir}/ceph/erasure-code/*.so

%files fuse
%{_bindir}/ceph-fuse
%{_bindir}/rbd-fuse
%_mandir/man8/ceph-fuse.8*
%_mandir/man8/rbd-fuse.8*
%{_sbindir}/mount.fuse.ceph

%files radosgw
#% {_initrddir}/ceph-radosgw
%{_bindir}/radosgw
%{_bindir}/radosgw-admin
%_mandir/man8/radosgw-admin.8*
%_mandir/man8/radosgw.8*
#% {_sbindir}/rcceph-radosgw
%{_sysconfdir}/bash_completion.d/radosgw-admin

%files -n %{libcls}
%{_libdir}/rados-classes

%files -n %{librados}
%{_libdir}/librados.so.%{maj2}*

%files -n %{libradosstriper}
%{_libdir}/libradosstriper.so.%{major}*

%files -n %{librbd}
%{_libdir}/librbd.so.%{major}*

%files -n %{libcephfs}
%{_libdir}/libcephfs.so.%{major}*

%files -n %{librgw}
%{_libdir}/librgw.so.%{maj2}*

%files -n %{devname}
%dir %{_docdir}/ceph
#%{_docdir}/ceph/sample.ceph.conf
#%{_docdir}/ceph/sample.fetch_config
%dir %{_includedir}/cephfs
%{_includedir}/cephfs/*
%dir %{_includedir}/rados
%{_includedir}/rados/*
%dir %{_includedir}/radosstriper
%{_includedir}/radosstriper/*
%dir %{_includedir}/rbd
%{_includedir}/rbd/*
%{_libdir}/libcephfs.so
%{_libdir}/librbd.so
%{_libdir}/librados.so
%{_libdir}/libradosstriper.so
%{_libdir}/librgw.so
%{_libdir}/ceph/erasure-code/*.so
%{_libdir}/ceph/compressor/*.so

%files -n python-ceph
%{python3_sitelib}/ceph_detect_init*
%{python3_sitelib}/*.py*
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/ceph_disk*
%{python3_sitearch}/cephfs*
%{python3_sitearch}/rados*
%{python3_sitearch}/rbd*
