__author__ = 'cetauri'import osimport shutilimport jsonfrom io import StringIOdef configLoad():    """    환경 설정 로드    """    content = open("sexy.json").read()    stringIO = StringIO(content)    return json.load(stringIO)def libraryRename(globalConfig):    suffix = globalConfig["suffix"]    libPath = globalConfig["libPath"]    libs = globalConfig["libs"]    for f in libs:        splitext = os.path.splitext(f)        source = libPath + f        target = libPath + splitext[0] + suffix + splitext[1]        if os.path.exists(source):            shutil.move(source, target)            print(f + " move " + target)def rewriteGYP(globalConfig):    """    node.gyp library_files rewrite    """    gyp = globalConfig["gyp"]    suffix = globalConfig["suffix"]    old_gyp = ""    for line in open(gyp["path"]):        old_gyp += line    # get only lib list    start = old_gyp.find(gyp["prefix"])    end = old_gyp.find(gyp["suffix"], start)    libList = list(old_gyp)[start:end - 4]    libText = "".join(libList).split("\n")    # rewrite library_files    new_gyp = ""    delimiter = "'lib/"    # print(libs)    for line in libText:        func_name = line.replace(delimiter, "").replace("',", "")        if func_name.strip() in globalConfig["libs"]:            s = line.find(delimiter)            e = line.find("',", s)            func = list(line)[s + len(delimiter):e]            func = "".join(func)            func = os.path.splitext(func)            new_gyp += ("      'lib/" + func[0] + suffix + func[1] + "',\n")        else:            new_gyp += line + "\n"    # save    gypList = list(old_gyp)    output = open(gyp["path"], "w")    output.write("".join(gypList[0:start]) + new_gyp + "".join(gypList[end:]))    output.close()def main():    """    build    """    globalConfig = configLoad()    libraryRename(globalConfig)    rewriteGYP(globalConfig)    # source 내용 변경    sexyConfig = globalConfig["sexy"]    version = sexyConfig["version"]    version_string = sexyConfig["version_string"]    path = sexyConfig["path"]    node_version = open(path)    soruce_code = node_version.read()    soruce_code = soruce_code.replace(version_string, version_string + " \"\\nSexy.js v"+version + "\"");    output = open(path, "w")    output.write(soruce_code)    output.close()if __name__ == '__main__':    main()