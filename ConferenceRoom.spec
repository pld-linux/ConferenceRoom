Summary:	ConferenceRoom IRC Server
Name:		ConferenceRoom
Version:	1.8.9.1
Release:	0.1
License:	not distributable
Group:		Applications/Communications
Source0:	CR%{version}-Linux.tar.gz
# NoSource0-md5:	ee92ada3f47d6da20f4855c1d5710e92
NoSource:	0
URL:		http://www.conferenceroom.com/
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Provides:	group(ircd)
Provides:	user(ircd)
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# already stripped
%define		no_install_post_strip		1
%define		no_install_post_chrpath		1

%description
ConferenceRoom is an IRC Daemon.

%prep
%setup -q -n CR%{version}-Linux

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_datadir},%{_libdir},/var/{lib,log}}/%{name}
cp -a programs/* $RPM_BUILD_ROOT%{_libdir}/%{name}
cp -a db/*.base $RPM_BUILD_ROOT/var/lib/%{name}
cp -a htdocs template variables $RPM_BUILD_ROOT%{_datadir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 75 ircd
%useradd -u 75 -d %{_datadir} -g ircd -c "ConferenceRoom IRCD" ircd

%postun
if [ "$1" = "0" ]; then
	%userremove ircd
	%groupremove ircd
fi

%files
%defattr(644,root,root,755)
%doc LICENSE.TXT PLATFORM README RELEASE
%dir %{_libdir}
%attr(755,root,root) %{_libdir}/*
%{_datadir}/%{name}
/var/lib/cr
/var/log/cr
