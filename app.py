# -*- coding: utf-8 -*-
import os
import sys

# 1. Vercel 환경인지 확인하고 실행 모드 고정
os.environ["OPENNAMU_RUN_MODE"] = "server"
os.environ["OPENNAMU_SETUP_TOOL"] = "init"

# 2. 파이썬 기본 경로 세팅 (오픈나무 모듈 인식용)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 3. [핵심] 오픈나무 순정 로직 그대로 가져와서 실행하기
# 오픈나무 공식 버전은 load_app_core() 내부에서 Flask 객체(fast_app)를 생성합니다.
from route.tool.func import *

# 4. Vercel이 찾을 수 있도록 최상위 레벨에 변수 강제 매핑
# 순정 오픈나무의 Flask 변수명인 fast_app을 Vercel 전용 이름인 app으로 연결합니다.
app = fast_app
application = fast_app
handler = fast_app

# 로컬 테스트용 (Vercel에서는 무시됨)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)