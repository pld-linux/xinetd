Summary:	Secure replacement for inetd
Summary(pl):	Bezpieczny odpowiednik inetd
Name:		xinetd
Version:	2.1.8.9pre13
Release:	6
Group:		Daemons
Group(de):	Server
Group(pl):	Serwery
License:	Distributable (BSD-like)
Source0:	http://www.xinetd.org/%{name}-%{version}.tar.gz
Source1:	%{name}.inet.sh
URL:		http://www.xinetd.org/
BuildRequires:	libwrap-devel
Requires:	rc-inetd
Prereq:		rc-scripts
Requires:	/etc/rc.d/init.d/rc-inetd
Provides:	inetdaemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	inetdaemon
Obsoletes:	inetd
Obsoletes:	rlinetd
Obsoletes:	netkit-base

%define         _sysconfdir     /etc

%description
Xinetd is a secure replacement for inetd, the Internet services
daemon. Xinetd provides access control for all services based on the
address of the remote host and/or on time of access and can prevent
denial-of-access attacks. Xinetd provides extensive logging, has no
limit on the number of server arguments and you can bind specific
services to specific IP addresses on your host machine.

%description -l pl
xinetd jest bezpieczniejszym i rozbudowanym odpowiednikiem inetd.
Niektóre funkcje to wbudowana kontrola dostêpu (oparta o libwrap),
kontrola zu¿ycia zasobów i wbudowana obs³uga IPv6.

%prep
%setup -q

%build
%configure  \
	--with-libwrap \
	--with-inet6 \
	--with-loadavg
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{_sbindir} \
	$RPM_BUILD_ROOT/%{_mandir}/man{5,8} \
	$RPM_BUILD_ROOT/%{_sysconfdir}/{rc.d/init.d,sysconfig}

install xinetd/xinetd $RPM_BUILD_ROOT/%{_sbindir}
install xinetd/itox $RPM_BUILD_ROOT/%{_sbindir}
install xinetd/xinetd.conf.man $RPM_BUILD_ROOT/%{_mandir}/man5/xinetd.conf.5
install xinetd/xinetd.log.man $RPM_BUILD_ROOT/%{_mandir}/man8/xinetd.log.8
install xinetd/xinetd.man $RPM_BUILD_ROOT/%{_mandir}/man8/xinetd.8
install xinetd/itox.8 $RPM_BUILD_ROOT/%{_mandir}/man8/itox.8
install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inet.script
:> $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.conf

cp xinetd/sample.conf .
cp xinetd/xconv.pl .

gzip -9nf README CHANGELOG sample.conf xconv.pl

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/rc-inetd ]; then
        /etc/rc.d/init.d/rc-inetd restart 1>&2
else
        echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start xinetd" 1>&2
fi

%preun
if [ "$1" = "0" -a -f /var/lock/subsys/rc-inetd ]; then
        /etc/rc.d/init.d/rc-inetd stop
fi

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) %ghost %{_sysconfdir}/xinetd.conf
%attr(640,root,root) /etc/sysconfig/rc-inet.script
%{_mandir}/man[158]/*
