from git import Repo
from datetime import datetime
import json
import time
import re
import os

configFile = "config.txt"
exsitsConfig = True
if not os.path.exists(configFile):
    exsitsConfig = False
    os.system(r'echo off > {}'.format(configFile))

gitPath = ""
gitList = []
if exsitsConfig == True:
    f = open('config.txt','r')
    text = f.readlines()
    index = 1
    print('0.输入路径')
    gitPathAll = ""
    for i in text:
        if i.strip()!='':
            gitList.append(i)
            print(str(index) + "."+i)
            gitPathAll += i + "\n"
            index += 1
    gitPathNo = input('请选择序号:')
    if int(gitPathNo)==0:
        gitPath = input("请输入git本地绝对路径(例如C:\\test):")
        f = open('config.txt', 'w')
        f.write(gitPathAll + gitPath)
        f.close()
    else:
        gitPath = gitList[int(gitPathNo)-1]
else:
    gitPath = input("请输入git本地绝对路径(例如C:\\test):")
    f = open('config.txt', 'w')
    f.write(gitPath)
    f.close()


startTime = input("请输入提交时间(例如2020-06-18 20:54:00):")

logStartTime = datetime.strptime(startTime,"%Y-%m-%d %H:%M:%S")

r = Repo(gitPath)
r.iter_commits()

# print([str(i.message) for i in r.iter_commits()]) # 获取提交信息
# print([str(i.message) for i in r.iter_commits()]) # 查看提交的hash值

index = 1
resultArray = []
result = ""
hasAddVersion = False
for item in r.iter_commits():
    timeArray = time.localtime(item.committed_date)
    logTimeStr = time.strftime("%Y-%m-%d %H:%M:%S",timeArray)
    logTime = datetime.strptime(logTimeStr,"%Y-%m-%d %H:%M:%S")
    if(logTime >= logStartTime):
        messageArray = item.message.split("\n")
        for message in messageArray:
            if message.strip()!='':
                print(message)
                messageTmp = re.match("[0-9]{1,3}\.([^\s]*)|([^\s]*)",message).group(1)
                print(messageTmp)
                messageFinal = ""
                if(messageTmp == None):
                    messageFinal = message
                else:
                    messageFinal = messageTmp
                print(messageFinal)
                if "版本号" not in messageFinal:
                    resultArray.append(messageFinal)
                else:
                    if hasAddVersion == False:
                        hasAddVersion = True
                        resultArray.append(messageFinal)


for message in reversed(resultArray):
    result += str(index)+"."+ message + "\n"
    index += 1

print()
print("-------------------->结果分割线start<--------------------")
print()
print(result)
print()
print("-------------------->结果分割线end<--------------------")
print()

# commit_log = r.git.log('--pretty={"commit":"%h","author":"%an","summary":"%s","date":"%cd"}', max_count=100,
#                           date='format:%Y-%m-%d %H:%M:%S')
# log_list = commit_log.split("\n")
# real_log_list = [eval(item) for item in log_list]
# print(real_log_list)

# for item in log_list:
#     itemJson = json.loads(item)
#     logTime = datetime.strptime(itemJson['date'],"%Y-%m-%d %H:%M:%S")
#     if(logTime > logStartTime):
#         print(itemJson['summary'])