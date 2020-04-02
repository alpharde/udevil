%global debug_package %{nil}

Name:		udevil		
Version:	0.4.5
Release:	1
Summary:	Mount and unmount without password
Group:		System Environment/Daemons
License:	GPLv3+
URL:		http://ignorantguru.github.com/udevil/
Source0:	https://raw.githubusercontent.com/IgnorantGuru/udevil/pkg/%{version}/udevil-%{version}.tar.xz
BuildRequires:	intltool, gettext
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gmodule-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gthread-2.0)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(libudev)

%description
udevil is a command line Linux program which mounts and unmounts 
removable devices without a password, shows device info, and monitors 
device changes. It can also mount ISO files, nfs://, smb://, ftp://, 
ssh:// and WebDAV URLs, and tmpfs/ramfs filesystems

%prep
%setup -q
sed -i 's/-o root -g root -m 4755//g' src/Makefile.in
sed -i '20i #include <sys/stat.h>' src/device-info.h

%build
%configure --libdir=%{_prefix}/lib
make %{?_smp_mflags}

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
make -C man %{?_smp_mflags} DESTDIR=%{buildroot} install
%find_lang %{name}

%pre
%service_add_pre devmon@.service

%preun
%service_del_preun devmon@.service

%post
%service_add_post devmon@.service

%postun
%service_del_postun devmon@.service

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING README
%dir %{_sysconfdir}/conf.d
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/conf.d/devmon
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%verify(not mode) %attr(0755,root,root) %{_bindir}/%{name}
%{_bindir}/devmon
%{_unitdir}/devmon@.service
%{_mandir}/man?/%{name}.?%{ext_man}

%changelog
