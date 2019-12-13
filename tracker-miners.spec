%global systemd_units tracker-extract.service tracker-miner-apps.service tracker-miner-fs.service tracker-writeback.service

Name: tracker-miners
Version: 2.1.5
Release: 5
Summary: the indexer daemon (tracker-miner-fs) and tools to extract metadata from many different filetypes.
License: GPLv2+ and LGPLv2+
URL: https://wiki.gnome.org/Projects/Tracker
Source0: https://download.gnome.org/sources/%{name}/2.1/%{name}-%{version}.tar.xz
Source1: tracker-miners.conf

BuildRequires: giflib-devel intltool libjpeg-devel libtiff-devel systemd vala
BuildRequires: pkgconfig(exempi-2.0) pkgconfig(flac) pkgconfig(gexiv2) pkgconfig(gstreamer-1.0)
BuildRequires: pkgconfig(gstreamer-pbutils-1.0) pkgconfig(gstreamer-tag-1.0) pkgconfig(icu-i18n)
BuildRequires: pkgconfig(icu-uc) pkgconfig(libexif) pkgconfig(libgsf-1) pkgconfig(libgxps)
BuildRequires: pkgconfig(libiptcdata) pkgconfig(libosinfo-1.0) pkgconfig(libpng) pkgconfig(libseccomp)
BuildRequires: pkgconfig(libxml-2.0) pkgconfig(poppler-glib) pkgconfig(taglib_c) pkgconfig(totem-plparser)
BuildRequires: pkgconfig(tracker-sparql-2.0) >= 2.1.0 pkgconfig(upower-glib) pkgconfig(vorbisfile)
Requires: tracker%{?_isa} >= 2.1.0

Obsoletes: tracker < 1.99.2
Conflicts: tracker < 1.99.2

%description
tracker-miners containsthe indexer daemon (tracker-miner-fs) and tools to extract metadata
from many different filetypes.

%package_help

%prep
%autosetup -n %{name}-%{version}

%build
%configure --disable-static --enable-libflac --enable-libvorbis --disable-mp3 \
           --disable-functional-tests --disable-silent-rules
%make_build

%install
%make_install
%delete_la
rm -rf %{buildroot}%{_datadir}/tracker-tests
rm -rf %{buildroot}%{_libdir}/%{name}-2.0/*.so
%find_lang %{name}

# remove rpath info
find %{buildroot}/ -type f -exec file {} ';' | grep "\<ELF\>" | grep -v 'libwriteback\|libtracker-extract' | awk -F ':' '{print $1}' | xargs -i chrpath --delete {}

install -d %{buildroot}%{_sysconfdir}/ld.so.conf.d
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf

%check

%pre

%preun
%systemd_user_preun %{systemd_units}

%post
%systemd_user_post %{systemd_units}

%postun
%systemd_user_postun_with_restart %{systemd_units}

%files -f %{name}.lang
%doc NEWS README
%license COPYING COPYING.LGPL COPYING.GPL AUTHORS
%config(noreplace) %{_sysconfdir}/xdg/autostart/tracker*.desktop
%{_userunitdir}/tracker*.service
%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf
%{_libdir}/%{name}-2.0/
%{_libexecdir}/tracker*
%{_datadir}/dbus-1/services/org.freedesktop.Tracker*
%{_datadir}/glib-2.0/schemas/*
%{_datadir}/tracker/
%{_datadir}/%{name}/

%files help
%{_mandir}/man1/tracker-*.1*

%changelog
* Mon Nov 11 2019 chengquan<chengquan3@huawei.com> - 2.1.5-5
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:remove rss service

* Thu Oct 31 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.1.5-4
- add Copyright in tracker-miners.conf.

* Mon Oct 21 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.1.5-3
- Package rebuild.

* Thu Sep 26 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.1.5-2
- Package init.
