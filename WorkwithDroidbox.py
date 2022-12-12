import os

path='/home/user/samples/apk'
outpath='/home/user/samples/out'
logpath='/home/user/samples/log'
order='sudo docker run -it --rm -v /home/user/samples:/home/user/samples:ro -v ~/samples/out:/samples/out honeynet/droidbox '

mvorder='mv ./out/* '

for dirpath, dirname, filenames in os.walk(path):
	for filename in filenames:
		if not os.path.isdir(os.path.join(logpath,filename)):
			os.makedirs(os.path.join(logpath,filename))
		mkorder=order+os.path.join(dirpath,filename)+' 15'
		print(mkorder)
		os.system(mkorder)
		os.system(mvorder+os.path.join(logpath,filename))
		#print mkorder
		#print mvorder+os.path.join(logpath,filename)
