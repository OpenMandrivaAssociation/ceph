%define _disable_ld_no_undefined 1
%define _disable_rebuild_configure 1

%define maj0 0
%define major 1
%define maj2 2
%define libcephfs %mklibname cephfs %{major}
%define liberasure %mklibname erasure %{major}
%define libcls %mklibname cls %{major}
%define librados %mklibname rados %{maj2}
%define libradosstriper %mklibname radosstriper %{major}
%define librbd %mklibname rbd %{major}
%define devname %mklibname ceph -d

Summary:	User space components of the Ceph file system
Name:		ceph
Version:	10.2.2
Release:	1
License:	GPLv2
Group:		System/Base
Url:		http://ceph.com
Source0:	http://ceph.com/download/%{name}-%{version}.tar.gz
Source1:	ceph.rpmlintrc
Patch0:		ceph-9.2.1-py3.patch
Patch1:		0001-Disable-erasure_codelib-neon-build.patch
Patch2:		0002-Do-not-use-momit-leaf-frame-pointer-flag.patch
Patch3:		0003-fix-tcmalloc-handling-in-spec-file.patch
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

#export CC=gcc
#export CXX=g++

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
        CXXFLAGS="$CXXFLAGS -DBOOST_VARIANT_USE_RELAXED_GET_BY_DEFAULT=1"

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
install -m 0644 -D udev/60-ceph-partuuid-workaround.rules %{buildroot}%{_udevrulesdir}/60-ceph-partuuid-workaround.rules

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
%{_bindir}/rbd
%{_bindir}/rbdmap
%{_bindir}/ceph-debugpack
%{_bindir}/ceph-coverage
%{_bindir}/ceph-dencoder
%{_bindir}/ceph-rest-api
%{_bindir}/ceph-post-file
%{_initrddir}/ceph
/sbin/mount.ceph
%{_sbindir}/ceph-create-keys
%{_sbindir}/ceph-disk
%{_sbindir}/ceph-disk-udev
%dir %{_libdir}/ceph
%{_libdir}/ceph/ceph_common.sh
%{_libdir}/ceph/ceph-monstore-update-crush.sh
%{_libexecdir}/ceph/ceph-osd-prestart.sh
%config(noreplace) %{_sysconfdir}/logrotate.d/ceph
%config(noreplace) %{_sysconfdir}/bash_completion.d/rados
%config(noreplace) %{_sysconfdir}/bash_completion.d/ceph
%config(noreplace) %{_sysconfdir}/bash_completion.d/rbd
%dir %{_localstatedir}/lib/ceph/
%dir %{_localstatedir}/lib/ceph/tmp/
%dir %{_localstatedir}/log/ceph/
%{_datadir}/ceph/id_dsa_drop.ceph.com
%{_datadir}/ceph/id_dsa_drop.ceph.com.pub
%{_datadir}/ceph/known_hosts_drop.ceph.com

%files -n %{liberasure}
%{_libdir}/ceph/erasure-code
%exclude %{_libdir}/ceph/erasure-code/*.so

%files fuse
%{_bindir}/ceph-fuse
%{_bindir}/rbd-fuse
/sbin/mount.fuse.ceph

%files radosgw
#% {_initrddir}/ceph-radosgw
%{_bindir}/radosgw
%{_bindir}/radosgw-admin
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
%{_libdir}/ceph/erasure-code/*.so

%files -n python-ceph
%{python3_sitelib}/ceph_detect_init*
%{python3_sitelib}/*.py*
%{python3_sitelib}/__pycache__/*
