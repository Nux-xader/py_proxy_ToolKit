import requests, sys, os
from concurrent.futures import ThreadPoolExecutor as thrd


log_file = "proxy_py_log.txt"
header = {"user-agent": "Mozilla/5.0 (Linux; Android 6.0.1; Redmi Note 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Mobile Safari/537.36"}
try: os.remove(log_file)
except: pass

class Proxy:
	def __init__(self):
		self.url = "http://httpbin.org"
		self.headers = {
			"user-agent": header["user-agent"], 
			"Referer": "https://google.com/", 
			"Connection": "keep-alive"}
		try:
			self.sess = requests.Session()
			self.sess.get(self.url+"/ip", headers=self.headers)
		except Exception as e:
			print(" [!] Please Check Your Internet Connection")
			open(log_file, "a").write(str(e)+"\n")
			sys.exit()

	def check(self, proxy):
		dummy_sess = self.sess
		try:
			ip = dummy_sess.get(self.url+"/ip", headers=self.headers, 
				proxies={"http": proxy,"https": proxy}, timeout=15)#.json()["origin"]
			return True
		except Exception as e:
			open(log_file, "a").write(str(e)+"\n")
			return False

	def get_free_proxy_list_net(self):
		dummy_sess = self.sess
		try:
			html = dummy_sess.get("https://free-proxy-list.net", headers=self.headers,  timeout=60).text
			pxy = html.split("</textarea>")[0].split(">")[-1]
			input(pxy)
			return True
		except Exception as e:
			open(log_file, "a").write(str(e)+"\n")
			return False


def clr():
	os.system('cls' if os.name == 'nt' else 'clear')

def banner():
	print("""
 █▀█ █▀█ █▀█ ▀▄▀ █▄█
 █▀▀ █▀▄ █▄█ █ █  █ 
 
 █▀█ █▄█
 █▀▀  █  V 1.0.0

 About Developer : https://github.com/Nux-xader
 Contact         : https://wa.me/+6281251389915
 _______________________________________________
""")

def checkProxy(px, saveTo, proxy, viewProgres=True):
	global success, filed
	status = px.check(proxy)
	if status:
		open(saveTo+"/live.txt", 'a').write("\n"+proxy)
		success+=1
	else:
		open(saveTo+"/die.txt", 'a').write("\n"+proxy)
		filed+=1
	if viewProgres: print(f"\n [Success >> {str(success)}]--[Total >> {str(total)}]--[Filed >> {str(filed)}]--[{proxy}]")


def loadProxy(path):
	try:
		data = [x for x in str(open(path, 'r').read()).split("\n") if len(x) > 5]
	except Exception as e:
		open(log_file, 'a').write(str(e))
		input(" [!] "+str(e)+"\n [Press Enter to Continue]")
		sys.exit()
	return data


def setSave():
	saveTo = str(input(" Save to : "))
	if saveTo.split(".")[-1] == "txt": saveTo = saveTo[:-4]
	try:
		os.mkdir(saveTo)
	except:
		x = str(input(" Folder "+saveTo+" already exists\n Are you sure replace it [y/n] ")).lower()
		if x == "y":
			[os.remove(i) for i in os.listdir(saveTo)]
		elif x == "n":
			sys.exit()
		else:
			print(" [!] Invalid input")
			sys.exit()
	return saveTo


def setThread():
	while True:
		try:
			num = int(input(" Input thread (default 50) : "))
			break
		except:
			print(" [!] Invalid input")
	return num


def menu():
	global success, filed, total
	clr()
	banner()
	print(""" Menu :
 [1] Proxy checker
 [0] Exit
""")
	success, filed, total = 0, 0, 0
	choice = str(input(" Choice : "))
	if choice == "1":
		data = loadProxy(str(input(" File list proxy : ")))
		total = len(data)
		saveTo = setSave()
		t = setThread()
		px = Proxy()
		with thrd(max_workers=t) as pool:
			for i in data:
				pool.submit(checkProxy, px, saveTo, i)


menu()