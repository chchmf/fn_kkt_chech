import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import time

model_code = input("Введи код модели:")

start = time.time()

file = open("schedule.txt","r", encoding='utf-8')
list = []

for eachLine in file:
    a = eachLine.strip().split("\n")
    for i in range(len(a)):
        list.append(a[i].replace('"',''))

def checkfns(sn, model):
	header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
			"Host": "kkt-online.nalog.ru",
			"Accept-Language": "ru",
			"Accept-Encoding": "gzip, deflate, br",
			"Connection": "keep-alive"}
	s = requests.Session()
	url = "https://kkt-online.nalog.ru/lkip.html?query=/fn/model/check&factory_number="+sn+"&model_code="+model
	req = s.get(url, headers=header, verify=False)
	return json.loads(req.content)

csv = open("list.csv","w")
csv.write("sn"+";"+"status"+"\n")

for i in range(len(list)):
	print(list[i], checkfns(list[i], model_code))
	csv.write(str(list[i])+";"+str(checkfns(list[i], model_code))+"\n")

csv.close()
stop = time.time() - start
input(f"Закончил за: {stop} секунд. Закрой меня...")

#st3f = 0080
#st5f = 0116
#st2f = 0009