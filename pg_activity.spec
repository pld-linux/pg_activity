# TODO:
#  Fix FATAL: 'PSProcess' object has no attribute 'get_memory_percent'
#  Move man dir to proper place ?

# NOTE:
#  Not sure if should be build as separte packages for py 3.x / 2.x  and binary package ?
#  Are modules used by other soft? If not just switch to py 3.x when there is release available

# Conditional build:
%bcond_with	doc		# don't build doc
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module

%define 	module	pgactivity
Summary:	-
Summary(pl.UTF-8):	-
# Name must match the python module/package name (as in 'import' statement)
Name:		pg_activity
Version:	1.2.0
Release:	0.1
License:	distributable
Group:		Libraries/Python
Source0:	https://github.com/julmon/pg_activity/archive/v%{version}.tar.gz
# Source0-md5:	1c75bdc026312b322e24fe6492ce6b5f
URL:		https://github.com/julmon/pg_activity
BuildRequires:	rpm-pythonprov
# remove BR: python-devel for 'noarch' packages.
# if py_postclean is used
BuildRequires:	rpmbuild(macros) >= 1.219
# if py3* macros are used
BuildRequires:	rpmbuild(macros) >= 1.612
# when using /usr/bin/env or other in-place substitutions
#BuildRequires:	sed >= 4.0
# when python3 present
%if %{with python2}
BuildRequires:	python-psutil
BuildRequires:	python-psycopg2 >= 2.2.1
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules
BuildRequires:	python3-psutil
BuildRequires:	python3-psycopg2 >= 2.2.1
BuildRequires:	python3-setuptools
%endif
# Below Rs only work for main package (python2)
#Requires:		python-libs
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
htop like application for PostgreSQL server activity monitoring

%description -l pl.UTF-8
Podobna do htop aplikacja monitorująca aktywność PostgresSQL

%package -n python3-%{module}
Summary:	-
Summary(pl.UTF-8):	-
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{module}

%description -n python3-%{module} -l pl.UTF-8

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
# %setup -q -n %{module}-%{version}
%setup -q

# setup copy of source in py3 dir
set -- *
install -d py3
cp -a "$@" py3

%build
%if %{with python2}
%{__python} setup.py build --build-base build-2 %{?with_tests:test} --with-man
%endif

%if %{with python3}
%{__python3} setup.py build --build-base build-3 %{?with_tests:test} --with-man
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%{__python} setup.py \
	build --build-base build-2 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean
%endif

%if %{with python3}
%{__python3} setup.py \
	build --build-base build-3 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%endif


%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.md docs
%dir %{py_sitescriptdir}/%{module}
%{py_sitescriptdir}//%{module}/*.py[co]
%attr(755,root,root) %{_bindir}/pg_activity
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/%{name}-%{version}-py*.egg-info
%endif
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README.md docs
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
