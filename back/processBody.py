from datetime import datetime, timedelta
from dateutil.parser import parse


def processBody(body):
    # date를 datetime형식으로 바꿔 줌
    for i in body:
        i['date'] = parse(i['date'])

    # date 기준 정렬
    body.sort(key=lambda b: b['date'])

    # 빈 데이터 날짜 사이값 직선 그래프 형태로 채우기
    i = 0
    while i < len(body)-1:
        print(i)
        x = (body[i+1]['date']-body[i]['date']).days
        y = (body[i+1]['value']-body[i]['value'])
        try:
            grad = y/x  # 데이터간의 기울기
        except:
            grad = 1
        idx = i
        for j in range(1, x):  # 빈공간 메꾸는 루프
            temp_date = body[i]['date']+timedelta(days=j)
            temp_data = body[i]['value']+grad*j
            body.insert(idx+1, {'date': temp_date, 'value': temp_data})
            idx = idx+1
        i = 1+idx
    return body
