import requests

def sendLine(content):
    try:
        TARGET_URL = 'https://notify-api.line.me/api/notify'
        TOKEN = 'yDUSKahXXt8Jr63GJ2eVMtekTB05EChUrPIZwk6b3CY' #'odbC9PrCtew1vMLA5qKQVJ71MbH882u9F1yTAFxjWR6'

        response = requests.post(
            TARGET_URL,
            headers={
                'Authorization': 'Bearer ' + TOKEN
            },
            data={
                'message': str(3)+'안녕하세요. 헬로우라인모니터링 테스트입니다.' + content
            }
        )



    except Exception as ex:
        print(ex)

sendLine('\n good')
