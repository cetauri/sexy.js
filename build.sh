#!/bin/sh

cd node
git reset --hard HEAD
cd ..


python3 build.py
cd node

make
./node test.js
./node -v
./node
cd ..
