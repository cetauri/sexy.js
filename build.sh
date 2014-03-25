#!/bin/sh
export SEXY_NODE_VERSION="v0.10.26"

git submodule init
git submodule update

cd node
git reset --hard HEAD
git checkout master

git branch -D $SEXY_NODE_VERSION
git checkout -b $SEXY_NODE_VERSION -t origin/$SEXY_NODE_VERSION-release
git checkout $SEXY_NODE_VERSION

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