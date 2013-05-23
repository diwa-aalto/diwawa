#!/bin/sh

RETVAL=0
QPKG_NAME="Optware"

_exit()
{
    /bin/echo -e "Error: $*"
    /bin/echo
    exit 1
}

# Determine BASE installation location according to smb.conf
BASE=
publicdir=`/sbin/getcfg Public path -f /etc/config/smb.conf`
if [ ! -z $publicdir ] && [ -d $publicdir ];then
	publicdirp1=`/bin/echo $publicdir | /bin/cut -d "/" -f 2`
	publicdirp2=`/bin/echo $publicdir | /bin/cut -d "/" -f 3`
	publicdirp3=`/bin/echo $publicdir | /bin/cut -d "/" -f 4`
	if [ ! -z $publicdirp1 ] && [ ! -z $publicdirp2 ] && [ ! -z $publicdirp3 ]; then
		[ -d "/${publicdirp1}/${publicdirp2}/Public" ] && BASE="/${publicdirp1}/${publicdirp2}"
	fi
fi

# Determine BASE installation location by checking where the Public folder is.
if [ -z $BASE ]; then
	for datadirtest in /share/HDA_DATA /share/HDB_DATA /share/HDC_DATA /share/HDD_DATA /share/MD0_DATA; do
		[ -d $datadirtest/Public ] && BASE="$datadirtest"
	done
fi
if [ -z $BASE ] ; then
	echo "The Public share not found."
	_exit 1
fi
QPKG_DIR=${BASE}/.qpkg/Optware

case "$1" in
  start)
  if [ `/sbin/getcfg ${QPKG_NAME} Enable -u -d FALSE -f /etc/config/qpkg.conf` = UNKNOWN ]; then
  	/sbin/setcfg ${QPKG_NAME} Enable TRUE -f /etc/config/qpkg.conf
  elif [ `/sbin/getcfg ${QPKG_NAME} Enable -u -d FALSE -f /etc/config/qpkg.conf` != TRUE ]; then
  	_exit  "${QPKG_NAME} is disabled."
  fi

  /bin/echo "Enable Optware/ipkg"
	# sym-link $QPKG_DIR to /opt
	/bin/rm -rf /opt
	/bin/ln -sf $QPKG_DIR /opt
        #sym-link the html dir
	/bin/ln -sf $QPKG_DIR/html /home/httpd/
	#sym-link the management website to /(Q)Web
	[ -d /share/Web ] && WebDir="/share/Web"
        [ -d /share/Qweb ] && WebDir="/share/Qweb" 
	[ -d $WebDir/Optware ] || /bin/ln -sf /home/httpd/html/Management $WebDir/Optware
	        	
	# adding Ipkg apps into system path ...
	/bin/cat /etc/profile | /bin/grep "PATH" | /bin/grep "/opt/bin" 1>>/dev/null 2>>/dev/null
	#[ $? -ne 0 ] && /bin/echo "export PATH=\$PATH":/opt/bin:/opt/sbin >> /etc/profile
 	[ $? -ne 0 ] && /bin/echo "export PATH=/opt/bin:/opt/sbin:\$PATH" >> /etc/profile
	
	# Patch per http://wiki.qnap.com/wiki/Install_Optware_IPKG
  	/bin/echo "Run Optware/ipkg /opt/etc/init.d/*"
  	source /etc/profile
        # Start all init scripts in /opt/etc/init.d
	# executing them in numerical order.
	#
	for i in /opt/etc/init.d/S??* ;do
	    # Ignore dangling symlinks (if any).
    	    #[ ! -f "$i" ] && continue

            case "$i" in
                *.sh)
	            # Source shell script for speed.
	            (
		        trap - INT QUIT TSTP
			set start
		        . $i
	    	    )
	        ;;
	        *)
	    	    # No sh extension, so fork subprocess.
	    	    $i start
                ;;          
            esac            
        done                
	# End patch
	# determine the right feed based on cpu type
        arch=$(/bin/uname -m)
        case "$(/bin/uname -m)" in
        armv5tejl)
          #X09 architecture
          kmod_feed="http://ipkg.nslu2-linux.org/feeds/optware/tsx09/cross/unstable"
          modelrange="tsx09"
        ;;
        armv5tel)
          #X19 architecture
          kmod_feed="http://ipkg.nslu2-linux.org/feeds/optware/tsx19/cross/unstable"
          modelrange="tsx19"
        ;;
        x86_64)
          #x86 architecture
          kmod_feed=""
          modelrange="ts509"
	;;
        i686)
          #x86 architecture
          kmod_feed=""
          modelrange="ts509"
        ;;
        *)
         #everyting else
         _exit "Unknown CPU architecture, quitting Optware start"
       ;;
       esac

       [ -z $kmod_feed ] || /bin/echo "src $modelrange $kmod_feed" > /opt/etc/ipkg/$modelrange-kmod.conf
       [ -z $kmod_feed ] || /usr/bin/wget -q $kmod_feed/Packages --spider || /bin/rm -rf /opt/etc/ipkg/$modelrange-kmod.conf
 
       ;;
  stop)
  	/bin/echo "Disable Optware/ipkg"
	export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin

	[ -d /share/Web ] && WebDir="/share/Web"
        [ -d /share/Qweb ] && WebDir="/share/Qweb"
        /bin/rm -f $WebDir/Optware

	/bin/sync
	/bin/sleep 1
	;;
  restart)
	$0 stop
	$0 start
	;;
  *)
	echo "Usage: $0 {start|stop|restart}"
	exit 1
esac

exit $RETVAL

