import os
import sys
import re
import werkzeug.routing

# 1. 경로 강제 추가 (최상단)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 2. Flask 객체 직접 생성 (에러 방지를 위해 먼저 선언)
from flask import Flask
app = Flask(__name__)
application = app # Vercel 핸들러 등록

# 3. OpenNamu 설정 및 라우트 로드
try:
    # DB 세팅을 건너뛰기 위해 환경변수 혹은 기본값 강제 주입
    if not os.path.exists('data.web.json'):
        with open('data.web.json', 'w') as f:
            f.write('{"type": "sqlite", "name": "data"}')

    # 필요한 모듈들을 불러오되, 오류가 나도 app은 유지되도록 처리
    from route.tool.func import *
    from route import *
    
    # 기존 OpenNamu의 app 설정들을 현재 app 객체에 덮어쓰기
    # (이미 생성된 app 객체에 라우팅 정보를 연결하는 과정)
    from route.tool.func import app as opennamu_app
    app = opennamu_app
    application = app
    
except Exception as e:
    print(f"OpenNamu Import Error (Ignored for Build): {e}")

# 4. 필수 컨버터 등록 (원본 코드 로직)
class EverythingConverter(werkzeug.routing.PathConverter):
    def __init__(self, map):
        super(EverythingConverter, self).__init__(map)
        self.regex = r'.*?'
    def to_python(self, value):
        return re.sub(r'^\\\.', '.', value)

class RegexConverter(werkzeug.routing.BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['everything'] = EverythingConverter
app.url_map.converters['regex'] = RegexConverter

# 5. Vercel 환경에서 필요한 최소 설정
app.config['JSON_AS_ASCII'] = False

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)