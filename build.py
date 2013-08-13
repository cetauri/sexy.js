__author__ = 'cetauri'
import os
import shutil
import io
import json
from io import StringIO




def configLoad():

    """
    환경 설정 로드

    """

    global globalConfig

    content = open("sexy.json").read()
    print(json)

    stringIO = StringIO(content)
    globalConfig = json.load(stringIO)


def main():
    """
    build

    """
    configLoad()

    print(globalConfig["libPath"])

    suffix = globalConfig["suffix"]
    libPath = globalConfig["libPath"]
    libs = globalConfig["libs"] #os.listdir(libPath)
    for f in libs:
    #     # print(f)
    #     # with open(prefix + f) as content_file:
    #     #     content = content_file.read()
    #     #     if regexp.search(content):
    #     #         print(f)
    #
        print(f)
        splitext = os.path.splitext(f)
        source = libPath + f
        target = libPath + splitext[0] + suffix + splitext[1]

        shutil.move(source, target)
        print("move file : "+ target)


if __name__ == '__main__':
    main()