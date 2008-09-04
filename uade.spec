Name:           uade
Version:        2.09
Release:        2%{?dist}
Summary:        Unix Amiga Delitracker Emulator
Group:          Applications/Multimedia
License:        GPLv2+ and Distributable
URL:            http://zakalwe.fi/uade
Source0:        http://zakalwe.fi/%{name}/uade2/%{name}-%{version}.tar.bz2
Source1:        README_%{name}.txt
Patch0:         %{name}-2.08-usedestdir.patch
Patch1:         %{name}-2.03-makenamesane.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  audacious-devel
BuildRequires:  libao-devel
BuildRequires:  pkgconfig
BuildRequires:  xmms-devel


%description
UADE plays old Amiga tunes through UAE emulation and a cloned m68k-assembler
Eagleplayer API. The player infrastructure of UADE is built on the ground work
of the Eagleplayer and Delitracker projects. UADE makes these external players
reusable on certain UNIX and other platforms. UADE contains a free
(as in freedom) implementation of Eagleplayer and Delitracker API for UNIX
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
Summary:        Unix Amiga Delitracker Emulator XMMS plugin
Group:          Applications/Multimedia
Requires:       %{name} = %{version}-%{release}
Requires:       xmms

%description -n xmms-%{name}
A plugin for XMMS that makes use of UADE to play various Amiga music module
formats using external players.


%package -n audacious-plugins-%{name}
Summary:        Unix Amiga Delitracker Emulator audacious plugin
Group:          Applications/Multimedia
Requires:       %{name} = %{version}-%{release}
Requires:       audacious

%description -n audacious-plugins-%{name}
A plugin for audacious that makes use of UADE to play various Amiga music
module formats using external players


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


%prep
%setup -q
%patch -p1
%patch1 -p1

# Encoding fixes
iconv -f iso8859-1 ChangeLog -t utf8 > ChangeLog.conv \
    && mv -f ChangeLog.conv ChangeLog

iconv -f iso8859-1 doc/UAE-README -t utf8 > UAE-README.conv \
    && mv -f UAE-README.conv doc/UAE-README


%build
%configure --with-uade123 --with-xmms --with-audacious --with-text-scope
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
install -pm0644 %{SOURCE1} README.dribble

# Place configs in a sane location and make symlinks
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
mv %{buildroot}%{_datadir}/%{name}/eagleplayer.conf %{buildroot}%{_sysconfdir}/%{name}
mv %{buildroot}%{_datadir}/%{name}/uade.conf %{buildroot}%{_sysconfdir}/%{name}
mv %{buildroot}%{_datadir}/%{name}/uaerc %{buildroot}%{_sysconfdir}/%{name}
ln -s ../../../etc/%{name}/eagleplayer.conf %{buildroot}%{_datadir}/%{name}
ln -s ../../../etc/%{name}/uade.conf %{buildroot}%{_datadir}/%{name}
ln -s ../../../etc/%{name}/uaerc %{buildroot}%{_datadir}/%{name}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_bindir}/uade123
%{_libdir}/%{name}
%{_mandir}/man1/uade123.1.gz
%{_datadir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/eagleplayer.conf
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/uaerc
%doc AUTHORS ChangeLog COPYING COPYING.GPL doc/BUGS doc/UAE-README
%doc doc/UAE-CREDITS doc/PLANS amigasrc/README README.dribble


%files mod2ogg
%{_bindir}/mod2ogg2.sh


%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/%{name}.pc


%files -n xmms-%{name}
%defattr(-,root,root,-)
%{_bindir}/uadexmmsadd
%{_libdir}/xmms/Input/libuade2.so


%files -n audacious-plugins-%{name}
%defattr(-,root,root,-)
%{_libdir}/audacious/Input/libuade2.so


%changelog
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

* Thu Feb 13 2007 Ian Chapman <packages[AT]amiga-hardware.com> 2.05-1
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
