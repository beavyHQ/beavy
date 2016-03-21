#!/bin/bash

set -e
echo "Downloading ICU – please wait."
wget --quiet http://download.icu-project.org/files/icu4c/57rc/icu4c-57rc-src.tgz

# checking md5sum!
echo 26acb3f79ba926c26bd76094bcf85866 *icu4c-57rc-src.tgz | md5sum -c

echo "Compiling and installing ICU"
tar xf icu4c-57rc-src.tgz
cd icu/source
./configure prefix=/usr && make && make install
echo "ICU successfully installed."
