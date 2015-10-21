#!/bin/bash
set -ef
domain="`cat domain.cfg`"
sh stop_fcgi.sh $domain
sh install_fcgi.sh $domain 
sh start_fcgi.sh $domain 
echo "done"
