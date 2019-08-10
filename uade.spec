#%%define _default_patch_fuzz 2

Name:           uade
Version:        2.13
Release:        13%{?dist}
Summary:        Unix Amiga DeliTracker Emulator
Group:          Applications/Multimedia
License:        GPLv2+ and Distributable
URL:            http://zakalwe.fi/uade
Source0:        http://zakalwe.fi/%{name}/uade2/%{name}-%{version}.tar.bz2
Source1:        README_%{name}.txt
Patch0:         uade-2.13-makenamesane.patch
Patch1:         uade-2.13-fixaudaciousplugin.patch
Patch2:         uade-2.13-coreinstalldestdir.patch
Patch3:         uade-2.13-uade123installdestdir.patch
Patch4:         uade-2.13-xmmsinstalldestdir.patch
Patch5:         uade-2.13-audaciousinstalldestdir.patch
Patch6:         uade-2.13-uadefsinstalldestdir.patch
Patch7:         uade-2.13-uadeinstalldestdir.patch
Patch8:         uade-2.13-COMMONGCCOPTS.patch
BuildRequires:  gcc
BuildRequires:  fuse-devel
BuildRequires:  libao-devel
BuildRequires:  pkgconfig
BuildRequires:  xmms-devel

%description
UADE plays old Amiga tunes through UAE emulation and a cloned m68k-assembler
Eagleplayer API. The player infrastructure of UADE is built on the ground work
of the Eagleplayer and DeliTracker projects. UADE makes these external players
reusable on certain UNIX and other platforms. UADE contains a free
(as in freedom) implementation of Eagleplayer and DeliTracker API for UNIX
variants.


%package devel
Summary:        Development files for uade
Group:          Applications/Multimedia
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
Requires:       libao-devel

%description devel
Development files for uade


%package -n xmms-%{name}
Summary:        Unix Amiga DeliTracker Emulator XMMS plug-in
Group:          Applications/Multimedia
Requires:       %{name} = %{version}-%{release}
Requires:       xmms

%description -n xmms-%{name}
A plug-in for XMMS that makes use of UADE to play various Amiga music module
formats using external players.


%package mod2ogg
Summary:        Encode music modules to ogg/mp3/flac etc
Group:          Applications/Multimedia
Requires:       %{name} = %{version}-%{release}
Requires:       flac
Requires:       lame
Requires:       sox
Requires:       vorbis-tools

%description mod2ogg
Encode any music module format into an ogg, mp3, flac, cdr or wav file


%package -n fuse-uadefs
Summary:        Pseudo file system for playing music modules as WAVs
Group:          System Environment/Base
Requires:       %{name} = %{version}-%{release}
Requires:       fuse

%description -n fuse-uadefs
Pseudo file system for playing music modules as WAVs. This allows audio players
which do not support music modules, to play them.


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

# Encoding fixes
iconv -f iso8859-1 ChangeLog -t utf8 > ChangeLog.conv \
    && mv -f ChangeLog.conv ChangeLog

iconv -f iso8859-1 doc/UAE-README -t utf8 > UAE-README.conv \
    && mv -f UAE-README.conv doc/UAE-README

# Some renaming to keep things standard
sed -i 's|uade2\/|uade\/|g' doc/uade123.1
sed -i 's|\.uade2\/|\.uade\/|g' src/frontends/xmms/plugin.c \
    src/frontends/uadefs/uadefs.c src/frontends/uade123/uade123.c \
    src/frontends/common/uadeconf.c src/frontends/common/uadeconf.c
sed -i 's|\/\.uade2|\/\.uade|g' src/frontends/meta-input/uade123.sh


%build
%configure --with-text-scope
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
install -pm0644 %{SOURCE1} README.rpmfusion

# Permission fixes
chmod 644 %{buildroot}%{_mandir}/man1/*

# Place configs in a sane location and make symlinks
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
mv %{buildroot}%{_datadir}/%{name}/eagleplayer.conf %{buildroot}%{_sysconfdir}/%{name}
mv %{buildroot}%{_datadir}/%{name}/uade.conf %{buildroot}%{_sysconfdir}/%{name}
mv %{buildroot}%{_datadir}/%{name}/uaerc %{buildroot}%{_sysconfdir}/%{name}
ln -s ../../../etc/%{name}/eagleplayer.conf %{buildroot}%{_datadir}/%{name}
ln -s ../../../etc/%{name}/uade.conf %{buildroot}%{_datadir}/%{name}
ln -s ../../../etc/%{name}/uaerc %{buildroot}%{_datadir}/%{name}


%files
%{_bindir}/uade123
%{_libdir}/%{name}
%{_mandir}/man1/uade123.1.gz
%{_datadir}/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/eagleplayer.conf
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/uaerc
%doc AUTHORS ChangeLog doc/UAE-README
%doc doc/UAE-CREDITS doc/PLANS amigasrc/README
%license COPYING COPYING.GPL


%files mod2ogg
%{_bindir}/mod2ogg2.sh


%files devel
%{_libdir}/pkgconfig/%{name}.pc


%files -n xmms-%{name}
%{_bindir}/uadexmmsadd
%{_libdir}/xmms/Input/libuade2.so


%files -n fuse-uadefs
%{_bindir}/uadefs
%{_mandir}/man1/uadefs.1.gz


%changelog
* Sat Aug 10 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.13-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.13-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Aug 19 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.13-11
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <sergio@serjux.com> - 2.13-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar 02 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 2.13-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 2.13-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Mar 26 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 2.13-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Feb 22 2016 Sérgio Basto <sergio@serjux.com> - 2.13-6
- Fix FTBFS (rfbz#3800), with patch8, Fedora package already send common
  optimization flags.
- Add license tag.
- Trivial spec cleanups.

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 2.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Mar 12 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.13-4
- https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Feb 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 16 2010 Bernie Innocenti <bernie@codewiz.org> - 2.13-2
- Disable audacious plugin

* Sat Mar 13 2010 Ian Chapman <packages [AT] amiga-hardware [DOT] com> - 2.13-1
- Upgraded to 2.13
- Removed some redundant options to %%configure
- Added fuse-devel BR for uadefs
- Updated all patches
- Added missing %%defattr(-,root,root,-) to mod2ogg files section
- Removed some obsolete documentation
- Own /etc/uade
- Added uadefs sub-package, a pseudo file system for representing the modules
  as WAV files

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.09-5
- rebuild for new F11 features

* Sun Oct 19 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.09-4
- _default_patch_fuzz 2

* Sun Sep 14 2008 Xavier Lamien <lxtnow[at]gmail.com> - 2.09-3
- Update files and rebuild for rpmfusion.

* Sun Mar 23 2008 Ian Chapman <packages[AT]amiga-hardware.com> 2.09-2
- Rebuild against latest audacious to avoid undefined symbol: xmms_usleep
- Convert UAE-README to UTF8
- Convert ChangeLog to UTF8

* Sun Jan 06 2008 Ian Chapman <packages[AT]amiga-hardware.com> 2.09-1
- Upgrade to 2.09

* Sun Nov 18 2007 Ian Chapman <packages[AT]amiga-hardware.com> 2.08-1
- Upgrade to 2.08
- Dropped explicit support for FC-5 and earlier
- Updated usedestdir patch
- Added text scope support
- Added mod2ogg

* Sun May 06 2007 Ian Chapman <packages[AT]amiga-hardware.com> 2.07-1
- Upgrade to 2.07

* Thu Apr 26 2007 Ian Chapman <packages[AT]amiga-hardware.com> 2.06-1
- Upgrade to 2.06

* Tue Feb 13 2007 Ian Chapman <packages[AT]amiga-hardware.com> 2.05-1
- Upgrade to 2.05

* Thu Jan 25 2007 Ian Chapman <packages[AT]amiga-hardware.com> 2.04-1
- Upgrade to 2.04
- Renamed audacious-uade to audacious-plugins-uade to match other repos

* Wed Sep 06 2006 Ian Chapman <packages[AT]amiga-hardware.com> 2.03-2
- Moved .pc into separate -devel sub package
- Renamed sub package uade-xmms to xmms-uade
- Added audacious support for fc6+
- Patched so that uadecore is installed correctly on x86_64
- Patched so that the .pc file is installed correctly on x86_64

* Mon Sep 04 2006 Ian Chapman <packages[AT]amiga-hardware.com> 2.03-1
- Initial release
