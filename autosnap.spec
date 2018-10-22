Name:		autosnap
Version:	0.1.1
Release:	0%{?dist}
Summary:>-------Automatlly snapshot tool
Group:		Applications/System
License:	GPLv3

URL:		https://github.com/ZVampirEM77/autosnap
Source0:>-------https://github.com/ZVampirEM77/%{name}/archive/%{version}/%{name}.tar.gz
BuildArch:  noarch

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: systemd

%description
%prep
%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
%{__python} setup.py install --skip-build --root %{buildroot} --install-scripts %{_bindir}
mkdir -p %{buildroot}%{_unitdir}
install -m 0644 ./systemd/autosnap.service %{buildroot}%{_unitdir}

%post
/bin/systemctl --system enable autosnap &> /dev/null || :

%postun
%files
#%doc README
#%doc LICENSE
%{_bindir}/auto_snap
%{_unitdir}/autosnap.service
%{python2_sitelib}/*
