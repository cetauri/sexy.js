#!/usr/bin/env python3
__author__ = 'cetauri'
import os
import json
import sys
from io import StringIO
import re
import shutil

def configLoad():

    """
    환경 설정 로드

    """

    content = open("sexy.json").read()
    stringIO = StringIO(content)
    return json.load(stringIO)


def main():
    print("start");
    if len(sys.argv) != 2:
        print("Please insert 'target Path' argument. "
              "\n"
              "ex) python3 npmChange.py ~/temp/project/aaa")
        sys.exit(0)


    path = sys.argv[1]+ '/node_modules/'

    globalConfig = configLoad()
    suffix = globalConfig["suffix"]
    libs = globalConfig["libs"]
    globalVars = globalConfig["global"]["list"]

    express = '(?<=require\(["\'])(' + "|".join(libs) + '?)(?=["\']\))'
    regexp = re.compile(express)

    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".js"):
                jsFile = root + "/" + file
                # print(jsFile)
                try:
                    jsSource = open(jsFile).read()
                    if regexp.search(jsSource):
                        freq = len(regexp.findall(jsSource))
                        count += freq

                        if not jsSource.__contains__(libs[0]+suffix):
                            jsSource = re.sub(express, "\\1" + suffix, jsSource)

                            # output = open(jsFile, "w")
                            # output.write(source)
                            # output.close()

                    # __filename, __dirname replace
                    for _var in globalVars:
                        if jsFile.endswith("src/node.js"):
                            continue

                        replaceVar = _var + suffix
                        if not jsSource.__contains__(replaceVar):
                            jsSource = jsSource.replace(_var, replaceVar)
                            # print(jsFile)

                    output = open(jsFile, "w")
                    output.write(jsSource)
                    output.close()

                except UnicodeDecodeError as e:
                        print("UnicodeDecodeError : path : " + jsFile)

                except BaseException as e:
                    print(str(e))
                    assert str(e) == "", "Unknown Exception"

    # folder(node_modules) rename
    node_modules = globalConfig["node_modules"]
    for npm in node_modules:
        source = path + npm
        target = source + suffix
        try:
            shutil.move(source, target)
        except IOError as e:
            print(str(e))


if __name__ == '__main__':
    main()
