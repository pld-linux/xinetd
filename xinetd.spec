Summary:	Xinetd - a powerful replacement for inetd
Summary(pl):	Xinetd - rozbudowany zamiennik inetd
Summary(pt_BR):	O xinetd � um substituto poderoso e seguro para o inetd
Summary(ru):	xinetd - ������� ������������� ������ inetd
Summary(uk):	xinetd - ������ ������������ ��ͦ�� inetd
Name:		xinetd
Version:	2.3.13
Release:	2
Group:		Daemons
License:	BSD-like
Source0:	http://www.xinetd.org/%{name}-%{version}.tar.gz
# Source0-md5:	4295b5fe12350f09b5892b363348ac8b
Source1:	%{name}.inet.sh
Patch0:		%{name}-no_libnsl.patch
URL:		http://www.xinetd.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libwrap-devel
PreReq:		rc-inetd
Provides:	inetdaemon
Obsoletes:	inetdaemon
Obsoletes:	inetd
Obsoletes:	rlinetd
Obsoletes:	netkit-base
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
xinetd is a powerful replacement for inetd. xinetd has access control
machanisms, extensive logging capabilities, the ability to make
services available based on time, and can place limits on the number
of servers that can be started, among other things.

xinetd has the ability to redirect TCP streams to a remote host and
port. This is useful for those of that use ip masquerading, or NAT,
and want to be able to reach your internal hosts.

xinetd also has the ability to bind specific services to specific
interfaces. This is useful when you want to make services available
for your internal network, but not the rest of the world. Or to have a
different service running on the same port, but different interfaces.

%description -l pl
xinetd jest bezpieczniejszym i rozbudowanym odpowiednikiem inetd.
Niekt�re funkcje to wbudowana kontrola dost�pu (oparta o libwrap),
kontrola zu�ycia zasob�w i wbudowana obs�uga IPv6.

%description -l pt_BR
O xinetd � um substituto poderoso para o inetd.

Tem mecanismos de controle de acesso, capacidades extensivas de
registro de ocorr�ncias, possibilita tornar servi�os dispon�veis de
acordo com hor�rios e pode limitar o n�mero de servidores que podem
ser iniciados, entre outras coisas.

Tamb�m possibilita redirecionar fluxos TCP para uma m�quina e porta
remota. Isto � �til para aqueles que usam ip masquerading ou NAT e
querem poder acessar m�quinas na rede interna.

Tamb�m possibilita associar servi�os espec�ficos a interfaces
espec�ficas. Isto � �til quando voc� quer disponibilizar servi�os para
sua rede interna, mas n�o para o resto do mundo. Ou ter um servi�o
diferente rodando na mesma porta, mas em interfaces diferentes.

%description -l uk
xinetd - ��ͦ�� inetd � �������� ������������.

����� ������, xinetd ��� ����Φ��� �����̦��� ��������, ����Ԧ
��������Ԧ ��������������, ����Φ��� ���������� ������Φ��� ���צӦ� �
��������Ԧ צ� ����, ���� ���������� ˦��˦��� ��������� ���������
�����Ҧ�.

xinetd ��� �����צ��� �������������� TCP ������ �� ����� ���� �� ����.
�� ������� ��� ���, ��� ����������դ ip ����������� �� NAT �� ����
���� �����צ��� ������� �� ����Ҧ�Φ� ���Ԧ�.

xinetd ����� ��� �����צ��� ����'������� �������Φ ���צ�� ��
���������� ��������Ӧ�. �� �������, ���� �� ������ ������� ���צ��
���������� ���� ��� ����Ҧ���ϧ ����֦, ��� �� ��� ����� ���������.
��� � ���� Ҧ�Φ ���צ�� �� ���� � ����Ҧ �����, ��� Ҧ����
�����������.

%description -l ru
xinetd - ������ inetd � �������� �������������.

����� �������, xinetd ����� ��������� ���������� ��������, �������
����������� ����������������, ����������� ������������ �����������
�������� � ����������� �� �������, ����� ������������ ����������
������������ ���������� ��������.

xinetd ����� ����������� �������������� TCP ������ �� ������ ���� �
����. ��� ������� ��� ���, ��� ���������� ip ����������� ��� NAT �
����� ����� ����������� ������� � ���������� ������.

xinetd ����� ����� ����������� ����������� ���������� ������� �
���������� �����������. ��� �������, ���� �� ������ ������� �������
���������� ������ ��� ���������� ����, �� �� ��� ���������� ���������.
��� �� ����� ������ ������� �� ��� �� ������ �����, �� ������
�����������.

%prep
%setup -q
%patch0 -p1

%build
%{__aclocal}
%{__autoconf}
cp -f /usr/share/automake/config.sub .
%configure  \
	--with-libwrap \
	--with-loadavg
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir} \
	$RPM_BUILD_ROOT%{_mandir}/man{5,8} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{rc.d/init.d,sysconfig}

install xinetd/xinetd $RPM_BUILD_ROOT%{_sbindir}
install xinetd/itox $RPM_BUILD_ROOT%{_sbindir}
install xinetd/xinetd.conf.man $RPM_BUILD_ROOT%{_mandir}/man5/xinetd.conf.5
install xinetd/xinetd.log.man $RPM_BUILD_ROOT%{_mandir}/man8/xinetd.log.8
install xinetd/xinetd.man $RPM_BUILD_ROOT%{_mandir}/man8/xinetd.8
install xinetd/itox.8 $RPM_BUILD_ROOT%{_mandir}/man8/itox.8
install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inet.script
:> $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.conf

cp xinetd/sample.conf .
cp xinetd/xconv.pl .

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
%doc README CHANGELOG sample.conf xconv.pl
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) %ghost %{_sysconfdir}/xinetd.conf
%attr(640,root,root) /etc/sysconfig/rc-inet.script
%{_mandir}/man[158]/*
