Summary:	Xinetd - a powerful replacement for inetd
Summary(pl):	Xinetd - rozbudowany zamiennik inetd
Summary(pt_BR):	O xinetd И um substituto poderoso e seguro para o inetd
Summary(ru):	xinetd - богатая возможностями замена inetd
Summary(uk):	xinetd - багата можливостями зам╕на inetd
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
NiektСre funkcje to wbudowana kontrola dostЙpu (oparta o libwrap),
kontrola zu©ycia zasobСw i wbudowana obsЁuga IPv6.

%description -l pt_BR
O xinetd И um substituto poderoso para o inetd.

Tem mecanismos de controle de acesso, capacidades extensivas de
registro de ocorrЙncias, possibilita tornar serviГos disponМveis de
acordo com horАrios e pode limitar o nЗmero de servidores que podem
ser iniciados, entre outras coisas.

TambИm possibilita redirecionar fluxos TCP para uma mАquina e porta
remota. Isto И Зtil para aqueles que usam ip masquerading ou NAT e
querem poder acessar mАquinas na rede interna.

TambИm possibilita associar serviГos especМficos a interfaces
especМficas. Isto И Зtil quando vocЙ quer disponibilizar serviГos para
sua rede interna, mas nЦo para o resto do mundo. Ou ter um serviГo
diferente rodando na mesma porta, mas em interfaces diferentes.

%description -l uk
xinetd - зам╕на inetd з багатими можливостями.

Серед ╕ншого, xinetd ма╓ механ╕зми управл╕ння доступом, багат╕
можливост╕ протоколювання, здатн╕сть регулювати доступн╕сть серв╕с╕в в
залежност╕ в╕д часу, може обмежувати к╕льк╕сть одночасно працюючих
сервер╕в.

xinetd ма╓ можлив╕сть перенаправляти TCP потоки на ╕нший хост та порт.
Це корисно для тих, хто використову╓ ip маскарадинг чи NAT та хоче
мати можлив╕сть доступу до внутр╕шн╕х хост╕в.

xinetd також ма╓ можлив╕сть прив'язувати конкретн╕ серв╕си до
конкретних ╕нтерфейс╕в. Це корисно, коли ви хочете зробити серв╕си
доступними лише для внутр╕шньо╖ мереж╕, але не для решти ╤нтернету.
Або ж мати р╕зн╕ серв╕си на тому ж номер╕ порта, але р╕зних
╕нтерфейсах.

%description -l ru
xinetd - замена inetd с богатыми возможностями.

Среди прочего, xinetd имеет механизмы управления доступом, богатые
возможности протоколирования, способность регулировать доступность
сервисов в зависимости от времени, может ограничивать количество
одновременно работающих серверов.

xinetd имеет возможность перенаправлять TCP потоки на другой хост и
порт. Это полезно для тех, кто использует ip маскарадинг или NAT и
хочет иметь возможность доступа к внутренним хостам.

xinetd также имеет возможность привязывать конкретные сервисы к
конкретным интерфейсам. Это полезно, если вы хотите сделать сервисы
доступными только для внутренней сети, но не для остального Интернета.
Или же иметь разные сервисы на том же номере порта, но разных
интерфейсах.

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
