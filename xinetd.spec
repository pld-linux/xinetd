#
# Conditional build:
%bcond_without	howl	# mdns/howl service registration support
#
Summary:	Xinetd - a powerful replacement for inetd
Summary(pl.UTF-8):	Xinetd - rozbudowany zamiennik inetd
Summary(pt_BR.UTF-8):	O xinetd é um substituto poderoso e seguro para o inetd
Summary(ru.UTF-8):	xinetd - богатая возможностями замена inetd
Summary(uk.UTF-8):	xinetd - багата можливостями заміна inetd
Name:		xinetd
Version:	2.3.14
Release:	2
License:	BSD-like
Group:		Daemons
Source0:	http://www.xinetd.org/%{name}-%{version}.tar.gz
# Source0-md5:	567382d7972613090215c6c54f9b82d9
Source1:	%{name}.inet.sh
Patch0:		%{name}-no_libnsl.patch
Patch1:		%{name}-tcp_rpc.patch
Patch2:		%{name}-howl.patch
Patch3:		%{name}-man.patch
URL:		http://www.xinetd.org/
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_howl:BuildRequires:	howl-devel >= 1.0.0-4}
BuildRequires:	libwrap-devel
%{?with_howl:BuildRequires:	pkgconfig}
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	rc-inetd
Requires:	rc-inetd
Provides:	inetdaemon
Obsoletes:	inetd
Obsoletes:	inetdaemon
Obsoletes:	netkit-base
Obsoletes:	rlinetd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing

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

%description -l pl.UTF-8
xinetd jest bezpieczniejszym i rozbudowanym odpowiednikiem inetd.
Niektóre funkcje to wbudowana kontrola dostępu (oparta o libwrap),
kontrola zużycia zasobów i wbudowana obsługa IPv6.

%description -l pt_BR.UTF-8
O xinetd é um substituto poderoso para o inetd.

Tem mecanismos de controle de acesso, capacidades extensivas de
registro de ocorrências, possibilita tornar serviços disponíveis de
acordo com horários e pode limitar o número de servidores que podem
ser iniciados, entre outras coisas.

Também possibilita redirecionar fluxos TCP para uma máquina e porta
remota. Isto é útil para aqueles que usam ip masquerading ou NAT e
querem poder acessar máquinas na rede interna.

Também possibilita associar serviços específicos a interfaces
específicas. Isto é útil quando você quer disponibilizar serviços para
sua rede interna, mas não para o resto do mundo. Ou ter um serviço
diferente rodando na mesma porta, mas em interfaces diferentes.

%description -l uk.UTF-8
xinetd - заміна inetd з багатими можливостями.

Серед іншого, xinetd має механізми управління доступом, багаті
можливості протоколювання, здатність регулювати доступність сервісів в
залежності від часу, може обмежувати кількість одночасно працюючих
серверів.

xinetd має можливість перенаправляти TCP потоки на інший хост та порт.
Це корисно для тих, хто використовує ip маскарадинг чи NAT та хоче
мати можливість доступу до внутрішніх хостів.

xinetd також має можливість прив'язувати конкретні сервіси до
конкретних інтерфейсів. Це корисно, коли ви хочете зробити сервіси
доступними лише для внутрішньої мережі, але не для решти Інтернету.
Або ж мати різні сервіси на тому ж номері порта, але різних
інтерфейсах.

%description -l ru.UTF-8
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
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__aclocal}
%{__autoconf}
cp -f /usr/share/automake/config.sub .
%configure \
	%{?with_howl:--with-howl} \
	--with-libwrap \
	--with-loadavg
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir} \
	$RPM_BUILD_ROOT%{_mandir}/man{5,8} \
	$RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

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
%service rc-inetd restart "xinetd"

%preun
if [ "$1" = "0" ]; then
	%service rc-inetd stop
fi

%files
%defattr(644,root,root,755)
%doc README CHANGELOG sample.conf xconv.pl
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) %ghost %{_sysconfdir}/xinetd.conf
%attr(640,root,root) /etc/sysconfig/rc-inet.script
%{_mandir}/man[158]/*
