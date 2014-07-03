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

LOG = logging.getLogger(__name__)

def update(hostname, port, path):

    from kinetic.admin import AdminClient

    ac = None
    try:
        ac = AdminClient(hostname,port)
        ac.connect()
    except:
        LOG.error("Failed to connect to drive at {0}:{1}".format(hostname,port))
        return

    data = ''
    try:
        f = open(path)
        chunk = 'x'

        while chunk:
            chunk = f.read(4096)
            data += chunk
            LOG.debug("Read: " + str(len(data)))
    except:
        LOG.error("Failed to read update binary at {0}.".format(path))
        return

    LOG.info("Firmware read, Size={0}".format(len(data)))
    ac.updateFirmware(data)
    LOG.info("Firmware update sent to drive.")

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Kinetic Drive Update Tool')
    parser.add_argument('host', metavar='H',
                       help='Hostname or IP address for the drive')
    parser.add_argument('path', metavar='p',
                       help='Path to the update binary')
    parser.add_argument('--log', dest='loglevel', default="info",
                       help='Logging level (default=warning)')
    parser.add_argument('--port', dest='port', type=int, default=8123,
                       help='Port number on the host listening for kinetic')

    args = parser.parse_args()

    numeric_level = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(format='%(asctime)-8s %(levelname)s: %(message)s',
                        datefmt="%H:%M:%S", level=numeric_level)

    update(args.host,args.port, args.path)

if __name__ == '__main__':
    main()

