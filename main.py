from html_table_parser import parser_functions as parser
import urllib
import requests
from bs4 import BeautifulSoup
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union
from datetime import datetime, date
import ssl
from concurrent.futures import ThreadPoolExecutor
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
app = FastAPI()

# 로그인
@app.get("/login/{id}/{password}")
def Login(id,password):
  session = requests.session()
  login = "https://portal.sejong.ac.kr/jsp/login/login_action.jsp"

  my={
      'mainLogin': 'Y',
      'rtUrl': 'blackboard.sejong.ac.kr',
      'id': id,
      'password': password,
  }
  header={
      "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
      "Referer" : "https://portal.sejong.ac.kr"
      }
  
  r = session.post(url = login, data=my, headers=header, timeout = 3, verify =False)
  
  if 'ssotoken' in r.headers.get('Set-Cookie', ''):
    return {"result" : "1" }
  else:
    return {"result" : "0" }
#예약 리스트
@app.get("/checklist/{id}/{password}")
def Checklist(id,password):
  session = requests.session()
  login = "https://portal.sejong.ac.kr/jsp/login/login_action.jsp"

  my={
      'mainLogin': 'Y',
      'rtUrl': 'blackboard.sejong.ac.kr',
      'id': id,
      'password': password,
  }
  header={
      "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
      "Referer" : "https://portal.sejong.ac.kr"
      }
  r = session.post(url = login, data=my, headers=header, timeout = 3,verify =False)
  url = "http://library.sejong.ac.kr/sso/Login.ax"
  r = session.post(url,verify=False)


  # 파싱
  url = "https://library.sejong.ac.kr/studyroom/List.axa"
  r = session.post(url, verify=False)
  soup = BeautifulSoup(r.text, "html.parser")
  tmp = soup.find_all('tbody')
  tmp = tmp[1]
  url = tmp.find_all('a')
  script = []
  for i in url:
      if 'javascript:studyroom.goStudyRoomBookingDetail' in i['href']:
          script.append(i['href'])
  studyroom_id = []
  for i in script:
      t = ''
      for j in i[47:]:
          if j == "'":
              break
          t += j
      studyroom_id.append(t)
  p = parser.make2d(tmp)
  result = []
  for idx, data in enumerate(p):
      room = {}
      room["title"] = data[0]
      date = data[1][0:10]
      datetime_date = datetime.strptime(date,'%Y/%m/%d')
      day = datetime_date.weekday()
      month = datetime_date.month
      datee = datetime_date.day
      room["month"] = month
      room["datee"] = datee
      room["day"] = day 
      
      room["starttime"] = data[1][11:13]
      time = data[1][20]
      room["endtime"] = int(data[1][11:13]) + int(time)
      room["number"] = data[2]
      room["roomid"] = studyroom_id[idx]
      result.append(room)
  return result

@app.get("/table/{id}/{password}")
def table(id,password):
    session = requests.session()
    login = "https://portal.sejong.ac.kr/jsp/login/login_action.jsp"

    my={
        'mainLogin': 'Y',
        'rtUrl': 'blackboard.sejong.ac.kr',
        'id': id,
        'password': password,
    }
    header={
        "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        "Referer" : "https://portal.sejong.ac.kr"
        }
    r = session.post(url = login, data=my, headers=header, timeout = 3)
    url = "http://library.sejong.ac.kr/sso/Login.ax"
    r = session.post(url,verify=False)



    roomdata =[
        {
            'roomId': 23,
        },
        {
            'roomId': 24,
        },
        {
            'roomId': 25,
        },
        {
            'roomId': 26,
        },
        {
            'roomId': 27,
        },
        {
            'roomId': 28,
        },
        {
            'roomId': 29,
        },
        {
            'roomId': 30,
        },
        {
            'roomId': 31,
        },
        {
            'roomId': 32,
        },
        {
            'roomId': 33,
        },
        {
            'roomId': 8,
        },
        {
            'roomId': 48,
        },
        {
            'roomId': 49,
        },
        {
            'roomId': 47,
        }
    ]

# 테이블 정보 가져오기
    def gettable(args):
        print('시작')
        a = session.post(args[0], data = args[1] , verify=False)
        print('종료')
        return a
    url = "https://library.sejong.ac.kr/studyroom/BookingTable.axa"
    list_of_urls = []
    for room in roomdata:
        list_of_urls.append((url,room)) 
    with ThreadPoolExecutor(max_workers=10) as pool:
        response_list = list(pool.map(gettable,list_of_urls))


    result = [
        {
            'roomId': 23,
            'name': '14 스터디룸 (4층)',
            'opentime': 10,
            'closetime': 21,
            'minuser': 3,
            'maxuser': 8,
        },
        {
            'roomId': 24,
            'name': '15 스터디룸 (4층)',
            'opentime': 10,
            'closetime': 21,
            'minuser': 3,
            'maxuser': 8,
        },
        {
            'roomId': 25,
            'name': '16 스터디룸 (4층)',
            'opentime': 10,
            'closetime': 21,
            'minuser': 3,
            'maxuser': 8,
        },
        {
            'roomId': 26,
            'name': '17 스터디룸 (4층)',
            'opentime': 10,
            'closetime': 21,
            'minuser': 3,
            'maxuser': 8,
        },
        {
            'roomId': 27,
            'name': '18 스터디룸 (4층)',
            'opentime': 10,
            'closetime': 21,
            'minuser': 3,
            'maxuser': 8,
        },
        {
            'roomId': 28,
            'name': '19 스터디룸 (4층)',
            'opentime': 10,
            'closetime': 21,
            'minuser': 3,
            'maxuser': 8,
        },
        {
            'roomId': 29,
            'name': '20 스터디룸 (4층)',
            'opentime': 10,
            'closetime': 21,
            'minuser': 3,
            'maxuser': 8,
        },
        {
            'roomId': 30,
            'name': '21 스터디룸 (4층)',
            'opentime': 10,
            'closetime': 21,
            'minuser': 3,
            'maxuser': 8,
        },
        {
            'roomId': 31,
            'name': '22 스터디룸 (4층)',
            'opentime': 10,
            'closetime': 21,
            'minuser': 3,
            'maxuser': 8,
        },
        {
            'roomId': 32,
            'name': '23 스터디룸 (4층)',
            'opentime': 10,
            'closetime': 21,
            'minuser': 3,
            'maxuser': 8,
        },
        {
            'roomId': 33,
            'name': '24 스터디룸 (4층)',
            'opentime': 10,
            'closetime': 21,
            'minuser': 3,
            'maxuser': 8,
        },
        {
            'roomId': 8,
            'name': '교육실 (2층)',
            'opentime': 10,
            'closetime': 17,
            'minuser': 2,
            'maxuser': 25,
        },
        {
            'roomId': 48,
            'name': '대양 AI 콜라보랩 Talk Room3',
            'opentime': 10,
            'closetime': 16,
            'minuser': 2,
            'maxuser': 4,
        },
        {
            'roomId': 49,
            'name': '대양 AI 콜라보랩 라운지A',
            'opentime': 10,
            'closetime': 16,
            'minuser': 2,
            'maxuser': 4,
        },
        {
            'roomId': 47,
            'name': '대양 AI 콜라보랩 라운지A',
            'opentime': 10,
            'closetime': 16,
            'minuser': 2,
            'maxuser': 4,
        }]
    for idx,data in enumerate(response_list):
        soup = BeautifulSoup(data.text, "html.parser")
        table_html = soup.find_all('table')
        table_arry = pd.read_html(str(table_html))
        table = table_arry[1]
        table = table.drop(0,axis = 1)
        a = len(table.index)
        tmp =[]
        for i in range(a):
            tmp.append(table.iloc[i].to_list())
        result[idx]["timetable"] = tmp;
        
    return result




# uvicorn main:app --reload
# http://52.79.223.149
# http://52.79.223.149/docs
#python3 -m uvicorn main:app

