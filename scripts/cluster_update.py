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

import os
import logging
import kinetic
from kinetic.admin import AdminClient

LOG = logging.getLogger(__name__)

def update_cluster(version, binary_path, drives_path):
    drives = []
    with open(drives_path) as f:
        drives = f.readlines()

    toread = os.path.getsize(binary_path)
    data = bytearray(toread)
    try:
        with open(binary_path,'r') as f:
            f.readinto(data)
    except Exception as ex:
        print ex
        LOG.error("Failed to read update binary at {0}.".format(binary_path))
        return

    cs = [AdminClient(x.strip(' \n\t'), chunk_size=1024*1024) for x in drives]

    failed = []
    updated = 0
    skipped = 0
    for c in cs:
        try:
            c.connect()
            config = c.getLog([3]).configuration
            if config.version == version:
                LOG.info("Drive %s is already up to date, skipping it." % c)
                skipped += 1
            else:
                LOG.info("Updating drive %s from version %s..." % (c, config.version))
                c.updateFirmware(data)
                LOG.info("Drive %s updated." % c)
                updated += 1
        except:
            failed.append(c)
            LOG.error("Failed to connect to drive at {0}".format(c))

    LOG.info("Cluster update finished ({0} updated, {1} failed, {2} skipped)."
            .format(updated, len(failed), skipped))

    if len(failed) > 0:
        LOG.info("Printing failed drives.")
        for c in failed: print c

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Kinetic Drive Update Tool')
    parser.add_argument('version', metavar='version',
                       help='Targer version for update.')
    parser.add_argument('path', metavar='path',
                       help='Path to the update binary')
    parser.add_argument('--drives', dest='drives', default="drives",
                       help='Path to file with drives addresses')
    parser.add_argument('--log', dest='loglevel', default="info",
                       help='Logging level (default=warning)')

    args = parser.parse_args()

    numeric_level = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(format='%(asctime)-8s %(levelname)s: %(message)s',
                        datefmt="%H:%M:%S", level=numeric_level)

    update_cluster(args.version, args.path, args.drives)

if __name__ == '__main__':
    main()
