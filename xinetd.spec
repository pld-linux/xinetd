# $Revision: 1.1 $
Summary:	Secure replacement for inetd
Summary(pl):	Bezpieczny odpowiednik inetd
Name:		xinetd
Version:	2.1.8.8p3
Release:	1
Group:		Daemons
Group(pl):	Serwery
License:	GPL
Source0:	http://www.xinetd.org/%{name}-%{version}.tar.gz
URL:		http://www.xinetd.org/
Requires:	rc-scripts
BuildRequires:	libcap-devel
BuildRequires:	libwrap-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	inetdaemon
Obsoletes:	inetd
Obsoletes:	netkit-base

%define         _sysconfdir     /etc

%description
xinetd  is  a  secure and enhances replacement for inetd. Some features
include built-in, libwrap based access control, resource control
and native IPv6 support.

%description -l pl
xinetd jest bezpieczniejszym i rozbudowanym odpowiednikiem inetd. Niektóre
funkcje to wbudowana kontrola dostêpu (oparta o libwrap), kontrola zu¿ycia
zasobów i wbudowana obs³uga IPv6.

%prep
%setup -q

%build
LDFLAGS="-s"; export LDFLAGS
%configure \
	--with-libwrap \
	--with-inet6 \
	--with-loadavg
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR="$RPM_BUILD_ROOT"

:> $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.conf

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man{1,5,8}/* README CHANGELOG

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_sbindir}/xinetd
%{_mandir}/man[158]/*
