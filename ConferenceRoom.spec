Summary:	ConferenceRoom IRC Server
Summary(pl.UTF-8):	ConferenceRoom - serwer IRC
Name:		ConferenceRoom
Version:	1.8.9.1
Release:	0.22
License:	not distributable
Group:		Applications/Communications
Source0:	CR%{version}-Linux.tar.gz
# NoSource0-md5:	ee92ada3f47d6da20f4855c1d5710e92
NoSource:	0
Source1:	CR-help.tar.bz2
# NoSource1-md5:	2b88e7639c2d13b9d23efbb683cf2213
NoSource:	1
Source2:	ConfRoom.conf
Source3:	cr.init
URL:		http://www.conferenceroom.com/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	rc-scripts >= 0.4.1.26
Provides:	group(ircd)
Provides:	user(ircd)
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# already stripped
%define		no_install_post_strip		1
%define		no_install_post_chrpath		1
%define		_enable_debug_packages		0

%description
ConferenceRoom is an IRC Daemon.

%description -l pl.UTF-8
ConferenceRoom to serwer IRC-a.

%package web
Summary:	ConferenceRoom Web components
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}

%description web
ConferenceRoom Web components

%prep
%setup -q -n CR%{version}-Linux -a1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_datadir}/cr,%{_libdir}/cr/programs,/var/lib/cr/db,/var/log/cr}
cp -a programs/* $RPM_BUILD_ROOT%{_libdir}/cr/programs
cp -a help $RPM_BUILD_ROOT%{_datadir}/cr
ln -s %{_datadir}/cr/help $RPM_BUILD_ROOT/var/lib/cr/help
cp -a htdocs template variables $RPM_BUILD_ROOT%{_datadir}/cr
cp -a mime.types $RPM_BUILD_ROOT%{_datadir}/cr

cp -p db/ConfRoom.base $RPM_BUILD_ROOT%{_sysconfdir}/ConfRoom.conf
cat %{SOURCE2} >> $RPM_BUILD_ROOT%{_sysconfdir}/ConfRoom.conf
ln -s %{_sysconfdir}/ConfRoom.conf $RPM_BUILD_ROOT/var/lib/cr/ConfRoom.conf

ln -s %{_libdir}/cr/programs $RPM_BUILD_ROOT/var/lib/cr
ln -s /var/log/cr $RPM_BUILD_ROOT/var/lib/cr/db/logs
ln -s /var/log/cr/craccess.log $RPM_BUILD_ROOT/var/lib/cr/db/craccess.log
install -D %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/cr

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 75 ircd
%useradd -u 75 -d /var/lib/cr -g ircd -c "ConferenceRoom IRCD" ircd

%post
/sbin/chkconfig --add cr
for a in craccess.log chan.log nick.log services.log; do
	if [ ! -f /var/log/cr/$a ]; then
		touch /var/log/cr/$a
		chown ircd:ircd /var/log/cr/$a
	fi
done

%preun
if [ "$1" = "0" ]; then
	%service -q cr stop
	/sbin/chkconfig --del cr
fi

%postun
if [ "$1" = "0" ]; then
	%userremove ircd
	%groupremove ircd
fi

%files
%defattr(644,root,root,755)
%doc LICENSE.TXT PLATFORM README RELEASE
%attr(660,root,ircd) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ConfRoom.conf
%attr(754,root,root) /etc/rc.d/init.d/cr
%dir %{_libdir}/cr
%dir %{_libdir}/cr/programs
%attr(755,root,root) %{_libdir}/cr/programs/*
%dir %{_datadir}/cr
%{_datadir}/cr/help
%dir %attr(775,root,ircd) /var/lib/cr
%dir %attr(770,root,ircd) /var/lib/cr/db
/var/lib/cr/ConfRoom.conf
/var/lib/cr/db/craccess.log
/var/lib/cr/db/logs
/var/lib/cr/help
/var/lib/cr/programs
%dir /var/log/cr

%files web
%defattr(644,root,root,755)
%{_datadir}/cr/mime.types
%{_datadir}/cr/htdocs
%{_datadir}/cr/template
%{_datadir}/cr/variables
