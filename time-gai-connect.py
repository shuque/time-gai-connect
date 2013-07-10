#!/usr/bin/env python
#
# time-gai-connect: measures TCP connection establishment times
# to a given hostname, using addresses returned by getaddrinfo().
# Arguments are a hostname, and optionally a port number, otherwise 
# port 80 is assumed.
# 
# Usage: time-gai-connect hostname [port]
#
# An example run with the IETF webserver www.ietf.org:
# 
#     $ time-gai-connect.py www.ietf.org
#     2001:1890:123a::1:1e                     90.98601 ms
#     12.22.58.30                              76.32303 ms
#
# Author: Shumon Huque <shuque@upenn.edu>
#

import sys, socket, time

host = sys.argv[1]
if len(sys.argv) == 3:
    PORT = int(sys.argv[2])
else:
    PORT = 80

try:
    ai_list = socket.getaddrinfo(host, PORT, socket.AF_UNSPEC, 
                                 socket.SOCK_STREAM)
except socket.gaierror:
    print "getaddrinfo() error:", sys.exc_info()[1]
    sys.exit(1)

for (family, socktype, proto, canon, sockaddr) in ai_list:
    addr, port = sockaddr[0:2]
    try:
        t1 = time.time()
        s = socket.socket(family, socktype)
        s.connect(sockaddr)
        t2 = time.time()
        s.close()
    except socket.error:
        print "ERROR: %s -> %s" % (sockaddr[0], sys.exc_info()[1])
        pass
    else:
        print "%-40s %8.5f ms" % (sockaddr[0], (t2-t1)*1000.0)

