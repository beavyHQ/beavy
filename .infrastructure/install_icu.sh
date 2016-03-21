#!/bin/bash

set -e
mkdir -p ~/.icu_cache
mkdir -p ~/lib
cd ~/.icu_cache
if [ ! -d "icu4c-57rc-src" ]; then
    echo "Downloading latest ICU – please wait."
    wget --quiet http://download.icu-project.org/files/icu4c/57rc/icu4c-57rc-src.tgz

    # checking md5sum!
    echo "26acb3f79ba926c26bd76094bcf85866 *icu4c-57rc-src.tgz" | md5sum -c -

    tar xf icu4c-57rc-src.tgz
    mv icu icu4c-57rc-src
fi

[ "$TRAVIS" == "true" ] && PREFIX="~/lib" || PREFIX="/usr"

echo "Compiling and installing ICU to $PREFIX"
cd icu4c-57rc-src/source
./configure prefix=$PREFIX && make && make install
echo "ICU successfully installed."
