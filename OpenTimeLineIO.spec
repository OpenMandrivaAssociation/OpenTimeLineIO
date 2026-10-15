%define libname %mklibname opentimelineio
%define devname %mklibname -d opentimelineio

Name:		OpenTimeLineIO
Version:	0.18.1
Release:	2
Source0:	https://github.com/AcademySoftwareFoundation/OpenTimelineIO/archive/refs/tags/v%{version}/%{name}-%{version}.tar.gz
Summary:	Editorial timeline information API
URL:		https://github.com/AcademySoftwareFoundation/OpenTimelineIO
License:	Apache-2.0 and MIT
Group:		System/Libraries
BuildRequires:	cmake
BuildRequires:	cmake(pybind11)
BuildRequires:	cmake(RapidJSON)
BuildRequires:	cmake(Imath)
BuildRequires:	pkgconfig(python3)
BuildRequires:	python%{pyver}dist(pybind11)
BuildOption:	-DCMAKE_CXX_STANDARD=23
BuildOption:	-DOTIO_CXX_INSTALL:BOOL=ON
BuildOption:	-DOTIO_PYTHON_INSTALL:BOOL=ON
BuildOption:	-DOTIO_PYTHON_INSTALL_DIR=%{python3_sitearch}
BuildOption:	-DOTIO_FIND_IMATH:BOOL=ON
BuildOption:	-DOTIO_FIND_RAPIDJSON:BOOL=ON
BuildOption:	-DUSE_DEPS_IMATH:BOOL=OFF
BuildOption:	-DOTIO_SHARED_LIBS:BOOL=ON
BuildOption:	-DBUILD_SHARED_LIBS:BOOL=ON
BuildOption:	-DOTIO_DEPENDENCIES_INSTALL:BOOL=OFF
BuildSystem:	cmake

%patchlist
# dropped (no longer applies): https://src.fedoraproject.org/rpms/OpenTimelineIO/raw/rawhide/f/cmake-install.patch
# Partial alternative to the above:
#https://github.com/AcademySoftwareFoundation/OpenTimelineIO/pull/1860.patch
# dropped (no longer applies): OpenTimeLineIO-system-libs.patch

%prep -a
# The GitHub archive does not ship the pybind11 submodule.
# Imported pybind11 targets must be GLOBAL: this file is added from a
# subdirectory, and the Python bindings are configured from the top level.
sed -i 's/add_subdirectory(pybind11)/find_package(pybind11 CONFIG REQUIRED GLOBAL)/' src/deps/CMakeLists.txt

%install -a
# Upstream installs the C++ libraries inside the Python package directory
# and the CMake configs under /usr/share/opentime{,lineio}. Neither is on
# the default linker or CMake search path, so kdenlive cannot see them.
otio_py=%{buildroot}%{python3_sitearch}/opentimelineio
mv ${otio_py}/libopentime.so* %{buildroot}%{_libdir}/
mv ${otio_py}/libopentimelineio.so* %{buildroot}%{_libdir}/
sed -i 's|%{python3_sitearch}/opentimelineio/|%{_libdir}/|g' \
	%{buildroot}%{_datadir}/opentime/*.cmake \
	%{buildroot}%{_datadir}/opentimelineio/*.cmake
mkdir -p %{buildroot}%{_libdir}/cmake/OpenTime
mkdir -p %{buildroot}%{_libdir}/cmake/OpenTimelineIO
# The generated configs compute their prefix as two directories above
# themselves, which is /usr only while they stay in /usr/share/<name>.
cat > %{buildroot}%{_libdir}/cmake/OpenTime/OpenTimeConfig.cmake << 'EOF'
include("%{_datadir}/opentime/OpenTimeConfig.cmake")
EOF
cat > %{buildroot}%{_libdir}/cmake/OpenTimelineIO/OpenTimelineIOConfig.cmake << 'EOF'
include("%{_datadir}/opentimelineio/OpenTimelineIOConfig.cmake")
EOF

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
# SONAME for 0.18 is 18. The libraries are on the default linker path.
# The Python extension has no RPATH and loads them from there.
%{_libdir}/libopentime.so.*
%{_libdir}/libopentimelineio.so.*

%files -n %{devname}
%{_includedir}/opentime
%{_includedir}/opentimelineio
%{_datadir}/opentime
%{_datadir}/opentimelineio
%{_libdir}/cmake/OpenTime
%{_libdir}/cmake/OpenTimelineIO
%{_libdir}/libopentime.so
%{_libdir}/libopentimelineio.so

%files -n python-opentimelineio
%{python3_sitearch}/opentimelineio
