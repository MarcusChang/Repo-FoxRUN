import json
import time
import os
import pdb
import collections
from collections import OrderedDict

INTERVAL=5
FOLDER=r'testResult/performance'

class PerfMeaHandler():    
    def __init__(self,device):
	self.start = 0
	self.stop = 0	
	self.keys =[]
	self.info= ''
	self.caseName=''
	self.AppName=''
	self.device_serial=device
	
    def startmea(self,casename,appname):        
        self.start = time.time()	
        self.caseName=casename
	self.AppName=appname.capitalize()
	
    def stopmea(self):
	self.stop = time.time()	
	self.generateJson(True)

    def getmemory(self,isSuccess,callstack,path):
	#pdb.set_trace()
	if (self.device_serial == None):
	    shellcommand="adb shell b2g-info > "
	else:
	    shellcommand="adb " +"-s "+self.device_serial+" shell b2g-info > "
        if isSuccess:
            os.system(shellcommand+path+r'/'+"meminfo.txt")
        else:
            self.info=callstack
    
    def parseMeminfo(self,path):
	meminfo = dict()
        try:
            with open(path+r'/'+"meminfo.txt", 'r') as f:
                data = f.readline().strip('\r\n')
		
		i = 0
		
		#exclude first line
		if data.find('megabytes') > 0:
		    data = f.readline().strip('\r\n')		
			
		while data: 		    
		
		    ps = self.processline(data)		
		    
		    if len(ps) != 0:			
			meminfo[i] = ps
			
		    data = f.readline().strip('\r\n')
		    i =i+1

        except IOError as ioerr:
            print('file read error: '+ str(ioerr))
	return meminfo
    
    def processline(self,line):
	ps = dict()
	arr = line.split(' ')
	fields = []
	    
	if len(self.keys) == 0 :
	    for i in range(len(arr)):
		if arr[i] !='':
		    self.keys.append(arr[i])	    
	else:
	    for i in range(len(arr)):
		if arr[i] !='':
		    #remove duplicate name filed, there are duplicate 'name' fields  when have space between string 'name'
		    if arr[i] == 'Keyboa' or arr[i] == 'a':
			continue
		    fields.append(arr[i])
	
	for i in range(len(fields)):
	    ps[self.keys[i]]=fields[i]		
	
	return ps
    
    def generateJson(self,isSuccess,callstack=None):	
	
	try: 
	    path = os.path.join(os.path.pardir,FOLDER,self.device_serial)
	    
	    casenamepath = self.caseName+'-'+time.strftime('%Y-%m-%d-%H-%I-%M-%S',time.localtime(time.time()))
	    
	    appPath = os.path.join(path,self.AppName+r'/'+casenamepath)
	   # pdb.set_trace()
	    if not os.path.exists(appPath):    
		os.makedirs(appPath)    
	    
	    #collect meminfo
	    self.getmemory(isSuccess,callstack,appPath)
	    time.sleep(INTERVAL)
	    meminfo = self.parseMeminfo(appPath)	
	    
	    collectionResult = self.formatdata(meminfo,isSuccess)
	    #pdb.set_trace()
	    
	    jsonfilename = time.strftime('%Y-%m-%d-%H-%I-%M-%S',time.localtime(time.time()))
	    
	    #create empty json file
	    filename=jsonfilename+'.json'    
	    jsonfile = os.path.join(appPath,filename)   
	
	    if not os.path.exists(jsonfile):
		#write meminfo with json to file
		file_object = open(jsonfile,'w')
		file_object.write(json.dumps(collectionResult,sort_keys=False,indent=1))
		file_object.close()
	except Exception, e:
	    print e	    
	
        
    def formatdata(self, memdata,isSuccess):	
	#memdata info example
	#{1: {'CPU(s)': '299.0', 'NAME': 'b2g', 'PID': '293', 'OOM_ADJ': '0', 'USS': '71.6', 'USER': 'root', 'RSS': '96.7', 'PSS': '79.3', 'PPID': '1', 'VSIZE': '249.3', 'NICE': '0'}, 2: {'CPU(s)': '3.0', 'NAME': '(Nuwa)', 'PID': '1117', 'OOM_ADJ': '0', 'USS': '2.5', 'USER': 'root', 'RSS': '19.9', 'PSS': '6.8', 'PPID': '293', 'VSIZE': '54.8', 'NICE': '0'}, 3: {'CPU(s)': '19.4', 'NAME': 'Homescreen', 'PID': '1210', 'OOM_ADJ': '2', 'USS': '31.7', 'USER': 'u0_a1210', 'RSS': '54.9', 'PSS': '38.0', 'PPID': '1117', 'VSIZE': '128.0', 'NICE': '1'}, 4: {'CPU(s)': '1.1', 'NAME': 'Built-in', 'PID': '1261', 'OOM_ADJ': '3', 'USS': '6.3', 'USER': 'u0_a1261', 'RSS': '21.7', 'PSS': '9.2', 'PPID': '1117', 'VSIZE': '63.0', 'NICE': '1'}, 5: {'CPU(s)': '6.7', 'NAME': 'Calendar', 'PID': '1919', 'OOM_ADJ': '11', 'USS': '14.2', 'USER': 'u0_a1919', 'RSS': '32.0', 'PSS': '17.9', 'PPID': '1117', 'VSIZE': '83.8', 'NICE': '18'}, 6: {'CPU(s)': '0.6', 'NAME': '(Preallocated', 'PID': '4234', 'OOM_ADJ': '1', 'USS': '5.7', 'USER': 'u0_a4234', 'RSS': '18.8', 'PSS': '8.0', 'PPID': '1117', 'VSIZE': '60.8', 'NICE': '18'}}
        #{'passes': True, 'end': '0', 'start': '0', 'testcase': 'aa', 'application': 'album', 'duration': '0'}
	
	
	stats={	    
	    "testcase":self.caseName,
	    "passes":isSuccess,    
	    "start":str(self.start),
	    "end":str(self.stop),
	    "duration":str(int(self.stop-self.start)),
	    "application":self.AppName
	}
	
	app={
	    "name": self.AppName,
	    "uss": '',
	    "pss": '',
	    "rss": '',
	    "vsize": '',
	    "cpu": ''
	}
	system={
	    "name": 'b2g',
	    "uss": '',
	    "pss": '',
	    "rss": '',
	    "vsize": '',
	    "cpu":''
	}
	mozPerfMemory={
	    "app": app,
	    "system": system	    
	}
	
	appAverage= {
	    "uss": '',
	    "pss": '',
	    "rss": '',
	    "vsize": '',
	    "cpu":''
		    }
	
	systemAverage={
	    "uss": '',
	    "pss": '',
	    "rss": '',
	    "vsize": '',
	    "cpu":'' 
		    }
	
	failerInfo={
	    "title":'',
	    "stack":''
	}
	
	
	dirResult = {
	    'stat':stats,
	    'pass':{				
		'mozPerfMemory':mozPerfMemory,
		'mozPerfDurations':''
		},
	    'failure': ''		
	}
	
	
	for k,v in memdata.items():
	   
	    if v['NAME'] == 'b2g':
		system['uss'] = v['USS']		
		system['pss'] = v['PSS']
		system['rss'] = v['RSS']
		system['vsize'] = v['VSIZE']
		system['cpu'] = v['CPU(s)']
	    if cmp(v['NAME'], self.AppName) == 0:
		
		app['uss'] = v['USS']		
		app['pss'] = v['PSS']
		app['rss'] = v['RSS']
		app['vsize'] = v['VSIZE']
		app['cpu'] = v['CPU(s)']
	#pdb.set_trace()	

	collectionResult = collections.OrderedDict(sorted(dirResult.items(),key=lambda t:len(t[0])))
	
	return collectionResult    

