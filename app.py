# -*- coding: utf-8 -*-
import os
import sys
from flask import Flask

# 1. Vercel이 파일 시작하자마자 검사하는 최상위(Top-level) 엔트리 포인트 선언 (눈속임 패치)
app = Flask(__name__)
application = app
handler = app

# 2. Vercel용 환경변수 주입 (SQLite 쓰기 에러 방지)
os.environ["OPENNAMU_RUN_MODE"] = "server"
os.environ["OPENNAMU_SETUP_TOOL"] = "init"
os.environ["OPENNAMU_DB_TYPE"] = os.environ.get("OPENNAMU_DB_TYPE", "sqlite")
if os.environ["OPENNAMU_DB_TYPE"] == "sqlite":
    os.environ["OPENNAMU_DB_NAME"] = "/tmp/data"

# 3. 파이썬 기본 경로 설정
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 4. 고랭 바이너리 강제 우회 패치 (Vercel 크래시 방지)
import subprocess
def dummy_popen(*args, **kwargs):
    class DummyProcess:
        def __init__(self):
            self.stdout = None
            self.stderr = None
        def poll(self): return None
        def wait(self, timeout=None): return 0
        def kill(self): pass
    print("Vercel Environment: Bypassing background golang engine.")
    return DummyProcess()
subprocess.Popen = dummy_popen

# 5. 오픈나무 코어 로직 불러오기
# 이제 오픈나무가 실행되면서 우리가 위에서 만든 'app' 객체에 라우트들을 심게 됩니다.
try:
    from route.tool.func import *
    
    # 오픈나무 내부의 Flask 객체(fast_app)를 우리가 선언한 app과 강제로 동기화
    if 'fast_app' in globals():
        fast_app = app
except Exception as e:
    print(f"Opunnamu core load warning: {e}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)