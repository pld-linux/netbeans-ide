Summary:	NetBeans IDE - The Smarter and Faster Way to Code
Name:		netbeans-ide
Version:	7.4
Release:	0.3
License:	CDDL v1.0 and GPL v2 and others
Group:		Development/Tools
# https://netbeans.org/downloads/zip.html
Source0:	http://download.netbeans.org/netbeans/%{version}/final/zip/netbeans-%{version}-201310111528.zip
# NoSource0-md5:	c78db3817710d8c1639664d212b505ce
# NoSource, because huge download
NoSource:	0
Source1:	netbeans.desktop
URL:		https://netbeans.org/features/
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	unzip
Requires:	desktop-file-utils
Requires:	jre >= 1.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir		%{_prefix}/lib/%{name}

%description
NetBeans IDE lets you quickly and easily develop Java desktop, mobile,
and web applications, as well as HTML5 applications with HTML,
JavaScript, and CSS.

The IDE also provides a great set of tools for PHP and C/C++
developers. It is free and open source and has a large community of
users and developers around the world.

%package javase
Summary:	NetBeans Java development
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-websvc = %{version}-%{release}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description javase
This package contains the Java related parts of NetBeans.

%package cpp
Summary:	NetBeans C++ development
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}

%description cpp
This package contains the C++ related parts of NetBeans.

%package javacard
Summary:	NetBeans Javacard development
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-javase = %{version}-%{release}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description javacard
This package contains the Javacard related parts of NetBeans.

%package ruby
Summary:	NetBeans Ruby development
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}

%description ruby
This package contains the Ruby related parts of NetBeans.

%package groovy
Summary:	NetBeans Groovy development
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description groovy
This package contains the Groovy related parts of NetBeans.

%package php
Summary:	NetBeans PHP development
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-websvc = %{version}-%{release}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description php
This package contains the PHP related parts of NetBeans.

%package mobile
Summary:	NetBeans Java Mobile development
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-javase = %{version}-%{release}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description mobile
This package contains the Java Mobile related parts of NetBeans.

%package java
Summary:	NetBeans Java Enterprise development
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-javase = %{version}-%{release}
Requires:	%{name}-mobile = %{version}-%{release}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description java
This package contains the Java Enterprise related parts of NetBeans.

%package websvc
Summary:	NetBeans websvccommon
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description websvc
This package contains the websvccommon related parts of Netbeans

%package javafx
Summary:	NetBeans javafx
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description javafx
This package contains the javafx related parts of Netbeans

%prep
%setup -qc
mv netbeans/* .; rmdir netbeans

# remove windows executables and libraries
find -type f -name "*.exe" -print -delete
find -type f -name "*.bat" -print -delete
find -type f -name "*.dll" -print -delete
# remove macos executables and libraries
find -type f -name "*.cmd" -print -delete
find -type f -name "*.dylib" -print -delete
# remove NON-Linux libraries
find -type d -maxdepth 5 -name "*SunOS*" | xargs rm -rfv
find -type d -maxdepth 5 -name "*MacOSX*" | xargs rm -rfv
find -type d -maxdepth 5 -name "*Windows*" | xargs rm -rfv
find -type d -maxdepth 5 -name "*windows*" | xargs rm -rfv
find -type d -maxdepth 5 -name "*hpux*" | xargs rm -rfv
find -type d -maxdepth 5 -name "*solaris*" | xargs rm -rfv
# Worround
rm -r profiler/lib/deployed/

# delete redundant files:
find -type f -name ".lastModified" -print -delete
find -type f -name ".document" -print -delete

%ifnarch %{ix86}
rm -rv ide/bin/nativeexecution/Linux-x86
rm -rv cnd/bin/Linux-x86
rm -rv platform/modules/lib/i386
%endif
%ifnarch %{x8664}
rm -rv ide/bin/nativeexecution/Linux-x86_64
rm -rv cnd/bin/Linux-x86_64
rm -rv platform/modules/lib/amd64
%endif

# fix +x
chmod +x platform/modules/lib/*/linux/libjnidispatch-*.so

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name},%{_bindir},%{_desktopdir},%{_pixmapsdir},%{_appdir}}


# hardlink test
cp -l LICENSE.txt $RPM_BUILD_ROOT/cp-test && l=l && rm -f $RPM_BUILD_ROOT/cp-test
cp -a$l . $RPM_BUILD_ROOT%{_appdir}

# move conf file to etc
for a in $RPM_BUILD_ROOT%{_appdir}/etc/*; do
	f=${a##*/}
	mv $a $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
	ln -s %{_sysconfdir}/%{name}/$f $RPM_BUILD_ROOT%{_appdir}/etc
done

# install executable
ln -sf %{_appdir}/bin/netbeans $RPM_BUILD_ROOT%{_bindir}/netbeans

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop
cp -p nb/netbeans.png $RPM_BUILD_ROOT%{_pixmapsdir}/netbeans.png

# documenation
%{__rm} $RPM_BUILD_ROOT%{_appdir}/{README.html,CREDITS.html,LICENSE.txt,THIRDPARTYLICENSE.txt}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database

%postun
%update_desktop_database

%files
%defattr(644,root,root,755)
%doc README.html CREDITS.html LICENSE.txt THIRDPARTYLICENSE.txt
%defattr(-,root,root,755)
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/netbeans.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/netbeans.clusters
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/netbeans.import
%attr(755,root,root) %{_bindir}/netbeans
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/netbeans.png
%dir %{_appdir}
%{_appdir}/netbeans.css
%{_appdir}/bin
%{_appdir}/etc
%{_appdir}/harness
%{_appdir}/ide
%{_appdir}/nb
%{_appdir}/platform
%{_appdir}/extide

%files javase
%defattr(644,root,root,755)
%defattr(-,root,root,755)
%{_appdir}/apisupport
%{_appdir}/java
%{_appdir}/profiler

%files cpp
%defattr(644,root,root,755)
%defattr(-,root,root,755)
%{_appdir}/cnd
%{_appdir}/dlight

%files javacard
%defattr(644,root,root,755)
%defattr(-,root,root,755)
%{_appdir}/javacard

%files php
%defattr(644,root,root,755)
%defattr(-,root,root,755)
%{_appdir}/php

%files groovy
%defattr(644,root,root,755)
%defattr(-,root,root,755)
%{_appdir}/groovy

%files websvc
%defattr(644,root,root,755)
%defattr(-,root,root,755)
%{_appdir}/websvccommon
%{_appdir}/webcommon

%files mobile
%defattr(644,root,root,755)
%defattr(-,root,root,755)
%{_appdir}/mobility

%files java
%defattr(644,root,root,755)
%defattr(-,root,root,755)
%{_appdir}/enterprise
%{_appdir}/ergonomics

%files javafx
%defattr(644,root,root,755)
%defattr(-,root,root,755)
%{_appdir}/javafx
