#!/bin/sh

git submodule init
git submodule update

cd node
git reset --hard HEAD
cd ..


python3 build.py
cd node

./configure
make

cd ..

cp node/out/Release/node sexy

# ./sexy test.js
# ./sexy -v
# ./sexy


# cp ./sexy /usr/local/bin