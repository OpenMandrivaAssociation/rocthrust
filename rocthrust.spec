# HIP port of Thrust (header-only) (TheRock 7.14)
%global debug_package %{nil}

Name:		rocthrust
Version:	7.14.0
Release:	1
Summary:	HIP port of Thrust (header-only)
License:	Apache-2.0 AND BSD-3-Clause AND MIT
Group:		Development/C++
URL:		https://github.com/ROCm/rocm-libraries
Source0:	https://github.com/ROCm/rocm-libraries/releases/download/therock-7.14/rocthrust.tar.gz#/rocthrust-%{version}.tar.gz

BuildRequires:	rocm-rpm-macros
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	rocm-cmake
BuildRequires:	hipcc
BuildRequires:	rocminfo
BuildRequires:	clang-tools
BuildRequires:	rocm-hip-devel
BuildRequires:	clang >= %{rocm_llvm_maj_ver}
BuildRequires:	rocprim-devel

ExclusiveArch:	%{x86_64} %{aarch64}

%description
rocThrust is a HIP port of Thrust on rocPRIM. Header-only package. GPU targets include gfx803.

%package devel
Summary:	Development files for rocthrust
Group:		Development/C++
Requires:	%{name} = %{version}-%{release}
Requires:	rocm-hip-devel
Requires:	rocprim-devel
Provides:	rocthrust-devel = %{EVRD}

%description devel
Headers and CMake package for rocthrust.

%prep
%autosetup -n rocthrust

export CXX=hipcc
export CC=clang
# Strip host-only -mfpmath (hipcc forwards flags to amdgcn device compiles)
CXXFLAGS=$(printf '%s' "%{optflags}" | sed 's/-mfpmath=sse//g')
export CXXFLAGS
export CFLAGS="$CXXFLAGS"
%cmake %{rocm_cmake_fhs} %{rocm_cmake_gpu_targets_prim} \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_CXX_COMPILER=hipcc \
	-DCMAKE_CXX_FLAGS="$CXXFLAGS" \
	-DBUILD_TEST=OFF \
	-DBUILD_BENCHMARK=OFF \
	-DBUILD_EXAMPLE=OFF \
	-DBUILD_DOCS=OFF \
	-DROCM_PATH=%{_prefix} \
	-DCMAKE_PREFIX_PATH=%{_prefix} \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build
if [ -d %{buildroot}/usr/lib/cmake/rocthrust ] && [ ! -d %{buildroot}%{_libdir}/cmake/rocthrust ]; then
	mkdir -p %{buildroot}%{_libdir}/cmake
	mv %{buildroot}/usr/lib/cmake/rocthrust %{buildroot}%{_libdir}/cmake/
	rmdir %{buildroot}/usr/lib/cmake 2>/dev/null || true
	rmdir %{buildroot}/usr/lib 2>/dev/null || true
fi

%files
%license LICENSE
%doc README.md
%exclude %{_docdir}/rocthrust/LICENSE

%files devel
%{_includedir}/thrust/
%{_libdir}/cmake/rocthrust/
