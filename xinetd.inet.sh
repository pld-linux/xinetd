# proces name
PROCESS_NAME=xinetd

# inet server config
CONFIG_FILE=/etc/xinetd.conf
CONFIG_FILE_UMASK=027

# inet server daemon executable file name
INETDAEMON=/usr/sbin/xinetd

# addytional inet server daemon argumments
INETDAEMON_ARGS=

PREAMBLE="# This file is autogenerated!"

parse_one_service()
{
	ERROR_CODE=0

	[ "${SERVICE_NAME:-not}" = "not" ]	&& ERROR_CODE=11
	[ "${PROTOCOL:-not}" = "not" ]		&& ERROR_CODE=12
	[ "${PORT:-not}" = "not" ]		&& ERROR_CODE=13
	[ "${USER:-not}" = "not" ]		&& ERROR_CODE=14
	[ "${SERVER:-not}" = "not" ]		&& ERROR_CODE=15
	[ "${FLAGS:-not}" = "not" ]		&& ERROR_CODE=16
	[ "${DAEMON:-not}" = "not" ]		&& ERROR_CODE=17
	[ "${SOCK_TYPE:-not}" = "not" ]		&& ERROR_CODE=18

	if [ ! $ERROR_CODE -eq 0 ] ; then
		echo "ERROR: Parse error."
		case "$ERROR_CODE" in
			11)
				echo "SERVICE_NAME not defined in /etc/sysconfig/rc-inetd/$CURRENT_SERVICE."
				;;
			12)
				echo "PROTOCOL not defined in /etc/sysconfig/rc-inetd/$CURRENT_SERVICE."
				;;
			13)
				echo "PORT not defined in /etc/sysconfig/rc-inetd/$CURRENT_SERVICE."
				;;
			14)
				echo "USER not defined in /etc/sysconfig/rc-inetd/$CURRENT_SERVICE."
				;;
			15)
				echo "SERVER not defined in /etc/sysconfig/rc-inetd/$CURRENT_SERVICE."
				;;
			16)
				echo "FLAGS not defined in /etc/sysconfig/rc-inetd/$CURRENT_SERVICE."
				;;
			17)
				echo "DAEMON not defined in /etc/sysconfig/rc-inetd/$CURRENT_SERVICE."
				;;
			18)
				echo "SOCK_TYPE not defined in /etc/sysconfig/rc-inetd/$CURRENT_SERVICE."
				;;
		esac
		return $ERROR_CODE
	fi

	echo "service $SERVICE_NAME"
	echo "{"
	if [ "${SERVICE_TYPE:-n}" != "n" ]; then
		for i in $SERVICE_TYPE ; do
			if [ "$i" = "RPC" ] ; then
				[ "${RPCVERSION:-n}" = "n" ] || echo "	rpc_version	= $RPCVERSION"
				[ "${RPCNUMBER:-n}" = "n" ] || echo "	rpc_number	= $RPCNUMBER"
			fi
			XSERVICE_TYPE="$XSERVICE_TYPE $i"
		done
	fi
	[ "${XSERVICE_TYPE:-n}" = "n" ] || echo "	type		=$XSERVICE_TYPE"
	echo "	socket_type	= $SOCK_TYPE"
	echo "	protocol	= $PROTOCOL"
	echo "	port		= $PORT"
	echo "	user		= $USER"
	[ "${GROUP:-n}" = "n" ] || echo "	group		= $GROUP"
        if [ "$SERVER" = "tcpd" ] ; then
		SERVER="$DAEMON"
        else
                DAEMONARGS="$DAEMON $DAEMONARGS"
                XFLAGS="$XFLAGS NAMEINARGS "
        fi
	echo "	server		= $SERVER"

	[ "${DAEMONARGS:-n}" = "n" ] || echo "	server_args	= $DAEMONARGS"

	for i in $FLAGS ; do
		if [ "$i" = "wait" ]; then
			echo "	wait		= yes"
		elif [ "$i" = "nowait" ]; then
			echo "	wait		= no"
			[ "${MAX_CONNECTIONS:-n}" = "n" ] || echo "	instances	= $MAX_CONNECTIONS"
			[ "${MAX_CONNECTIONS_PER_SOURCE:-n}" = "n" ] || echo "	per_source	= $MAX_CONNECTIONS_PER_SOURCE"
		else
			XFLAGS="$XFLAGS $i"
		fi
	done
	[ "${XFLAGS:-n}" = "n" ]	|| echo "	flags		=$XFLAGS"

	[ "${INTERFACE:-n}" = "n" ]	|| echo "	bind		= $INTERFACE"
	[ "${NICE:-n}" = "n" ]		|| echo "	nice		= $NICE"
	[ "${INITGROUPS:-n}" = "n" ]	|| echo "	groups		= $INITGROUPS"
	[ "${LOG_TYPE:-n}" = "n" ]	|| echo "	log_type	= $LOG_TYPE"
	[ "${LOG_SUCCESS:-n}" = "n" ]	|| echo "	log_on_success	= $LOG_SUCCESS"
	[ "${LOG_FAILURE:-n}" = "n" ]	|| echo "	log_on_failure	= $LOG_FAILURE"
	[ "${ENV:-n}" = "n" ]		|| echo "	env		= $ENV"
	[ "${PASSENV:-n}" = "n" ]	|| echo "	passenv		= $PASSENV"
	[ "${MAX_LOAD:-n}" = "n" ]	|| echo "	max_load	= $MAX_LOAD"
	[ "${ACCESS_TIMES:-n}" = "n" ]	|| echo "	access_times	= $ACCESS_TIMES"
	[ "${REDIRECT:-n}" = "n" ]	|| echo "	redirect	= $REDIRECT"
	[ "${BANNER:-n}" = "n" ]	|| echo "	banner		= $BANNER"
	[ "${BANNER_SUCCESS:-n}" = "n" ]	|| echo "	banner_success	= $BANNER_SUCCESS"
	[ "${BANNER_FAILURE:-n}" = "n" ]	|| echo "	banner_fail	= $BANNER_FAILURE"
	[ "${CONNECTIONS_PER_SECOND:-n}" = "n" ]	|| echo "	cps		= $CONNECTIONS_PER_SECOND"
	echo "}"

	unset i XFLAGS XSERVICE_TYPE
	return 0
}

status_rc_inetd()
{
	status $INETDAEMON
}

reload_config()
{
	killall -USR1 $INETDAEMON
}
