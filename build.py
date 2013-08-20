#! #!/usr/bin/python3__author__ = 'cetauri'import osimport shutilimport jsonimport loggingfrom io import StringIOimport logging.configimport sysimport relogging.config.fileConfig('logging.conf')# create loggerlogger = logging.getLogger('simpleExample')def configLoad():    """    환경 설정 로드    """    content = open("sexy.json").read()    stringIO = StringIO(content)    return json.load(stringIO)def libraryRename(globalConfig):    suffix = globalConfig["suffix"]    libPath = globalConfig["libPath"]    libs = globalConfig["libs"]    for f in libs:        splitext = os.path.splitext(f)        source = libPath + f        target = libPath + splitext[0] + suffix + splitext[1]        if os.path.exists(source):            shutil.move(source, target)            print(f + " move " + target)def rewriteGYP(globalConfig):    """    node.gyp library_files rewrite    :param globalConfig:    """    gyp = globalConfig["gyp"]    suffix = globalConfig["suffix"]    old_gyp = ""    for line in open(gyp["path"]):        old_gyp += line    # get only lib list    start = old_gyp.find(gyp["prefix"])    end = old_gyp.find(gyp["suffix"], start)    libList = list(old_gyp)[start:end]    libText = "".join(libList).split("\n")    # rewrite library_files    new_gyp = ""    delimiter = "'lib/"    # print(libs)    for line in libText:        func_name = line.replace(delimiter, "").replace("',", "")        if func_name.strip() in globalConfig["libs"]:            s = line.find(delimiter)            e = line.find("',", s)            func = list(line)[s + len(delimiter):e]            func = "".join(func)            func = os.path.splitext(func)            new_gyp += ("      'lib/" + func[0] + suffix + func[1] + "',\n")        else:            new_gyp += line + "\n"    # save    gypList = list(old_gyp)    output = open(gyp["path"], "w")    output.write("".join(gypList[0:start]) + new_gyp + "".join(gypList[end:]))    output.close()def markVersion(globalConfig):    """    :param globalConfig:    :rtype : object    """    sexyConfig = globalConfig["sexy"]    version = sexyConfig["version"]    version_string = sexyConfig["version_string"]    path = sexyConfig["path"]    new_node_version = ""    node_version = open(path)    for line in node_version:        if line.startswith(version_string):            new_node_version += version_string + " \"\\nSexy.js v" + version + "\"\n"        else:            new_node_version += line    output = open(path, "w")    output.write(new_node_version)    output.close()    # print(new_node_version)def rewriteGlobalVars(globalConfig):    """    NativeModule.wrapper 에 \n 을 넣으면 에러 메시지에  suffix 노출을 막을 수 있다    """    logging.info("# " + sys._getframe().f_code.co_name + " start")    node_path = globalConfig["global"]["path"]    node_code = open(node_path).read()    suffix = globalConfig["suffix"]    if not node_code.__contains__(suffix):        for _var in globalConfig["global"]["list"]:            logging.info(_var)            node_code = node_code.replace(_var, _var + suffix)        # print(node_code)        output = open(node_path, "w")        output.write(node_code)        output.close()    logging.info("# " + sys._getframe().f_code.co_name + " finish")def reRequireLibrary(globalConfig):    # require(', ') 사이의 값    # ",' 가능    # 전후방 탐색으로 원하는 결과만    suffix = globalConfig["suffix"]    express = '(?<=require\(["\'])(\w+?)(?=["\']\))'    regexp = re.compile(express)    count = 0    for root, dirs, files in os.walk("node/lib"):        for file in files:            if file.endswith(".js"):                jsFile = root + "/" + file                print(jsFile)                try:                    jsSource = open(jsFile).read()                    if regexp.search(jsSource):                        freq = len(regexp.findall(jsSource))                        count += freq                        print(regexp.findall(jsSource))                        # print(re.sub(express, "require('\\1" + suffix + "')", jsSource))                        print(re.sub(express, "\\1" + suffix, jsSource))                except UnicodeDecodeError as e:                    if file != "parser-high-byte-character.js":                        assert str(e) == "", str(e) + " (" + jsFile + ")"                except BaseException as e:                    print(str(e))                    assert str(e) == "", "Unknown Exception"    print(count)def main():    """    build    """    globalConfig = configLoad()    #    # libraryRename(globalConfig)    #    # rewriteGYP(globalConfig)    #    # rewriteGlobalVars(globalConfig)    #    # markVersion(globalConfig)    reRequireLibrary(globalConfig)    #TODO loggingif __name__ == '__main__':    main()