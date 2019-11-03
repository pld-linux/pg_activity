# TODO:
#  Move man dir to proper place ?

# NOTE:
#  Not sure if should be build as separate packages for py 3.x / 2.x  with different binaries? Same conflicting binaries?
#  Are modules used by other soft? For now, just switch to py 3.x.

# Conditional build:
%bcond_without	tests	# do not perform "make test"
# NOTE: building both python2 and python3 results with broken "binaries"
%bcond_with	python2 # CPython 2.x module  
%bcond_without	python3 # CPython 3.x module

%define		module	pgactivity
Summary:	A top like application for PostgreSQL server activity monitoring
Name:		pg_activity
Version:	1.3.1
Release:	4
License:	distributable
Group:		Libraries/Python
Source0:	https://github.com/julmon/pg_activity/archive/v%{version}.tar.gz
# Source0-md5:	273eb398eee15a66ba532a576e9da7da
URL:		https://github.com/julmon/pg_activity
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
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
Requires:	python-modules
Requires:	python-psutil
Requires:	python-psycopg2
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
Requires:	python3-psutil
Requires:	python3-psycopg2

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
%setup -q

%build
%if %{with python2}
%py_build
%endif

%if %{with python3}
%py3_build
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python3}
%py3_install
%endif

%if %{with python2}
rm -r $RPM_BUILD_ROOT%{_bindir}
%py_install
%py_postclean
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/pg_activity
%dir %{py_sitescriptdir}/%{module}
%{py_sitescriptdir}//%{module}/*.py[co]
%{py_sitescriptdir}/%{name}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README.md docs
%attr(755,root,root) %{_bindir}/pg_activity
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{name}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
