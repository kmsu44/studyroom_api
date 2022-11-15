from html_table_parser import parser_functions as parser
import requests
from bs4 import BeautifulSoup
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union
from datetime import datetime, date
import asyncio
import aiohttp
from timeit import default_timer as dt
import time
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
from timeit import default_timer as dt
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
  if p[0][2] != '* 예약내역이 없습니다.':
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
        room["bookingId"] = studyroom_id[idx]
        result.append(room)

  return result

@app.get("/Table/{year}/{month}")
def Table(year,month):
    start = time.time()
    url = "https://library.sejong.ac.kr/studyroom/BookingTable.axa"
    roomdata =[
            {
                'roomId': 23,
                'year' : year,
                'month': month,
            },
            {
                'roomId': 24,
                'year' : year,
                'month': month,
            },
            {
                'roomId': 25,
                'year' : year,
                'month': month,
            },
            {
                'roomId': 26,
                'year' : year,
                'month': month,
            },
            {
                'roomId': 27,
                'year' : year,
                'month': month,
            },
            {
                'roomId': 28,
                'year' : year,
                'month': month,
            },
            {
                'roomId': 29,
                'year' : year,
                'month': month,
            },
            {
                'roomId': 30,
                'year' : year,
                'month': month,
            },
            {
                'roomId': 31,
                'year' : year,
                'month': month,
            },
            {
                'roomId': 32,
                'year' : year,
                'month': month,
            },
            {
                'roomId': 33,
                'year' : year,
                'month': month,
            },
            {
                'roomId': 8,
                'year' : year,
                'month': month,
            },
            {
                'roomId': 48,
                'year' : year,
                'month': month,
            },
            {
                'roomId': 49,
                'year' : year,
                'month': month,
            },
            {
                'roomId': 47,
                'year' : year,
                'month': month,
            }
        ]
    data = []
    async def get_html(idx,room):
        async with aiohttp.ClientSession() as session:
            async with session.post(url,data = room, ssl = False) as response:
                data.append((idx,await response.text()))


    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(
        asyncio.gather(
            *(get_html(idx,room) for idx,room in enumerate(roomdata))
        )
    )
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
    for idx,data in enumerate(data):
            k, d = data
            html = ' '.join(d.split())
            soup = BeautifulSoup(html, "html.parser")
            table_html = soup.find_all('table')
            table_arry = pd.read_html(str(table_html))
            table = table_arry[1]
            table = table.drop(0,axis = 1)
            a = len(table.index)
            tmp =[]
            for i in range(a):
                tmp.append(table.iloc[i].to_list())
            result[k]["timetable"] = tmp;

    end = time.time()
    print(end-start)
    return result


@app.get("/Remove/{id}/{password}/{roomId}/{cancelMsg}/{bookingId}")
def Remove(id, password, roomId, cancelMsg, bookingId):
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
    
    #실행
    remove_data = {
        'cancelMsg': cancelMsg,
        'bookingId': bookingId,
        'expired': 'C',
        'roomId': roomId,
        'mode': 'update',
        'classId': '0'
    }
    booking_url = "https://library.sejong.ac.kr/studyroom/BookingProcess.axa"
    r = session.post(booking_url, data = remove_data,verify=False)
    return {"result" : "몰라용"}

@app.get("/UserFind/{id}/{password}/{sid}/{name}/{year}/{month}/{datee}")
def UserFind(id,password,sid,name,year,month,datee):
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


    # 파싱
    url = "https://library.sejong.ac.kr/studyroom/UserFind.axa"
    data = {
    'altPid' : sid,
    'name': name,
    'userBlockUser' : "Y",
    'year': year,
    'month' : month,
    'day' : datee
    }
    r = session.post(url, data =data, verify=False)
    return r.headers['X-JSON']

@app.get("/Reservation/{id}/{password}/{year}/{month}/{datee}/{startHour}/{hour}/{purpose}/{maxuser}/{roomId}/{ipid0}/{ipid1}/{ipid2}")
def Reservation(id, password, year, month, datee,startHour, hour, purpose,maxuser,roomId,ipid0,ipid1,ipid2):
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
    # 파싱
    booking_data = {
        'year' : year,
        'month' : month,
        'day' : datee,
        'startHour' : startHour,
        'closeTime' : startHour,
        'hours' : hour,
        'purpose' : purpose,
        'ipid1' : ipid1,
        'ipid2' : ipid2,
        'mode' : 'INSERT',
        'idx' : maxuser,
        'ipid' : ipid0,
        'roomId' : roomId
    }
    booking_url = "https://library.sejong.ac.kr/studyroom/BookingProcess.axa"
    rrr = session.post(booking_url, data = booking_data,verify=False)
    return {"result" : rrr.text}

@app.get("/test")
def test():
    result = {}
    result[1] = 1
    result[2] = 2
    return result
# @app.get("/Reservation")
# def Reservation():

# uvicorn main:app --reload
# http://52.79.223.149
# http://52.79.223.149/docs
#python3 -m uvicorn main:app

