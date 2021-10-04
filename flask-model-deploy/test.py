import requests

# localhost의 8888포트로 request를 보냅니다. 
# 이때 전달할 파일을 딕셔너리 형태로 위치를 전달합니다.
response = requests.post("http://35.222.99.236:9000/api", files={'file': open('aespa.png', 'rb')})

print(response.json())

# 다음과 같이 curl로 리눅스 cli에서 요청할 수도 있습니다.
# curl -X POST -F file=@aespa.png 'http://localhost:8080/api'