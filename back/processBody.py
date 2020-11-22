from datetime import datetime
from dateutil.parser import parse
import statistics


def processBody(body):
    # 우선 data에 키 'value'가 없는 데이터를 찾음
    list = []
    checkValue = False
    for i in body['data']:
        if 'value' in i:
            list.append(i['value'])
        else:
            checkValue = True

    median = statistics.median(list)  # 값이 있는 데이터만으로 중간값 추출
    # 채워야할 데이터가 있을때만 실행하는 부분
    if checkValue:
        for idx, i in enumerate(body['data']):
            if 'value' not in i:
                body['data'][idx]['value'] = median

    # date 형식이 2020-01-01 형식을 기준으로 오름차순으로 정렬함
    body['data'] = sorted(
        body['data'], key=lambda t: datetime.strptime(t['date'], '%Y-%m-%d'))
    # 정렬된 데이터의 date를 datetime형식으로 바꿔 줌
    for i in range(len(body['data'])):
        body['data'][i]['date'] = parse(body['data'][i]['date'])
    # 정렬되고 date가 datetime 형식인 body로 return
    return body
