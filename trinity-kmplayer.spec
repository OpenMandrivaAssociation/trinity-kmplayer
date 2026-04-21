%bcond clang 1
%bcond xine 1

# TDE variables
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif

%define tde_pkg kmplayer
%define tde_prefix /opt/trinity


%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity


Name:		trinity-%{tde_pkg}
Version:	0.10.0c
Release:	%{?tde_version:%{tde_version}_}3
Summary:	Media player for Trinity
Group:		Applications/Multimedia
URL:		http://www.trinitydesktop.org/
#URL:		http://kmplayer.kde.org

License:	GPLv2+


Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/multimedia/%{tarball_name}-%{tde_version}.tar.xz

BuildSystem:    cmake

BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DCMAKE_INSTALL_PREFIX=%{tde_prefix}
BuildOption:    -DINCLUDE_INSTALL_DIR=%{tde_prefix}/include/tde
BuildOption:    -DSHARE_INSTALL_PREFIX=%{tde_prefix}/share
BuildOption:    -DWITH_ALL_OPTIONS=ON
BuildOption:    -DBUILD_ALL=ON
BuildOption:    -DWITH_GCC_VISIBILITY=%{!?with_clang:ON}%{?with_clang:OFF}

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
# Koffice support
BuildRequires:	trinity-koffice-devel >= %{tde_version}

BuildRequires:	desktop-file-utils

BuildRequires:	trinity-tde-cmake >= %{tde_version}

%{!?with_clang:BuildRequires:	gcc-c++}

BuildRequires:	pkgconfig
BuildRequires:	libtool

# DBUS support
BuildRequires:	trinity-dbus-tqt-devel >= %{tde_version}


# GSTREAMER support
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0)

# XINE support
%{?with_xine:BuildRequires:  pkgconfig(libxine)}

# X11 stuff
BuildRequires:  pkgconfig(xt)
BuildRequires:  pkgconfig(xv)

# GTK2 stuff
BuildRequires:  pkgconfig(gtk+-2.0)

# DBUS stuff
BuildRequires:  pkgconfig(dbus-glib-1)

# NSPR support
BuildRequires:  pkgconfig(nspr)

Requires:		%{name}-base = %{EVRD}


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
%{tde_prefix}/bin/kmplayer
%{tde_prefix}/bin/knpplayer
%{tde_prefix}/bin/kxvplayer
%{tde_prefix}/share/services/kmplayer_koffice.desktop
%{tde_prefix}/%{_lib}/libkmplayercommon.so.1
%{tde_prefix}/%{_lib}/libkmplayercommon.so.1.0.0
%{tde_prefix}/%{_lib}/libtdeinit_kmplayer.la
%{tde_prefix}/%{_lib}/libtdeinit_kmplayer.so
%{tde_prefix}/%{_lib}/trinity/kmplayer.la
%{tde_prefix}/%{_lib}/trinity/kmplayer.so
%{tde_prefix}/%{_lib}/trinity/libkmplayerkofficepart.la
%{tde_prefix}/%{_lib}/trinity/libkmplayerkofficepart.so
%{tde_prefix}/share/applications/tde/kmplayer.desktop

%exclude %{tde_prefix}/share/apps/kmplayer/bookmarks.xml
%exclude %{tde_prefix}/share/apps/kmplayer/kmplayerpartui.rc
%exclude %{tde_prefix}/share/apps/kmplayer/noise.gif
%exclude %{tde_prefix}/share/apps/kmplayer/pluginsinfo
%{tde_prefix}/share/apps/kmplayer/

##########

%package base
Group:			Applications/Multimedia
Summary:		Base files for KMPlayer [Trinity]

%description base
Core files needed for KMPlayer.

%files base
%defattr(-,root,root,-)
%{tde_prefix}/bin/kgstplayer
%{tde_prefix}/bin/kxineplayer
%dir %{tde_prefix}/share/config
%config(noreplace) %{tde_prefix}/share/config/kmplayerrc
%{tde_prefix}/share/apps/kmplayer/bookmarks.xml
%{tde_prefix}/share/apps/kmplayer/noise.gif
%{tde_prefix}/share/icons/hicolor/*/apps/kmplayer.png
%{tde_prefix}/share/icons/hicolor/*/apps/kmplayer.svgz
%{tde_prefix}/share/mimelnk/application/x-kmplayer.desktop
%{tde_prefix}/share/mimelnk/video/x-ms-wmp.desktop
%{tde_prefix}/share/man/man1/kmplayer.1*

##########

%package konq-plugins
Group:			Applications/Multimedia
Requires:		%{name}-base = %{EVRD}
Requires:		trinity-konqueror >= %{tde_version}
Summary:		KMPlayer plugin for KHTML/Konqueror [Trinity]

%description konq-plugins
This plugin enables audio/video playback inside konqueror, using Xine (with
*kxineplayer) or GStreamer (with *kgstplayer), such as movie trailers, web
tv or radio. It mimics QuickTime, MS Media Player and RealPlayer plugin
browser plugins.

%files konq-plugins
%defattr(-,root,root,-)
%{tde_prefix}/%{_lib}/trinity/libkmplayerpart.la
%{tde_prefix}/%{_lib}/trinity/libkmplayerpart.so
%{tde_prefix}/share/apps/kmplayer/kmplayerpartui.rc
%{tde_prefix}/share/apps/kmplayer/pluginsinfo
%{tde_prefix}/share/services/kmplayer_part.desktop

##########

%package doc
Group:			Applications/Multimedia
Requires:		%{name} = %{EVRD}
Summary:		Handbook for KMPlayer [Trinity]

%description doc
Documention for KMPlayer, a basic audio/video viewer application for TDE.

%files doc
%defattr(-,root,root,-)
%{tde_prefix}/share/doc/tde/HTML/*/kmplayer

##########

%package devel
Group:			Applications/Multimedia
Requires:		%{name} = %{EVRD}
Summary:		Media player for Trinity (devlopment files)

%description devel
Development files for KMPlayer, a basic audio/video viewer application for TDE.

%files devel
%defattr(-,root,root,-)
%{tde_prefix}/%{_lib}/libkmplayercommon.la
%{tde_prefix}/%{_lib}/libkmplayercommon.so


%conf -p
unset QTDIR QTINC QTLIB
export PATH="%{tde_prefix}/bin:${PATH}"
export PKG_CONFIG_PATH="%{tde_prefix}/%{_lib}/pkgconfig:${PKG_CONFIG_PATH}"


%install -a
%find_lang %{tde_pkg}

# Removes unwanted files
%__rm -f %{?buildroot}%{tde_prefix}/share/mimelnk/application/x-mplayer2.desktop

