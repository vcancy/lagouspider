# coding=gbk
import requests
from pymongo import MongoClient

companys = []

fn = 1
totalCount = 1
url ='https://www.lagou.com/jobs/positionAjax.json?city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false'
headers ={
'Accept':'application/json, text/javascript, */*; q=0.01',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
'Connection':'keep-alive',
'Content-Length':'26',
'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
'Cookie':'user_trace_token=20170615211203-1f3ab3b8d2794b6dbd620f9d54c69e9e; LGUID=20170615211203-398d65d4-51cc-11e7-9c5e-5254005c3644; JSESSIONID=ABAAABAACDBAAIAAEBE8FE6335339D0654450A9EE74BC55; _putrc=793FFDF4BF0180D1; login=true; unick=%E4%BF%9E%E6%9D%B0; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=3; TG-TRACK-CODE=index_navigation; SEARCH_ID=1e0dbc7106554f28b70583651d23fba2; index_location_city=%E5%8C%97%E4%BA%AC; _gid=GA1.2.881407919.1500860630; _gat=1; _ga=GA1.2.334214877.1497532334; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1500258068,1500860631,1500886703,1500900445; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1500903407; LGSID=20170724204712-367c0dc9-706e-11e7-b00b-525400f775ce; LGRID=20170724213633-1bd29411-7075-11e7-b072-525400f775ce',
'Host':'www.lagou.com',
'Origin':'https://www.lagou.com',
'Referer':"https://www.lagou.com/jobs/list_Python?city=%E5%8C%97%E4%BA%AC&cl=false&fromSearch=true&labelWords=&suginput=",
'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
'X-Anit-Forge-Code':'0',
'X-Anit-Forge-Token':'None',
'X-Requested-With':'XMLHttpRequest'
}
session = requests.session()
client = MongoClient()
db = client.lagou
while fn<=1:
    print('开始处理第{}页'.format(fn))
    data = 'first=false&pn={}&kd=Python'.format(fn)
    response = session.request(url=url, method='post', data=data, headers=headers)
    pagedata = response.json()
    print(pagedata)
    if pagedata.get('code') == 0:
        data = pagedata.get('content').get('positionResult').get('result')
        totalCount = pagedata.get('content').get('positionResult').get('totalCount')
        totalCount = totalCount/15+1 if totalCount%15>0 else totalCount/15 #最大显示30页
        fn +=1
        companys.extend(data)

inserts = []
for doc in companys:
    companyShortName = doc.get('companyShortName')
    if db.lagou.find_one({'companyShortName':companyShortName})==None:
        inserts.append(doc)
    else:print('重复记录:{}'.format(companyShortName))

if len(inserts)>0:
    db.lagou.insert(inserts)