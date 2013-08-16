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

    # global globalConfig

    content = open("sexy.json").read()
    print(json)

    stringIO = StringIO(content)
    return json.load(stringIO)


def main():
    """
    build

    """
    globalConfig = configLoad()

    suffix = globalConfig["suffix"]
    libPath = globalConfig["libPath"]
    libs = globalConfig["libs"]
    for f in libs:
    #     # print(f)
    #     # with open(prefix + f) as content_file:
    #     #     content = content_file.read()
    #     #     if regexp.search(content):
    #     #         print(f)
    #

        # print(f)
        splitext = os.path.splitext(f)
        source = libPath + f
        target = libPath + splitext[0] + suffix + splitext[1]

        if os.path.exists(source):
            shutil.move(source, target)
            print(f +" move "+ target)


    # node.gyp 변경
    gyp = globalConfig["gyp"]

    old_gyp = ""
    for line in open(gyp["path"]):
        old_gyp += line

    # lib list
    start = old_gyp.find(gyp["prefix"])
    end = old_gyp.find(gyp["suffix"], start)

    libList = list(old_gyp)[start:end-4]
    libText = "".join(libList).split("\n")
    # print(  libText )

    new_gyp = ""
    delimiter = "'lib/"

    for line in libText:
        # print (line)
        if line.__contains__(delimiter):
            s = line.find(delimiter)
            e = line.find("',", s)

            func = list(line)[s + len(delimiter):e]
            func = "".join(func)
            func = os.path.splitext(func)

            new_gyp += ("      'lib/" + func[0] + suffix + func[1] + "',\n")
        else:
            new_gyp += line +"\n"

    # print("".join(new_gyp))

    gypList = list(old_gyp)
    print( "".join(gypList[0:start]) )
    print( "".join(new_gyp)+"," )
    print( "".join(gypList[end:]))
    # source 내용 변경

if __name__ == '__main__':
    main()