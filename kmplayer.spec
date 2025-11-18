#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define tde_pkg kmplayer
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_confdir %{_sysconfdir}/trinity
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%if 0%{?mdkversion}
%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1
%endif

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity
%global toolchain %(readlink /usr/bin/cc)


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.10.0c
Release:	%{?tde_version}_%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}
Summary:	Media player for Trinity
Group:		Applications/Multimedia
URL:		http://www.trinitydesktop.org/
#URL:		http://kmplayer.kde.org

%if 0%{?suse_version}
License:	GPL-2.0+
%else
License:	GPLv2+
%endif

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}

Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/multimedia/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildRequires:  cmake make
BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	trinity-tde-cmake >= %{tde_version}
%if "%{?toolchain}" != "clang"
BuildRequires:	gcc-c++
%endif
BuildRequires:	pkgconfig
BuildRequires:	libtool

# SUSE desktop files utility
%if 0%{?suse_version}
BuildRequires:	update-desktop-files
%endif

%if 0%{?opensuse_bs} && 0%{?suse_version}
# for xdg-menu script
BuildRequires:	brp-check-trinity
%endif

# DBUS support
%if 0%{?mgaversion} || 0%{?mdkversion} || 0%{?rhel} >= 5 || 0%{?fedora} || 0%{?suse_version}
BuildRequires:	trinity-dbus-tqt-devel >= %{tde_version}
%endif

# GSTREAMER support
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0)

# XINE support
%define with_xine 1
BuildRequires:  pkgconfig(libxine)

# X11 stuff
BuildRequires:  pkgconfig(xt)
BuildRequires:  pkgconfig(xv)

# GTK2 stuff
BuildRequires:  pkgconfig(gtk+-2.0)

# DBUS stuff
BuildRequires:  pkgconfig(dbus-glib-1)

# NSPR support
BuildRequires:  pkgconfig(nspr)

# Koffice support
BuildRequires:	trinity-koffice-devel

Requires:		%{name}-base = %{?epoch:%{epoch}:}%{version}-%{release}


%description
A basic audio/video viewer application for Trinity.

KMPlayer can:
* play DVD (DVDNav only with the Xine player)
* play VCD
* let the backend players play from a pipe (read from stdin)
* play from a TV device (experimental)
* show backend player's console output
* launch ffserver (only 0.4.8 works) when viewing from a v4l device
* DCOP KMediaPlayer interface support
* VDR viewer frontend (with *kxvplayer), configure VDR keys with standard TDE
  shortcut configure window
* Lots of configurable shortcuts. Highly recommended for the VDR keys
  (if you have VDR) and volume increase/decrease

%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog INSTALL README.md TODO
%{tde_bindir}/kmplayer
%{tde_bindir}/knpplayer
%{tde_bindir}/kxvplayer
%{tde_datadir}/services/kmplayer_koffice.desktop
%{tde_libdir}/libkmplayercommon.so.1
%{tde_libdir}/libkmplayercommon.so.1.0.0
%{tde_libdir}/libtdeinit_kmplayer.la
%{tde_libdir}/libtdeinit_kmplayer.so
%{tde_tdelibdir}/kmplayer.la
%{tde_tdelibdir}/kmplayer.so
%{tde_tdelibdir}/libkmplayerkofficepart.la
%{tde_tdelibdir}/libkmplayerkofficepart.so
%{tde_tdeappdir}/kmplayer.desktop

%exclude %{tde_datadir}/apps/kmplayer/bookmarks.xml
%exclude %{tde_datadir}/apps/kmplayer/kmplayerpartui.rc
%exclude %{tde_datadir}/apps/kmplayer/noise.gif
%exclude %{tde_datadir}/apps/kmplayer/pluginsinfo
%{tde_datadir}/apps/kmplayer/

##########

%package base
Group:			Applications/Multimedia
Summary:		Base files for KMPlayer [Trinity]

%description base
Core files needed for KMPlayer.

%files base
%defattr(-,root,root,-)
%{tde_bindir}/kgstplayer
%{tde_bindir}/kxineplayer
%dir %{tde_datadir}/config
%config(noreplace) %{tde_datadir}/config/kmplayerrc
%{tde_datadir}/apps/kmplayer/bookmarks.xml
%{tde_datadir}/apps/kmplayer/noise.gif
%{tde_datadir}/icons/hicolor/*/apps/kmplayer.png
%{tde_datadir}/icons/hicolor/*/apps/kmplayer.svgz
%{tde_datadir}/mimelnk/application/x-kmplayer.desktop
%{tde_datadir}/mimelnk/video/x-ms-wmp.desktop
%{tde_mandir}/man1/kmplayer.1*

##########

%package konq-plugins
Group:			Applications/Multimedia
Requires:		%{name}-base = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:		trinity-konqueror >= %{tde_version}
Summary:		KMPlayer plugin for KHTML/Konqueror [Trinity]

%description konq-plugins
This plugin enables audio/video playback inside konqueror, using Xine (with
*kxineplayer) or GStreamer (with *kgstplayer), such as movie trailers, web
tv or radio. It mimics QuickTime, MS Media Player and RealPlayer plugin
browser plugins.

%files konq-plugins
%defattr(-,root,root,-)
%{tde_tdelibdir}/libkmplayerpart.la
%{tde_tdelibdir}/libkmplayerpart.so
%{tde_datadir}/apps/kmplayer/kmplayerpartui.rc
%{tde_datadir}/apps/kmplayer/pluginsinfo
%{tde_datadir}/services/kmplayer_part.desktop

##########

%package doc
Group:			Applications/Multimedia
Requires:		%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Summary:		Handbook for KMPlayer [Trinity]

%description doc
Documention for KMPlayer, a basic audio/video viewer application for TDE.

%files doc
%defattr(-,root,root,-)
%{tde_tdedocdir}/HTML/*/kmplayer

##########

%package devel
Group:			Applications/Multimedia
Requires:		%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Summary:		Media player for Trinity (devlopment files)

%description devel
Development files for KMPlayer, a basic audio/video viewer application for TDE.

%files devel
%defattr(-,root,root,-)
%{tde_libdir}/libkmplayercommon.la
%{tde_libdir}/libkmplayercommon.so

##########

%if 0%{?suse_version} && 0%{?opensuse_bs} == 0
%debug_package
%endif

##########

%prep
%autosetup -n %{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig:${PKG_CONFIG_PATH}"

if ! rpm -E %%cmake|grep -e 'cd build\|cd ${CMAKE_BUILD_DIR:-build}'; then
  %__mkdir_p build
  cd build
fi

%cmake \
  -DCMAKE_BUILD_TYPE="RelWithDebInfo" \
  -DCMAKE_C_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_CXX_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_SKIP_RPATH=OFF \
  -DCMAKE_SKIP_INSTALL_RPATH=OFF \
  -DCMAKE_INSTALL_RPATH="%{tde_libdir}" \
  -DCMAKE_VERBOSE_MAKEFILE=ON \
  -DWITH_GCC_VISIBILITY=OFF \
  \
  -DCMAKE_INSTALL_PREFIX=%{tde_prefix} \
  -DINCLUDE_INSTALL_DIR=%{tde_tdeincludedir} \
  -DLIB_INSTALL_DIR=%{tde_libdir} \
  -DSHARE_INSTALL_PREFIX=%{tde_datadir} \
  \
  -DWITH_ALL_OPTIONS=ON \
  -DBUILD_ALL=ON \
  ..

%__make %{?_smp_mflags} || %__make


%install
export PATH="%{tde_bindir}:${PATH}"
%__make install DESTDIR=%{buildroot} -C build

%find_lang %{tde_pkg}

# Removes unwanted files
%__rm -f %{?buildroot}%{tde_datadir}/mimelnk/application/x-mplayer2.desktop

# Updates applications categories for openSUSE
%if 0%{?suse_version}
%suse_update_desktop_file -r "%{tde_pkg}" TDE AudioVideo Player Video
%endif

