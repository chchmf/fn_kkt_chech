import json
import asyncio
import aiohttp
import time

model_code = input("Введи код модели:")

start = time.time()

file = open("schedule.txt","r", encoding='utf-8')
list = []

for eachLine in file:
    a = eachLine.strip().split("\n")
    for i in range(len(a)):
        list.append(a[i].replace('"',''))

def gen(sn, model):
	for i in sn:
		yield  f"https://kkt-online.nalog.ru/lkip.html?query=/fn/model/check&factory_number={i}&model_code={model}", i

csv = open("list.csv","w")
csv.write("sn"+";"+"status"+"\n")

async def get_data(session, url, sn):
	async with session.get(url, ssl=False) as resp:
		resp_text = await resp.text()
		print(sn+";"+str(json.loads(resp_text)))
		json_text = json.loads(resp_text)
		if "error" in json_text:
			csv.write(sn+";"+str(json_text["error"])+"\n")
		elif json_text["check_status"] == 0:
			csv.write(sn+";"+str(json_text["check_result"])+"\n")
		else:
			csv.write(sn+";"+str("Готова к преключениям")+"\n")

async def checkfns():
	async with aiohttp.ClientSession() as session:
		tasks = []
		for i in gen(list, model_code):
			task = asyncio.create_task(get_data(session, i[0], i[1]))	
			tasks.append(task)
		await asyncio.gather(*tasks)

asyncio.run(checkfns())


csv.close()
stop = time.time() - start
input(f"Закончил за: {stop} секунд. Закрой меня...")

#st3f = 0080
#st5f = 0116
#st2f = 0009