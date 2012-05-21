Summary: Timezone data
Name: tzdata
Version: 2011h
%define tzdata_version %{version}
%define tzcode_version 2011g
Release: 1
License: Public Domain
Group: System/Base
URL: ftp://elsie.nci.nih.gov/pub/

# The tzdata-base-0.tar.bz2 is a simple building infrastructure and
# test suite.  It is occasionally updated from glibc sources, and as
# such is under LGPLv2+, but none of this ever gets to be part of
# final zoneinfo files.
Source0: tzdata-base-0.tar.bz2
# These are official upstream.
Source1: ftp://elsie.nci.nih.gov/pub/tzdata%{tzdata_version}.tar.gz
Source2: ftp://elsie.nci.nih.gov/pub/tzcode%{tzcode_version}.tar.gz
BuildArch: noarch

%description
This package contains data files with rules for various timezones around
the world.

%prep
%setup -q -n tzdata
mkdir tzdata%{tzdata_version}
tar xzf %{SOURCE1} -C tzdata%{tzdata_version}
mkdir tzcode%{tzcode_version}
tar xzf %{SOURCE2} -C tzcode%{tzcode_version}
sed -e 's|@objpfx@|'`pwd`'/obj/|' \
    -e 's|@datadir@|%{_datadir}|' \
  Makeconfig.in > Makeconfig


%build
make

%install
rm -fr $RPM_BUILD_ROOT
sed -i 's|@install_root@|%{buildroot}|' Makeconfig
make install

%check
echo ====================TESTING=========================
make check
echo ====================TESTING END=====================

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_datadir}/zoneinfo

