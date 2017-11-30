%define _disable_ld_no_undefined 1
%define _disable_rebuild_configure 1
%define _disable_lto 1

%define maj0 0
%define major 1
%define maj2 2
%define libcephfs %mklibname cephfs %{maj2}
%define libcls %mklibname cls %{major}
%define librados %mklibname rados %{maj2}
%define libradosstriper %mklibname radosstriper %{major}
%define librbd %mklibname rbd %{major}
%define librgw %mklibname rgw %{maj2}
%define devname %mklibname ceph -d

%bcond_without python2

Summary:	User space components of the Ceph file system
Name:		ceph
Version:	12.2.1
Release:	1
License:	GPLv2
Group:		System/Base
Url:		http://ceph.com
Source0:	http://download.ceph.com/tarballs/%{name}-%{version}.tar.gz
Source1:	ceph.rpmlintrc
BuildRequires:	boost-devel
BuildRequires:	fcgi-devel
BuildRequires:	git-core
BuildRequires:	cmake
BuildRequires:	keyutils-devel
BuildRequires:	libaio-devel
BuildRequires:	pkgconfig(atomic_ops)
BuildRequires:	pkgconfig(blkid)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(fuse3)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libedit)
BuildRequires:	pkgconfig(lttng-ust)
BuildRequires:	pkgconfig(nss)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(leveldb)
BuildRequires:	pkgconfig(libudev)
BuildRequires:	pkgconfig(systemd)
BuildRequires:	pkgconfig(babeltrace)
BuildRequires:	pkgconfig(python3)
BuildRequires:	python-setuptools
BuildRequires:	python-cython
BuildRequires:	python-virtualenv
BuildRequires:	python-nose
BuildRequires:	python-requests
BuildRequires:	python-sphinx
BuildRequires:	python-pip
%if %{with python2}
BuildRequires:	pkgconfig(python2)
BuildRequires:	python2-setuptools
BuildRequires:	python2-cython
BuildRequires:	python2-virtualenv
BuildRequires:	python2-nose
BuildRequires:	python2-requests
BuildRequires:	python2-sphinx
BuildRequires:	python2-pip
%endif
BuildRequires:	snappy-devel
BuildRequires:	yasm
Obsoletes: %mklibname erasure 1

%libpackage os_tp 1
%libpackage osd_tp 1
%libpackage rados_tp 2
%libpackage rbd_tp 1

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

%package -n python2-ceph
Summary:	Python 2.x libraries for the Ceph distributed filesystem
Group:		System/Libraries
License:	LGPLv2

%description -n python2-ceph
This package contains Python 2.x libraries for interacting with Cephs RADOS
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

%cmake \
	-DBUILD_SHARED_LIBS:BOOL=ON \
	-DWITH_CEPHFS:BOOL=ON \
	-DWITH_SYSTEMD:BOOL=ON \
	-DWITH_SYSTEM_BOOST:BOOL=ON \
	-DWITH_PYTHON3:BOOL=ON
%make

%install
%makeinstall_std -C build

mkdir -p %{buildroot}/lib
mv %{buildroot}%{_libexecdir}/systemd %{buildroot}/lib/

mv %{buildroot}%{_prefix}/etc %{buildroot}

chmod 0644 %{buildroot}%{_docdir}/ceph/sample.ceph.conf
install -m 0644 -D src/logrotate.conf %{buildroot}%{_sysconfdir}/logrotate.d/ceph

# udev rules
mkdir -p %{buildroot}%{_udevrulesdir}
install -m 0644 -D udev/*.rules %{buildroot}%{_udevrulesdir}/

# Probably not needed with systemd...
rm -rf %{buildroot}%{_sysconfdir}/init.d

# Tests that shouldn't be required post-install
# and that drag in a slew of dependencies...
rm -f %{buildroot}%{_bindir}/dmclock-*tests \
	%{buildroot}%{_bindir}/ceph_test_*

%files
%doc README COPYING
%{_sysconfdir}/bash_completion.d/ceph
%{_sysconfdir}/bash_completion.d/rados
%{_sysconfdir}/bash_completion.d/rbd
%{_udevrulesdir}/*.rules
%{_systemunitdir}/*.service
%{_systemunitdir}/*.target
%{_bindir}/ceph-objectstore-tool
%{_bindir}/cephfs-table-tool
%{_bindir}/rbd-replay
%{_bindir}/rbd-replay-many
%{_bindir}/ceph
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
%{_bindir}/ceph-bluestore-tool
%{_bindir}/ceph-client-debug
%{_bindir}/ceph-kvstore-tool
%{_bindir}/ceph-mgr
%{_libdir}/ceph/mgr
%{_bindir}/ceph-monstore-tool
%{_bindir}/ceph-osdomap-tool
%{_bindir}/ceph_bench_log
%{_bindir}/ceph_erasure_code
%{_bindir}/ceph_erasure_code_benchmark
%{_bindir}/ceph_kvstorebench
%{_bindir}/ceph_multi_stress_watch
%{_bindir}/ceph_objectstore_bench
%{_bindir}/ceph_omapbench
%{_bindir}/ceph_perf_local
%{_bindir}/ceph_perf_msgr_client
%{_bindir}/ceph_perf_msgr_server
%{_bindir}/ceph_perf_objectstore
%{_bindir}/ceph_psim
%{_bindir}/ceph_radosacl
%{_bindir}/ceph_rgw_jsonparser
%{_bindir}/ceph_rgw_multiparser
%{_bindir}/ceph_scratchtool
%{_bindir}/ceph_scratchtoolpp
%{_bindir}/ceph_smalliobench
%{_bindir}/ceph_smalliobenchdumb
%{_bindir}/ceph_smalliobenchfs
%{_bindir}/ceph_smalliobenchrbd
%{_bindir}/ceph_tpbench
%{_bindir}/ceph_xattr_bench
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
%{_bindir}/rbd-replay-prep
%{_bindir}/rbdmap
%{_bindir}/ceph-debugpack
%{_bindir}/ceph-coverage
%{_bindir}/ceph-dencoder
%{_bindir}/ceph-rest-api
%{_bindir}/ceph-post-file
%{_sbindir}/mount.ceph
%{_sbindir}/ceph-create-keys
%{_sbindir}/ceph-disk
%{_sbindir}/ceph-disk-udev
%{_libexecdir}/ceph
%dir %{_libdir}/ceph
%{_libdir}/ceph/ceph-monstore-update-crush.sh
%config(noreplace) %{_sysconfdir}/logrotate.d/ceph
%{_datadir}/ceph/id_rsa_drop.ceph.com
%{_datadir}/ceph/id_rsa_drop.ceph.com.pub
%{_datadir}/ceph/known_hosts_drop.ceph.com
%dir %{_libdir}/ceph/compressor
%{_libdir}/ceph/compressor/*.so*
%{_libdir}/ceph/crypto
%{_libdir}/ceph/erasure-code
%{_libdir}/ceph/libceph-common.so*
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

%files fuse
%{_bindir}/ceph-fuse
%{_bindir}/rbd-fuse
%_mandir/man8/ceph-fuse.8*
%_mandir/man8/rbd-fuse.8*
%{_sbindir}/mount.fuse.ceph

%files radosgw
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
%{_libdir}/libcephfs.so.%{maj2}*

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
%{_libdir}/libos_tp.so
%{_libdir}/libosd_tp.so
%{_libdir}/librados_tp.so
%{_libdir}/librbd_tp.so

%files -n python-ceph
%{python3_sitelib}/*.py*
%{python3_sitearch}/cephfs*
%{python3_sitearch}/rados*
%{python3_sitearch}/rbd*
%{python3_sitearch}/rgw*

%if %{with python2}
%files -n python2-ceph
%{python2_sitelib}/*.py*
%{python2_sitelib}/ceph_detect_init*
%{python2_sitelib}/ceph_disk*
%{python2_sitearch}/cephfs*
%{python2_sitearch}/rados*
%{python2_sitearch}/rbd*
%{python2_sitearch}/rgw*
%endif
