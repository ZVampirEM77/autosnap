Name:		autosnap
Version:	0.1
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
install -m 0644 %{_unitdir}/autosnap.service %{buildroot}%{_unitdir}
#mkdir -p %{buildroot}%{_mandir}/man8
#install -m 0644 gwcli.8 %{buildroot}%{_mandir}/man8/
#mkdir -p %{buildroot}%{_sysconfdir}/systemd/system/umstor-iscsi-proxy.service.d
#install -m 0644 .%{_sysconfdir}/systemd/system/rbd-target-gw.service.d/dependencies.conf %{buildroot}%{_sysconfdir}/systemd/system/rbd-target-gw.service.d/

%post
#/bin/systemctl --system daemon-reload &> /dev/null || :
/bin/systemctl --system enable autosnap &> /dev/null || :

%postun
%files
#%doc README
#%doc LICENSE
%{_bindir}/auto_snap
%{_unitdir}/autosnap.service
%{python2_sitelib}/*
