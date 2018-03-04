Summary:	XBLAS - Extra Precise Basic Linear Algebra Subroutines
Summary(pl.UTF-8):	XBLAS - procedury BLAS rozszerzonej precyzji
Name:		xblas
Version:	1.0.248
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://www.netlib.org/xblas/%{name}-%{version}.tar.gz
# Source0-md5:	990c680fb5e446bb86c10936e4cd7f88
URL:		http://www.netlib.org/xblas/
BuildRequires:	gcc-fortran
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The XBLAS library of routines is part of a reference implementation
for the Dense and Banded Basic Linear Algebra Subroutines, along with
their Extended and Mixed Precision versions, as documented in Chapters
2 and 4 of the new BLAS Standard.

%description -l pl.UTF-8
Biblioteka procedur XBLAS to część implementacji referencyjnej
standardu Dense and Banded Basic Linear Algebra Subroutines
(gęste i pasmowe podstawowe procedury algebry liniowej), wraz z
wersjami o rozszerzonej i mieszanej precyzji, zgodna z dokumentacją w
rozdziałach 2 i 4 nowego standardu BLAS.

%package devel
Summary:	Header files for XBLAS library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki XBLAS
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for XBLAS library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki XBLAS.

%package static
Summary:	Static XBLAS library
Summary(pl.UTF-8):	Statyczna biblioteka XBLAS
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static XBLAS library.

%description static -l pl.UTF-8
Statyczna biblioteka XBLAS.

%package doc
Summary:	XBLAS documentation
Summary(pl.UTF-8):	Dokumentacja projektu XBLAS
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc
XBLAS documentation.

%description doc -l pl.UTF-8
Dokumentacja projektu XBLAS.

%prep
%setup -q

%build
CFLAGS="%{rpmcflags} -fPIC"
%configure \
	%{!?with_static_libs:--disable-static}

%{__make} -j1

%{__cc} -shared -o libxblas.so.%{version} -Wl,-soname,libxblas.so.1 -Wl,--whole-archive libxblas.a -Wl,--no-whole-archive

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}/xblas}

install libxblas.so.%{version} $RPM_BUILD_ROOT%{_libdir}
ln -sf libxblas.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libxblas.so.1
ln -sf libxblas.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libxblas.so
cp -p libxblas.a $RPM_BUILD_ROOT%{_libdir}
cp -p src/*.h $RPM_BUILD_ROOT%{_includedir}/xblas

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README
%attr(755,root,root) %{_libdir}/libxblas.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libxblas.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libxblas.so
%dir %{_includedir}/xblas
%{_includedir}/xblas/blas_*.h
%{_includedir}/xblas/f2c-bridge.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libxblas.a

%files doc
%defattr(644,root,root,755)
%doc doc/report.ps
