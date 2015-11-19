# TODO:
#  Fix FATAL: 'PSProcess' object has no attribute 'get_memory_percent'
#  Move man dir to proper place ?

# NOTE:
#  Not sure if should be build as separte packages for py 3.x / 2.x  and binary package ?
#  Are modules used by other soft? If not just switch to py 3.x when there is release available

# Conditional build:
%bcond_without	tests	# do not perform "make test"

%define 	module	pgactivity
Summary:	A top like application for PostgreSQL server activity monitoring
Name:		pg_activity
Version:	1.2.0
Release:	0.1
License:	distributable
Group:		Libraries/Python
Source0:	https://github.com/julmon/pg_activity/archive/v%{version}.tar.gz
# Source0-md5:	1c75bdc026312b322e24fe6492ce6b5f
URL:		https://github.com/julmon/pg_activity
BuildRequires:	python-psutil
BuildRequires:	python-psycopg2 >= 2.2.1
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.612
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
htop like application for PostgreSQL server activity monitoring

%description -l pl.UTF-8
Podobna do htop aplikacja monitorująca aktywność PostgresSQL

%prep
%setup -q

%build
%{__python} setup.py build %{?with_tests:test} \
	--with-man

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/pg_activity
%dir %{py_sitescriptdir}/%{module}
%{py_sitescriptdir}//%{module}/*.py[co]
%{py_sitescriptdir}/%{name}-%{version}-py*.egg-info
