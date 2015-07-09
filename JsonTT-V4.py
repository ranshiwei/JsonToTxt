__author__ = 'Ran'
# coding=utf-8
# 此版本处理输入文件或文件夹下所有json文件
import json
import socket
import struct
import os.path


class JsonToTxt:

    def __init__(self):
        self.Ipdict = {}
        self.Dirpath = ''
        self.files = {}
        self.loadfiles = []

    def splitIp(self, ip, infoDict):
        ipKey = socket.ntohl(struct.unpack("I", socket.inet_aton(str(ip)))[0])
        self.Ipdict[ipKey] = infoDict

    def readCont(self, filepath):
        parentPath = os.path.dirname(filepath)
        self.Dirpath = parentPath + '/'
        file = open(filepath, 'r', encoding = 'utf-8')
        while 1:
                eachLine = file.readline()
                i = 0
                try:
                    info = json.loads(eachLine)
                    self.splitIp(info["host"], info)
                    # loglen = len(info["log"])
                    # while i < loglen:
                        # print(info["log"][i])
                        # i += 1
                except:
                    break

    def createTxt(self):

        keys = sorted(self.Ipdict)
        print('Converting...: ' + self.Dirpath)
        if os.path.exists(self.Dirpath+'/JsonToTxt'):
            dirpath = self.Dirpath+'JsonToTxt'
        else:
            os.mkdir(self.Dirpath+'JsonToTxt')
            dirpath = self.Dirpath+'JsonToTxt'

        i = 0
        while i < 256:
            file = open(dirpath + '/ip-'+ str(i) +'.txt', 'a', encoding = 'utf-8')
            self.files[i] = file
            i += 1
        for val in keys:
            ip = socket.inet_ntoa(struct.pack('I', socket.htonl(val)))
            name = ip.split('.')
            if int(name[0]) >= 0 and int(name[0]) <= 255:
                dicfile = self.files[int(name[0])]
                items = self.Ipdict[val]
                loglen = len(items["log"])
                logItems = []
                m = 0
                while m < loglen:
                    try:
                        logItem = items["log"][m]
                        logItem  = '{type}    {data}     {error}'.format(type = logItem["type"], data = logItem["data"], error = logItem["error"])
                        logItems.append({logItem})
                    except:
                        m += 1
                        continue
                    m += 1
                print('{host}\t\t {domain}\t {time}\t {log}'.format(host = items["host"], domain = items["domain"], time = items["time"], log = logItems), file=dicfile)
                logItem = {}
                logItems = []
        j = 0
        while j < 256:
            self.files[j].close()
            j += 1
        self.Ipdict = {}

    def ListFiles(self, dir, wildcard, recursion):
        exts = wildcard.split(" ")
        files = os.listdir(dir)
        for name in files:
            fullname=os.path.join(dir, name)
            if(os.path.isdir(fullname) & recursion):
                self.ListFiles(fullname, wildcard, recursion)
            else:
                for ext in exts:
                    if(name.endswith(ext)):
                        self.loadfiles.append(dir + '/' +name)
                        break

jtt = JsonToTxt()
PPath = input("input your file path or files folder path:")

if os.path.isfile(PPath):
    PPath = PPath.replace('\\', '/')
    print('Loading file: ' + PPath)
    jtt.readCont(PPath)
    jtt.createTxt()
else:
    PPath = PPath.replace('\\', '/')
    print('Root path:  ' + PPath)

    wildcard = ".json .JSON"
    jtt.ListFiles(PPath, wildcard, 1)
    loadfiles = jtt.loadfiles
    for i in range(len(loadfiles)):
        print('Current loading files: ' + str(loadfiles[i]))
        jtt.readCont(loadfiles[i])
        jtt.createTxt()