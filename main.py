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
from typing import Dict
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
        tt = ''
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
            # {
            #     'roomId': 8,
            #     'year' : year,
            #     'month': month,
            # },
            {
                'roomId': 48,
                'year' : year,
                'month': month,
            },
            # {
            #     'roomId': 49,
            #     'year' : year,
            #     'month': month,
            # },
            # {
            #     'roomId': 47,
            #     'year' : year,
            #     'month': month,
            # }
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
                'info' : "본인포함 3~8인 이용가능.\n토요일 개방시간 : 10:00~16:00\n방학중  개방시간 : 10:00~16:00.\n일요일, 공휴일은  휴실\n※ 예약 후 미사용시 예약취소합니다. 위반시 예약자는 1개월간 예약할 수 없습니다.(예약시간 20분경과시 이용제한)"
            },
            {
                'roomId': 24,
                'name': '15 스터디룸 (4층)',
                'opentime': 10,
                'closetime': 21,
                'minuser': 3,
                'maxuser': 8,
                'info' : "본인포함 3~8인 이용가능.\n토요일 개방시간 : 10:00~16:00\n방학중  개방시간 : 10:00~16:00.\n일요일, 공휴일은  휴실\n※ 예약 후 미사용시 예약취소합니다. 위반시 예약자는 1개월간 예약할 수 없습니다.(예약시간 20분경과시 이용제한)"
            },
            {
                'roomId': 25,
                'name': '16 스터디룸 (4층)',
                'opentime': 10,
                'closetime': 21,
                'minuser': 3,
                'maxuser': 8,
                'info' : "본인포함 3~8인 이용가능.\n토요일 개방시간 : 10:00~16:00\n방학중  개방시간 : 10:00~16:00.\n일요일, 공휴일은  휴실\n※ 예약 후 미사용시 예약취소합니다. 위반시 예약자는 1개월간 예약할 수 없습니다.(예약시간 20분경과시 이용제한)"
            },
            {
                'roomId': 26,
                'name': '17 스터디룸 (4층)',
                'opentime': 10,
                'closetime': 21,
                'minuser': 3,
                'maxuser': 6,
                'info' : "본인포함 3~6인 이용가능.\n토요일 개방시간 : 10:00~16:00\n방학중  개방시간 : 10:00~16:00.\n일요일, 공휴일은  휴실\n※ 예약 후 미사용시 예약취소합니다. 위반시 예약자는 1개월간 예약할 수 없습니다.(예약시간 20분경과시 이용제한)"
            },
            {
                'roomId': 27,
                'name': '18 스터디룸 (4층)',
                'opentime': 10,
                'closetime': 21,
                'minuser': 3,
                'maxuser': 6,
                'info' : "본인포함 3~6인 이용가능.\n토요일 개방시간 : 10:00~16:00\n방학중  개방시간 : 10:00~16:00.\n일요일, 공휴일은  휴실\n※ 예약 후 미사용시 예약취소합니다. 위반시 예약자는 1개월간 예약할 수 없습니다.(예약시간 20분경과시 이용제한)"
            },
            {
                'roomId': 28,
                'name': '19 스터디룸 (4층)',
                'opentime': 10,
                'closetime': 21,
                'minuser': 3,
                'maxuser': 6,
                'info' : "본인포함 3~6인 이용가능.\n토요일 개방시간 : 10:00~16:00\n방학중  개방시간 : 10:00~16:00.\n일요일, 공휴일은  휴실\n※ 예약 후 미사용시 예약취소합니다. 위반시 예약자는 1개월간 예약할 수 없습니다.(예약시간 20분경과시 이용제한)"
            },
            {
                'roomId': 29,
                'name': '20 스터디룸 (4층)',
                'opentime': 10,
                'closetime': 21,
                'minuser': 3,
                'maxuser': 6,
                'info' : "본인포함 3~6인 이용가능.\n토요일 개방시간 : 10:00~16:00\n방학중  개방시간 : 10:00~16:00.\n일요일, 공휴일은  휴실\n※ 예약 후 미사용시 예약취소합니다. 위반시 예약자는 1개월간 예약할 수 없습니다.(예약시간 20분경과시 이용제한)"
            },
            {
                'roomId': 30,
                'name': '21 스터디룸 (4층)',
                'opentime': 10,
                'closetime': 21,
                'minuser': 3,
                'maxuser': 6,
                'info' : "본인포함 3~6인 이용가능.\n토요일 개방시간 : 10:00~16:00\n방학중  개방시간 : 10:00~16:00.\n일요일, 공휴일은  휴실\n※ 예약 후 미사용시 예약취소합니다. 위반시 예약자는 1개월간 예약할 수 없습니다.(예약시간 20분경과시 이용제한)"
            },
            {
                'roomId': 31,
                'name': '22 스터디룸 (4층)',
                'opentime': 10,
                'closetime': 21,
                'minuser': 3,
                'maxuser': 6,
                'info' : "본인포함 3~6인 이용가능.\n토요일 개방시간 : 10:00~16:00\n방학중  개방시간 : 10:00~16:00.\n일요일, 공휴일은  휴실\n※ 예약 후 미사용시 예약취소합니다. 위반시 예약자는 1개월간 예약할 수 없습니다.(예약시간 20분경과시 이용제한)"
            },
            {
                'roomId': 32,
                'name': '23 스터디룸 (4층)',
                'opentime': 10,
                'closetime': 21,
                'minuser': 3,
                'maxuser': 8,
                'info' : "본인포함 3~6인 이용가능.\n토요일 개방시간 : 10:00~16:00\n방학중  개방시간 : 10:00~16:00.\n일요일, 공휴일은  휴실\n※ 예약 후 미사용시 예약취소합니다. 위반시 예약자는 1개월간 예약할 수 없습니다.(예약시간 20분경과시 이용제한)"
            },
            {
                'roomId': 33,
                'name': '24 스터디룸 (4층) 당일예약',
                'opentime': 10,
                'closetime': 21,
                'minuser': 3,
                'maxuser': 8,
                'info' : "본인포함 3~6인 이용가능.\n토요일 개방시간 : 10:00~16:00\n방학중  개방시간 : 10:00~16:00.\n일요일, 공휴일은  휴실\n※ 예약 후 미사용시 예약취소합니다. 위반시 예약자는 1개월간 예약할 수 없습니다.(예약시간 20분경과시 이용제한)"
            },
            # {
            #     'roomId': 8,
            #     'name': '교육실 (2층)',
            #     'opentime': 10,
            #     'closetime': 17,
            #     'minuser': 2,
            #     'maxuser': 25,
            # },
            {
                'roomId': 48,
                'name': '대양 AI 콜라보랩 Talk Room3',
                'opentime': 10,
                'closetime': 16,
                'minuser': 2,
                'maxuser': 4,
                'info' : '■ 이용 가능 인원\n- 본인 포함 2~4인\n■ 이용 가능 시간\n- 평일(월~금) 10:00~12:00, 13:00~17:00 (※ 점심시간 12:00~13:00 이용불가)\n- 휴일(토~일), 공휴일 이용불가\n※ 소프트웨어, AI 관련 교육 및 행사시 사용 제한\n(관련하여 예약가능일을 임의 조정할 수 있음)\n■ 이용 문의 \n- Tel. 02-6935-2697\n■ 주의사항\n- 예약 후 미사용시 예약취소, 위반시 예약자는 1개월간 예약 불가 \n※ 예약시간 20분 경과시 이용제한 \n- 금지사항 : 식음료 반입, 실내 소음 유발, 마스크 미착용 및 불량착용 \n※ 미준수시 즉시 퇴실 조치 및 이후 이용제한'
            },
            # {
            #     'roomId': 49,
            #     'name': '대양 AI 콜라보랩 라운지A',
            #     'opentime': 10,
            #     'closetime': 16,
            #     'minuser': 2,
            #     'maxuser': 4,
            # },
            # {
            #     'roomId': 47,
            #     'name': '대양 AI 콜라보랩 라운지A',
            #     'opentime': 10,
            #     'closetime': 16,
            #     'minuser': 2,
            #     'maxuser': 4,
            # }
            ]
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


@app.get("/Remove/{id}/{password}/{cancelMsg}/{bookingId}")
def Remove(id, password,cancelMsg, bookingId):
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
        'mode': 'update',
        'classId': '0'
    }
    booking_url = "https://library.sejong.ac.kr/studyroom/BookingProcess.axa"
    r = session.post(booking_url, data = remove_data,verify=False)
    return {"result" : "취소 완료"}

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
    kk = r.headers['X-JSON'][25:31]
    return kk


@app.get("/Ipid/{id}/{password}")
def Ipid(id,password):
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
    r = session.post("https://library.sejong.ac.kr/studyroom/Request.ax?roomId=23")
    soup = BeautifulSoup(r.text, "html.parser")
    a = soup.select_one('#ipid')
    return a['value']



class Data(BaseModel):
    year : str
    month : str
    day : str
    startHour : str
    closeTime : str
    hours : str
    purpose : str
    ipid : str
    ipid1 : Union[str, None] = None
    ipid2 : Union[str, None] = None
    ipid3 : Union[str, None] = None
    ipid4 : Union[str, None] = None
    ipid5 : Union[str, None] = None
    ipid6 : Union[str, None] = None
    ipid7 : Union[str, None] = None
    idx : str
    roomId : str

class Result(BaseModel):
    result :str

@app.post("/Reservation/{id}/{password}",response_model=Dict[str, str])
def Reservation(id : str,password : str,data: Data):
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
        'year' : data.year,
        'month' : data.month,
        'day' : data.day,
        'startHour' : data.startHour,
        'closeTime' : data.closeTime,
        'hours' : data.hours,
        'purpose' : data.purpose,
        'mode' : 'INSERT',
        'idx' : data.idx,
        'ipid' : data.ipid,
        'roomId' : data.roomId
    }
    if data.ipid1:
        booking_data["ipid1"] = data.ipid1
    if data.ipid2:
        booking_data["ipid2"] = data.ipid2
    if data.ipid3:
        booking_data["ipid3"] = data.ipid3
    if data.ipid4:
        booking_data["ipid4"] = data.ipid4
    if data.ipid5:
        booking_data["ipid5"] = data.ipid5
    if data.ipid6:
        booking_data["ipid6"] = data.ipid6
    if data.ipid7:
        booking_data["ipid7"] = data.ipid7

    booking_url = "https://library.sejong.ac.kr/studyroom/BookingProcess.axa"
    rrr = session.post(booking_url, data = booking_data,verify=False)
    if rrr.text == '':
        result = '예약 완료'
    else:
        result = rrr.text
        result = result[2:]
    return {'result' : result}
@app.get("/booktime/{roomId}/{year}/{month}/{day}")
def booktime(roomId,year,month,day):
    session = requests.session()
    url = "https://library.sejong.ac.kr/studyroom/BookingTime.axa"
    data ={
    "roomId" : roomId,
    "year" : year,
    "month" : month,
    "day" : day
    }
    r = session.post(url,data=data,verify=False)
    soup = BeautifulSoup(r.text, "html.parser")
    a = soup.select_one('#startHour')
    b = a.find_all('option')
    result = []
    for i in b:
        result.append(i['value'])
    return result

@app.get("/accompany/{id}/{password}/{bookingId}")
def accompany(id, password,bookingId):
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
    url = "https://library.sejong.ac.kr/studyroom/BookingDetail.axa"

    ipid = Ipid(id,password)
    data = {
    "bookingId" : bookingId,
    "ipid" : ipid,
    }
    r = session.post(url, data,verify=False)
    soup = BeautifulSoup(r.text, "html.parser")
    tablelist = soup.find_all('table')
    datatable = tablelist[2]
    p = parser.make2d(datatable)
    a = p[4][1]
    a = a.replace('\t','')
    a = a.replace('\r','')
    a = a.replace(' ','')
    a = a.replace('\xa0','')
    b = list(a.split('\n'))
    return(b)


# uvicorn main:app --reload
# http://52.79.223.149
# http://52.79.223.149/docs
#python3 -m uvicorn main:app

