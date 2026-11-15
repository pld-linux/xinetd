Summary:	Xinetd - a powerful replacement for inetd
Summary(pl.UTF-8):	Xinetd - rozbudowany zamiennik inetd
Summary(pt_BR.UTF-8):	O xinetd é um substituto poderoso e seguro para o inetd
Summary(ru.UTF-8):	xinetd - богатая возможностями замена inetd
Summary(uk.UTF-8):	xinetd - багата можливостями заміна inetd
Name:		xinetd
Version:	2.3.15.4
Release:	2
License:	BSD-like
Group:		Networking/Daemons
Source0:	https://github.com/openSUSE/xinetd/releases/download/%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	cbdb8e10a7ccb047c08ac1922e670318
Source1:	%{name}.inet.sh
# https://github.com/openSUSE/xinetd/commit/e95de5911c230236b51de59bd1df3f0adcc0b961
Patch0:		%{name}-cps-instances-limit.patch
URL:		https://github.com/openSUSE/xinetd/
BuildRequires:	libselinux-devel
BuildRequires:	libtirpc-devel
BuildRequires:	libwrap-devel
BuildRequires:	pkgconfig
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
%patch -P0 -p1

%build
# empty parameter lists mean (void) since C23, which gcc 15 defaults to
%configure \
	CFLAGS="%{rpmcflags} -std=gnu17" \
	--disable-silent-rules \
	--with-labeled-networking \
	--with-libwrap \
	--with-loadavg \
	--with-rpc
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/sysconfig

# rc-inetd regenerates %{_sysconfdir}/xinetd.conf on every start, so upstream's
# xinetd.conf and xinetd.d/ would only be dead files here
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	sysconf_DATA= \
	xinetconf_DATA=

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inet.script
:> $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.conf

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
%doc CHANGELOG COPYRIGHT README.md contrib/xinetd.conf
%attr(755,root,root) %{_bindir}/itox
%attr(755,root,root) %{_bindir}/xconv.pl
%attr(755,root,root) %{_sbindir}/xinetd
%attr(640,root,root) %ghost %{_sysconfdir}/xinetd.conf
%attr(640,root,root) /etc/sysconfig/rc-inet.script
%{_mandir}/man5/xinetd.conf.5*
%{_mandir}/man5/xinetd.log.5*
%{_mandir}/man8/itox.8*
%{_mandir}/man8/xconv.pl.8*
%{_mandir}/man8/xinetd.8*
