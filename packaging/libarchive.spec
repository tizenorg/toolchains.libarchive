
Name:       libarchive
Summary:    A library for handling streaming archive formats
Version:    2.8.3
Release:    1
Group:      System/Libraries
License:    BSD
URL:        http://code.google.com/p/libarchive/
Source0:    http://libarchive.googlecode.com/files/libarchive-%{version}.tar.gz
Source1001: packaging/libarchive.manifest 
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(ext2fs)
BuildRequires:  bison
BuildRequires:  zlib-devel
BuildRequires:  bzip2-devel
BuildRequires:  libacl-devel
BuildRequires:  libattr-devel
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool

%description
Libarchive is a programming library that can create and read several different 
streaming archive formats, including most popular tar variants, several cpio 
formats, and both BSD and GNU ar variants. It can also write shar archives and 
read ISO9660 CDROM images and ZIP archives.



%package devel
Summary:    Development files for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.



%prep
%setup -q -n %{name}-%{version}


%build
cp %{SOURCE1001} .
libtoolize --force  || :
autoreconf  || :

%configure --disable-static \
    --disable-bsdtar \
    --disable-bsdcpio

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

iconv -f latin1 -t utf-8 < NEWS > NEWS.utf8; cp NEWS.utf8 NEWS
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name cpio.5 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name mtree.5 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name tar.5 -exec rm -f {} ';'

# Tizen SDK license
mkdir -p %{buildroot}/usr/share/license
cp COPYING %{buildroot}/usr/share/license/%{name}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig



%files
%manifest libarchive.manifest
%defattr(-,root,root,-)
%doc COPYING README NEWS
%{_libdir}/*.so.*
/usr/share/license/%{name}


%files devel
%manifest libarchive.manifest
%defattr(-,root,root,-)
%doc
%{_includedir}/*
%{_mandir}/*/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

