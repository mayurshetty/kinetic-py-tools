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

#@author: Ignacio Corderi

import logging
from kinetic.admin import AdminClient

LOG = logging.getLogger(__name__)

class DiscoveredDrive(object):

    def __init__(self, config, address):
        self.config = config
        self.availableAt = [address]

def discover(base, timeout, drives_path):
    current = 1

    drives = {}

    if '.' in base and not base.endswith('.'):
        base += '.'

    while current < 255:
        try:
            address = base + str(current)
            c = AdminClient(address, connect_timeout=timeout)
            config = c.getLog([3]).configuration

            LOG.info("Discovered a drive at {0} (SN={1})"
                     .format(address, config.serialNumber))

            if config.serialNumber in drives:
                drives[config.serialNumber].availableAt.append(address)
            else:
                drives[config.serialNumber] = DiscoveredDrive(config, address)

        except: pass

        current += 1

    with open(drives_path,'w+') as f:
        for sn, d in drives.iteritems():
            LOG.info("Drive with SN={0} (Version={2}) available at {1}"
                     .format(sn, d.availableAt, d.config.version))
            f.write(d.availableAt[0] + "\n")

    LOG.info("Discovered {0} drives.".format(len(drives)))

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Kinetic Discovery Tool')
    parser.add_argument('subnet', metavar='subnet',
                       help='Subnet to scan (i.e. 192.168.33.)')
    parser.add_argument('--timeout', dest='timeout', type=int, default=50,
                       help='Connect timeout in ms (default=50)')
    parser.add_argument('--output', dest='drives', default="drives",
                       help='Path to file with drives addresses')
    parser.add_argument('--log', dest='loglevel', default="info",
                       help='Logging level (default=info)')

    args = parser.parse_args()

    numeric_level = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(format='%(asctime)-8s %(levelname)s: %(message)s',
                        datefmt="%H:%M:%S", level=numeric_level)

    discover(args.subnet, timeout=(args.timeout / 1000.), drives_path=args.drives)

if __name__ == '__main__':
    main()
