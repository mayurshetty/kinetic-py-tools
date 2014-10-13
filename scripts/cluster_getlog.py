#!/usr/bin/python
# Copyright (c) 2014 Seagate Technology

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

#@author: Mayur Shetty

import sys
import kinetic
import logging
import datetime
from kinetic.admin import AdminClient

LOG = logging.getLogger(__name__)

def getLog(drives_path):
    buf = 0
    today = datetime.datetime.today().strftime("%m-%d-%Y_%H.%M.%S")
    fname = "logfile" + today
    f1 = open(fname,'w+', buf)
    drives = []
    with open(drives_path) as f:
        drives = f.readlines()
	
    cs = [AdminClient(x.strip(' \n\t'), chunk_size=1024*1024) for x in drives]
    for c in cs:
        try:
            serialNum = c.getLog([3]).configuration.serialNumber
            version = c.getLog([3]).configuration.version
            nic1 = c.getLog([3]).configuration.interface[0].name
            ip1 = c.getLog([3]).configuration.interface[0].ipv4Address
            mac1 = c.getLog([3]).configuration.interface[0].MAC
            nic2 = c.getLog([3]).configuration.interface[1].name
            ip2 = c.getLog([3]).configuration.interface[1].ipv4Address
            mac2 = c.getLog([3]).configuration.interface[1].MAC
            hda_temp = c.getLog([1]).temperature[0].current
            cpu_temp = c.getLog([1]).temperature[1].current
            total_capacity = c.getLog([2]).capacity.nominalCapacityInBytes
            capacity_full = c.getLog([2]).capacity.portionFull
            util_name1 = c.getLog([0]).utilization[0].name
            util_value1 = c.getLog([0]).utilization[0].value
            util_name2 = c.getLog([0]).utilization[1].name
            util_value2 = c.getLog([0]).utilization[1].value
            util_name3 = c.getLog([0]).utilization[2].name
            util_value3 = c.getLog([0]).utilization[2].value
            util_name4 = c.getLog([0]).utilization[3].name
            util_value4 = c.getLog([0]).utilization[3].value

    	    print >>f1, "Serial Number:\t\t %s" % serialNum
            print >>f1, "Version:\t\t %s" % version
            print >>f1, "Network Port 1:\t\t %s" % nic1
            print >>f1, "IP Address:\t\t %s" % ip1
            print >>f1, "MAC Address:\t\t %s" % mac1
            print >>f1, "Network Port 2:\t\t %s" % nic2
            print >>f1, "IP Address:\t\t %s" % ip2
            print >>f1, "MAC Address:\t\t %s" % mac2
            print >>f1, "HDA Temperature:\t %s F" % hda_temp
            print >>f1, "CPU Temperature:\t %s F" % cpu_temp
            print >>f1, "Total Capacity:\t\t %s TB" % (total_capacity/float(1000000000000))
            print >>f1, "Capacity Full:\t\t %s Bytes" % capacity_full
            print >>f1, "Hard Disk:\t\t %s" % util_name1
            print >>f1, "Hard Disk Utlization:\t %s" % util_value1
            print >>f1, "Network Port :\t\t %s" % util_name2
            print >>f1, "Network Utilization:\t %s" % util_value2
            print >>f1, "Network Port :\t\t %s" % util_name3
            print >>f1, "Netowrk Utilization:\t %s" % util_value3
            print >>f1, "CPU:\t\t\t %s" % util_name4
            print >>f1, "CPU Utilization:\t %s" % util_value4
            print >>f1, "-------------------------------------------\n"

        except:
            LOG.error("Failed to connect to drive at {0}".format(c))
            return

def python_version():
    if sys.version_info <= (2,7,3):
        print "Python Version is too old. Update Python to 2.7.3 or later"
        exit()

def main():
    python_version()
    import argparse

    parser = argparse.ArgumentParser(description='Kinetic drive info using GetLog')
    parser.add_argument('drives_path', metavar='<drives_path>',
		       help='Path to the file with the drive IP addresses')

    args = parser.parse_args()
    getLog(args.drives_path)


if __name__ == '__main__':
    main()
