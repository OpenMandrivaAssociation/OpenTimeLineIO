%define libname %mklibname opentimelineio
%define devname %mklibname -d opentimelineio

Name:		OpenTimeLineIO
Version:	0.17.0
Release:	1
Source0:	https://github.com/AcademySoftwareFoundation/OpenTimelineIO/archive/refs/tags/v%{version}/%{name}-%{version}.tar.gz
Summary:	Editorial timeline information API
URL:		https://github.com/AcademySoftwareFoundation/OpenTimelineIO
License:	Apache-2.0 and MIT
Group:		System/Libraries
BuildRequires:	cmake
BuildRequires:	cmake(pybind11)
BuildRequires:	cmake(RapidJSON)
BuildRequires:	pkgconfig(python3)
BuildRequires:	python%{pyver}dist(pybind11)
BuildOption:	-DOTIO_CXX_INSTALL:BOOL=ON
BuildOption:	-DOTIO_PYTHON_INSTALL:BOOL=ON
BuildOption:	-DOTIO_PYTHON_INSTALL_DIR=%{python3_sitearch}
BuildOption:	-DOTIO_FIND_IMATH:BOOL=ON
BuildOption:	-DOTIO_SHARED_LIBS:BOOL=ON
BuildOption:	-DBUILD_SHARED_LIBS:BOOL=ON
BuildOption:	-DOTIO_DEPENDENCIES_INSTALL:BOOL=OFF
BuildSystem:	cmake

%patchlist
https://src.fedoraproject.org/rpms/OpenTimelineIO/raw/rawhide/f/cmake-install.patch
# Partial alternative to the above:
#https://github.com/AcademySoftwareFoundation/OpenTimelineIO/pull/1860.patch
OpenTimeLineIO-system-libs.patch

%description
OpenTimelineIO is an interchange format and API for editorial cut information.
OTIO contains information about the order and length of cuts and references to
external media. It is not however, a container format for media.

%package -n %{libname}
Summary:	Editorial timeline information API
Group:		System/Libraries

%description -n %{libname}
Editorial timeline information API

%package -n %{devname}
Summary:	Editorial timeline information API
Group:		System/Libraries
Requires:	%{libname} = %{EVRD}

%description -n %{devname}
Editorial timeline information API

%package -n python-opentimelineio
Summary:	Python bindings to the OpenTimeLineIO library
Group:		Libraries/Python
Requires:	%{libname} = %{EVRD}

%description -n python-opentimelineio
Python bindings to the OpenTimeLineIO library

%files -n %{libname}
%{_libdir}/libopentime.so.0.17.0
%{_libdir}/libopentimelineio.so.0.17.0

%files -n %{devname}
%{_includedir}/opentime
%{_includedir}/opentimelineio
%{_datadir}/cmake/opentime
%{_datadir}/cmake/opentimelineio
%{_libdir}/libopentime.so
%{_libdir}/libopentimelineio.so

%files -n python-opentimelineio
%{python3_sitearch}/opentimelineio
%{python3_sitearch}/opentimelineview
%{_libdir}/_opentime.cpython-*.so
%{_libdir}/_otio.cpython-*.so
