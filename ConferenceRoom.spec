Summary:	ConferenceRoom IRC Server
Summary(pl.UTF-8):	ConferenceRoom - serwer IRC
Name:		ConferenceRoom
Version:	1.8.9.1
Release:	0.10
License:	not distributable
Group:		Applications/Communications
Source0:	CR%{version}-Linux.tar.gz
# NoSource0-md5:	ee92ada3f47d6da20f4855c1d5710e92
NoSource:	0
Source1:	ConfRoom.conf
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

%define		_sysconfdir	/etc/cr

# already stripped
%define		no_install_post_strip		1
%define		no_install_post_chrpath		1

%description
ConferenceRoom is an IRC Daemon.

%description -l pl.UTF-8
ConferenceRoom to serwer IRC-a.

%prep
%setup -q -n CR%{version}-Linux

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_datadir}/cr,%{_sysconfdir},%{_libdir}/cr/programs,/var/{lib,log}/cr}
cp -a programs/* $RPM_BUILD_ROOT%{_libdir}/cr/programs
cp -a htdocs template variables $RPM_BUILD_ROOT%{_datadir}/cr
cp -a mime.types $RPM_BUILD_ROOT%{_datadir}/cr
cp -a db/ConfRoom.base $RPM_BUILD_ROOT%{_sysconfdir}/ConfRoom.conf
cat %{SOURCE1} >> $RPM_BUILD_ROOT%{_sysconfdir}/ConfRoom.conf
ln -s %{_sysconfdir}/ConfRoom.conf $RPM_BUILD_ROOT%{_libdir}/cr

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
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.conf
%dir %{_libdir}
%attr(755,root,root) %{_libdir}/*
%{_datadir}/cr
/var/lib/cr
/var/log/cr
