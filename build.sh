#!/bin/sh

git submodule init
git submodule update

cd node
git reset --hard HEAD
git checkout origin/v0.10.18-release
cd ..


python3 build.py
cd node

./configure
make

cd ..

cp node/out/Release/node sexy

./sexy test.js
./sexy -v
# ./sexy


# cp ./sexy /usr/local/bin