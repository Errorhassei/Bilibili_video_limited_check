import os
import requests
import json
import time
import datetime
from pathlib import Path


import colorama
 
colorama.init(autoreset=True)
#?bvid=BV1FA4y1Z7ZZ
GET_VIDEO_INFORMATION_URL = "https://api.bilibili.com/x/web-interface/archive/stat"
PAGE_LIST_URL = "https://api.bilibili.com/x/player/pagelist"
GET_NOW_WATCHING = "https://api.bilibili.com/x/player/online/total"

header={
	'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36'
}
last_view = 0
last_check_time = time.strftime("%a %b %d %H:%M:%S %Y",time.localtime())
dir = Path('/history')
if(dir.exists()==False): os.system('mkdir history')

print("enter the video's BVID:")
bvid = input()
i = datetime.datetime.now()
file = open('history/'+bvid+'-'+str(i.year)+'-'+str(i.month)+'-'+str(i.day)+'-'+str(i.hour)+'-'+str(i.minute)+'-'+str(i.second)+'.txt','w')


print("enter time interval(s):")
time_interval = input()

Re = requests.get(PAGE_LIST_URL , {
    "bvid" : bvid
}).json()
cid = Re['data'][0]['cid']
while True:
    Re = requests.get(GET_VIDEO_INFORMATION_URL,params={
        "bvid" : bvid,
        "jsonp": "jsonp"
    },headers=header).json()
    if(Re['data']['view'] < last_view) :
        file.write("Your videos has been limited!"+'\n')
        file.write(" Last check time : " + last_check_time +'\n' + "    Views : " + str(last_view) + '\n')
        print("\033[0;31;41mYour videos has been limited!\033[0m" + '\n')
        print(" Last check time : " + last_check_time +'\n' + "    Views : " + str(last_view) + '\n')
    last_check_time = time.strftime("%a %b %d %H:%M:%S %Y",time.localtime())
    print("\033[1;35m This check time : " + last_check_time +'\n' + "    Views : " + str(Re['data']['view']) +'\n')
    file.write("This check time : " + last_check_time +'\n' + "    Views : " + str(Re['data']['view']) +'\n')
    last_view = Re['data']['view']
    Re = requests.get(GET_NOW_WATCHING,{
        'cid' : cid ,
        'bvid' : bvid,
        "jsonp": "jsonp"
    }).json()
    print('\033[1;35m    Number of viewers now : ' + str(Re['data']['total']) + '\n')
    file.write("    Number of viewers now : "+ str(Re['data']['total']) + '\n')
    time.sleep(int(time_interval))
