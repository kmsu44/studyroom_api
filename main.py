from html_table_parser import parser_functions as parser
import urllib
import requests
from bs4 import BeautifulSoup
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union
from datetime import datetime, date
import json
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


# uvicorn main:app --reload
#http://52.78.105.103
#http://52.78.105.103/docs
#python3 -m uvicorn main:app

