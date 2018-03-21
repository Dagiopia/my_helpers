#!/bin/bash 
# add ips with more than 5 trials to an ipset of the firewall for punishment
# Dagim Sisay <email@dagiopia.net>
# February, 2018

SETNAME="metfo_ipwoch"

# if ipset doesn't exist, create it
ipset list $SETNAME
if [ $? -ne 0 ] ; then
    ipset create $SETNAME iphash
fi

declare -a ARR
ARR=($( grep "Failed password for root" /var/log/auth.log | grep -Po '(?<=from ).*(?= port)' | uniq -c | sort -nr -k1 | sort -u -k2 | sort -nr -k1))
#N=0
#while [ "x${ARR[@]}" != "x" ] ; do N=$(( $N+1 )) ; done
ADD=0
for i in ${ARR[@]} ; do 
	if [ 0 == $ADD ] && [ 5 -le $i ] ; then
		ADD=1
	elif [ $ADD == 1 ] ; then
		ipset add $SETNAME $i 
		ADD=0
	fi

done

ipset save $SETNAME -f /etc/ipset.conf
