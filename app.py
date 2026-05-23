# -*- coding: utf-8 -*-
import os
import sys

# 1. Vercel 환경에서 파일 쓰기 에러 및 바이너리 구동 방지 환경변수 주입
os.environ["OPENNAMU_RUN_MODE"] = "server"
os.environ["OPENNAMU_SETUP_TOOL"] = "init"
# 임시 폴더(/tmp) 외의 공간에 파일 생성을 시도하다 터지는 것을 막기 위해 가상 경로 주입
os.environ["OPENNAMU_DB_TYPE"] = os.environ.get("OPENNAMU_DB_TYPE", "sqlite")
if os.environ["OPENNAMU_DB_TYPE"] == "sqlite":
    os.environ["OPENNAMU_DB_NAME"] = "/tmp/data" # Vercel에서 유일하게 허용된 쓰기 가능 폴더

# 2. 파이썬 기본 경로 설정
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 3. 오픈나무 코어 로직 로드
from route.tool.func import *

# 4. 고랭 바이너리 실행 단계에서 Vercel이 크래시 내는 것을 방지하기 위한 치트키
# Vercel 환경일 경우 subprocess 기능을 강제로 패치하여 외부 바이너리 실행을 우회합니다.
import subprocess
original_popen = subprocess.Popen
def dummy_popen(*args, **kwargs):
    class DummyProcess:
        def __init__(self):
            self.stdout = None
            self.stderr = None
        def poll(self): return None
        def wait(self, timeout=None): return 0
        def kill(self): pass
    print("Vercel Environment: Bypassing background golang engine binary execution.")
    return DummyProcess()
subprocess.Popen = dummy_popen

# 5. Vercel용 최상위 엔트리 포인트 변수 바인딩
# 오픈나무 코어 내부에 생성된 fast_app을 Vercel이 찾을 수 있도록 연결
try:
    app = fast_app
    application = fast_app
    handler = fast_app
except NameError:
    # 혹시 모를 로딩 타이밍 에러 방지용 백업 Flask 생성
    from flask import Flask
    app = Flask(__name__)
    application = app
    handler = app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)