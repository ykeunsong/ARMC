#coding: utf-8
import os
import re

p=re.compile(r'String #\d{1,3}: .*\n', re.UNICODE)

path='./strings/0-normal'
#path='./strings/1-malware'

malstrings=['chmod', 'insmod', 'bash', 'killall', 'mkdir', 'getprop', 'content://mms-sms', 'content://sms', 'content://browser/bookmarks', 
           'BOOKMARKS_URI', 'CONTENT_URI', 'EXTERNAL_CONTENT_URI', 'INTERNAL_CONTENT_URI', 'NEW_OUTGOING_CALL']

dic={}

for dirpath, dirnames, filenames in os.walk(path):
    for filename in filenames:
        #print(os.path.join(dirpath,filename))
        with open(os.path.join(dirpath,filename), 'r', encoding='UTF8') as f:
            #print(filename)
            data=f.read()#.replace('\n', ' ').split(' ')
            for malstring in malstrings:
                #for st in data:
                if malstring in data:#st==malstring:
                    print(malstring+' '+filename+'\\n')

word_freq=[]
for key, value in dic.items():
    word_freq.append((value, key))


word_freq.sort(reverse=True)
#print(word_freq)

