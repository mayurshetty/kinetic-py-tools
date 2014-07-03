# Kinetic Pyhton Tools
This project contains tools designed to help with deployment and management of Kinetic drives

## Initial Setup
````
git clone https://github.com/Seagate/kinetic-py-tools.git
````

## Available scripts

### Discovery
````
python scripts/discover.py <subnet: 192.168.0>
````
The default output is a file `drives` which contains one line per drive.
Some of the other scripts that operate over a set of drives require this input file.

### Kinetic Drive Firmware Update
````
python scripts/update.py <host> <path>
````

### Kinetic Cluster Update
````
python scripts/cluster_update.py <target_version> <path>
````
This will update all drives in the file `drives` with a version different than `<target_version>`


License
-------

This project is licensed under The MIT License (MIT)
* [Markdown](LICENSE/mit.md) version
* [Original](LICENSE/mit.txt) version
