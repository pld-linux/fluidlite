#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Software SoundFont synth
Summary(pl.UTF-8):	Programowy syntezator oparty na SoundFontach
Name:		fluidlite
Version:	0
%define	snap	20170304
%define	gitref	7b5f2798d5c0f34e5436530412fe51e5183e8aa4
Release:	0.%{snap}.1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://github.com/divideconcept/FluidLite/archive/%{gitref}/FluidLite-%{snap}.tar.gz
# Source0-md5:	e6b663fd040885e0fc21e191b3053d2e
Patch0:		%{name}-pc.patch
URL:		https://github.com/divideconcept/FluidLite
BuildRequires:	cmake >= 3.1
BuildRequires:	libogg-devel >= 2:1.3.2
BuildRequires:	libvorbis-devel >= 1:1.3.5
BuildRequires:	pkgconfig
Requires:	libogg >= 2:1.3.2
Requires:	libvorbis >= 1:1.3.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FluidLite is a very light version of FluidSynth designed to be
hardware, platform and external dependency independant.

%description -l pl.UTF-8
FluidLite to bardzo lekka wersja FluidSyntha, zaprojektowana jako
niezależna od sprzętu, platformy i zależności zewnętrznych.

%package devel
Summary:	Header files for FluidLite library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki FluidLite
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libogg-devel >= 2:1.3.2
Requires:	libvorbis-devel >= 1:1.3.5

%description devel
Header files for FluidLite library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki FluidLite.

%package static
Summary:	Static FluidLite library
Summary(pl.UTF-8):	Statyczna biblioteka FluidLite
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static FluidLite library.

%description static -l pl.UTF-8
Statyczna biblioteka FluidLite.

%prep
%setup -q -n FluidLite-%{gitref}
%patch0 -p1

%{__rm} -r libogg-1.3.2 libvorbis-1.3.5

%build
install -d build
cd build
# change include dir to subdir (/usr/include/fluidsynth belongs to full fluidsynth)
%cmake .. \
	-DCMAKE_INSTALL_INCLUDEDIR=include/fluidlite \
	%{!?with_static_libs:-DFLUIDLITE_BUILD_STATIC=OFF}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_libdir}/libfluidlite.so

%files devel
%defattr(644,root,root,755)
%dir %{_includedir}/fluidlite
%{_includedir}/fluidlite/fluidlite.h
%{_includedir}/fluidlite/fluidsynth
%{_pkgconfigdir}/fluidlite.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libfluidlite.a
%endif
