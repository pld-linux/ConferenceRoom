Summary:	ConferenceRoom IRC Server
Summary(pl.UTF-8):	ConferenceRoom - serwer IRC
Name:		ConferenceRoom
Version:	1.8.9.1
Release:	0.11
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

install -d $RPM_BUILD_ROOT{%{_datadir}/cr,%{_libdir}/cr/programs,/var/lib/cr/db,/var/log/cr}
cp -a programs/* $RPM_BUILD_ROOT%{_libdir}/cr/programs
cp -a htdocs template variables $RPM_BUILD_ROOT%{_datadir}/cr
cp -a mime.types $RPM_BUILD_ROOT%{_datadir}/cr
cp -a db/ConfRoom.base $RPM_BUILD_ROOT/var/lib/cr/ConfRoom.conf
cat %{SOURCE1} >> $RPM_BUILD_ROOT/var/lib/cr/ConfRoom.conf
ln -s %{_libdir}/cr/programs $RPM_BUILD_ROOT/var/lib/cr
ln -s /var/log/cr $RPM_BUILD_ROOT/var/lib/cr/db/logs
ln -s /var/log/cr/craccess.log $RPM_BUILD_ROOT/var/lib/cr/db/craccess.log

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 75 ircd
%useradd -u 75 -d /var/lib/cr -g ircd -c "ConferenceRoom IRCD" ircd

%post
for a in craccess.log chan.log nick.log services.log; do
	if [ ! -f /var/log/cr/$a ]; then
		touch /var/log/cr/$a
		chown ircd:ircd /var/log/cr/$a
	fi
done

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
%{_datadir}/cr
%dir /var/lib/cr
%config(noreplace) %verify(not md5 mtime size) /var/lib/cr/*.conf
%dir /var/lib/cr/db
/var/lib/cr/db/craccess.log
/var/lib/cr/db/logs
/var/lib/cr/programs
%dir /var/log/cr
