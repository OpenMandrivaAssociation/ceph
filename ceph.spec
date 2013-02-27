%define _disable_ld_no_undefined 1

%define	major	1
%define	maj2	2
%define	libcephfs	%mklibname cephfs %{major}
%define	libcls		%mklibname cls %{major}
%define	librados	%mklibname rados %{maj2}
%define	librbd		%mklibname rbd %{major}
%define	devname		%mklibname ceph -d

Summary:	User space components of the Ceph file system
Name:		ceph
Version:	0.57
Release:	1
License:	GPLv2
Group:		System/Base
Url:		http://ceph.com
Source0:	http://ceph.com/download/%{name}-%{version}.tar.bz2

BuildRequires:	boost-devel
BuildRequires:	keyutils-devel
BuildRequires:	libaio-devel
BuildRequires:	libatomic_ops-devel
BuildRequires:	libfcgi-devel
BuildRequires:	pkgconfig(fuse)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libedit)
BuildRequires:	pkgconfig(nss)
BuildRequires:	pkgconfig(uuid)
Requires(preun,post):	chkconfig

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
Requires:	mod_fcgid

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
Requires:	%{libcephfs} = %{version}-%{release}
Requires:	%{libcls} = %{version}-%{release}
Requires:	%{librados} = %{version}-%{release}
Requires:	%{librbd} = %{version}-%{release}

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

%build
%configure2_5x \
	--disable-static \
	--with-radosgw \
	--without-hadoop \
	--without-tcmalloc

%make

%install
%makeinstall_std

install -D src/init-ceph %{buildroot}%{_initrddir}/ceph
install -D src/init-radosgw %{buildroot}%{_initrddir}/ceph-radosgw
mkdir -p %{buildroot}%{_sbindir}
ln -sf ../../etc/init.d/ceph %{buildroot}%{_sbindir}/rcceph
ln -sf ../../etc/init.d/ceph-radosgw %{buildroot}%{_sbindir}/rcceph-radosgw
install -m 0644 -D src/logrotate.conf %{buildroot}%{_sysconfdir}/logrotate.d/ceph

mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/tmp/
mkdir -p %{buildroot}%{_localstatedir}/log/ceph/
mkdir -p %{buildroot}%{_localstatedir}/run/ceph/
mkdir -p %{buildroot}%{_sysconfdir}/ceph/

%post
/sbin/chkconfig --add ceph

%preun
if [ $1 = 0 ] ; then
    /sbin/service ceph stop >/dev/null 2>&1
    /sbin/chkconfig --del ceph
fi

%postun
if [ "$1" -ge "1" ] ; then
    /sbin/service ceph condrestart >/dev/null 2>&1 || :
fi

%files
%config %{_sysconfdir}/bash_completion.d/ceph
%config %{_sysconfdir}/bash_completion.d/rados
%config %{_sysconfdir}/bash_completion.d/radosgw-admin
%config %{_sysconfdir}/bash_completion.d/rbd
%dir %{_sysconfdir}/ceph/
%config(noreplace) %{_sysconfdir}/logrotate.d/ceph
%{_initrddir}/ceph
%{_bindir}/ceph
%{_bindir}/cephfs
%{_bindir}/ceph-conf
%{_bindir}/ceph-clsinfo
%{_bindir}/crushtool
%{_bindir}/monmaptool
%{_bindir}/osdmaptool
%{_bindir}/ceph-authtool
%{_bindir}/ceph-syn
%{_bindir}/ceph-run
%{_bindir}/ceph-mon
%{_bindir}/ceph-mds
%{_bindir}/ceph-osd
%{_bindir}/ceph-rbdnamer
%{_bindir}/ceph-dencoder
%{_bindir}/librados-config
%{_bindir}/rados
%{_bindir}/rbd
%{_bindir}/ceph-debugpack
%{_bindir}/ceph-filestore-dump
%{_bindir}/ceph-coverage
%{_sbindir}/ceph-create-keys
%{_sbindir}/ceph-disk-activate
%{_sbindir}/ceph-disk-prepare
%{_sbindir}/mkcephfs
%{_sbindir}/mount.ceph
%{_sbindir}/rcceph
%{_libdir}/ceph
%{_mandir}/man8/ceph*.8*
%{_mandir}/man8/mkcephfs.8*
%{_mandir}/man8/crushtool.8*
%{_mandir}/man8/osdmaptool.8*
%{_mandir}/man8/monmaptool.8*
%{_mandir}/man8/mount.ceph.8*
%{_mandir}/man8/rados.8*
%{_mandir}/man8/rbd.8*
%exclude %{_mandir}/man8/ceph-fuse.8*
%{_mandir}/man8/librados-config.8*
%dir %{_localstatedir}/lib/ceph/
%dir %{_localstatedir}/lib/ceph/tmp/
%dir %{_localstatedir}/log/ceph/
%ghost %dir %{_localstatedir}/run/ceph/

%files fuse
%{_bindir}/ceph-fuse
%{_bindir}/rbd-fuse
%{_sbindir}/mount.fuse.ceph
%{_mandir}/man8/ceph-fuse.8*
%{_mandir}/man8/rbd-fuse.8*

%files radosgw
%{_initrddir}/ceph-radosgw
%{_bindir}/radosgw
%{_bindir}/radosgw-admin
%{_sbindir}/rcceph-radosgw
%{_mandir}/man8/radosgw.8*
%{_mandir}/man8/radosgw-admin.8*

%files -n %{libcls}
%dir %{_libdir}/rados-classes
%{_libdir}/rados-classes/libcls_rbd.so.%{major}*
%{_libdir}/rados-classes/libcls_rgw.so.%{major}*
%{_libdir}/rados-classes/libcls_kvs.so.%{major}*
%{_libdir}/rados-classes/libcls_lock.so.%{major}*
%{_libdir}/rados-classes/libcls_refcount.so.%{major}*

%files -n %{librados}
%{_libdir}/librados.so.%{maj2}*

%files -n %{librbd}
%{_libdir}/librbd.so.%{major}*

%files -n %{libcephfs}
%{_libdir}/libcephfs.so.%{major}*

%files -n %{devname}
%dir %{_docdir}/ceph
%{_docdir}/ceph/sample.ceph.conf
%{_docdir}/ceph/sample.fetch_config
%dir %{_includedir}/cephfs
%{_includedir}/cephfs/*
%dir %{_includedir}/rados
%{_includedir}/rados/*
%dir %{_includedir}/rbd
%{_includedir}/rbd/*
%{_libdir}/libcephfs.so
%{_libdir}/librbd.so
%{_libdir}/librados.so
%{_libdir}/rados-classes/libcls_rbd.so
%{_libdir}/rados-classes/libcls_rgw.so
%{_libdir}/rados-classes/libcls_kvs.so
%{_libdir}/rados-classes/libcls_lock.so
%{_libdir}/rados-classes/libcls_refcount.so

%files -n python-ceph
%{python_sitelib}/rados.py*
%{python_sitelib}/rbd.py*

