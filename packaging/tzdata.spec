Summary: Timezone data
Name: tzdata
Version: 2013h
Release: 1
License: Public Domain
Group: System/Base
URL: http://www.iana.org/time-zones

Source0: %{name}-%{version}.tar.gz
# These are official upstream.
Source1: ftp://ftp.iana.org/tz/releases/tzdata%{version}.tar.gz
Source2: ftp://ftp.iana.org/tz/releases/tzcode%{version}.tar.gz
Patch1:         tzdata-china.diff
Patch2:         iso3166-uk.diff
BuildArch: noarch
%global AREA    Etc
%global ZONE    UTC

%description
This package contains data files with rules for various timezones around
the world.

%prep
%setup -c -T -b 1 -b 2
%patch1 -p1
%patch2 -p1

sed -ri 's@/usr/local/etc/zoneinfo@%{_datadir}/zoneinfo@g' *

%build
unset ${!LC_*}
LANG=POSIX
LC_ALL=POSIX
AREA=%{AREA}
ZONE=%{ZONE}
export AREA LANG LC_ALL ZONE
make %{?_smp_mflags} TZDIR=%{_datadir}/zoneinfo CFLAGS="$RPM_OPT_FLAGS -DHAVE_GETTEXT=1 -DTM_GMTOFF=tm_gmtoff -DTM_ZONE=tm_zone" AWK=awk
make %{?_smp_mflags} TZDIR=zoneinfo AWK=awk zones
# Generate posixrules
./zic -y ./yearistype -d zoneinfo -p %{AREA}/%{ZONE}

%install
rm -fr %{buildroot}
mkdir -p %{buildroot}%{_datadir}/zoneinfo
cp -a zoneinfo %{buildroot}%{_datadir}/zoneinfo/posix
cp -al %{buildroot}%{_datadir}/zoneinfo/posix/. %{buildroot}%{_datadir}/zoneinfo
cp -a zoneinfo-leaps %{buildroot}%{_datadir}/zoneinfo/right
rm -f  %{buildroot}%{_datadir}/zoneinfo/posixrules
ln -sf /etc/localtime      %{buildroot}%{_datadir}/zoneinfo/posixrules
install -m 644 iso3166.tab %{buildroot}%{_datadir}/zoneinfo/iso3166.tab
install -m 644 zone.tab    %{buildroot}%{_datadir}/zoneinfo/zone.tab
#mkdir -p %{buildroot}/etc
#rm -f  %{buildroot}/etc/localtime
#cp -fp %{buildroot}%{_datadir}/zoneinfo/%{AREA}/%{ZONE} %{buildroot}/etc/localtime

%check

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_datadir}/zoneinfo