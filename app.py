import os
import sys
import stat
import subprocess
import time
import urllib.request
from flask import Flask

# 1. 오픈나무 기본 변수 설정
os.environ["OPENNAMU_RUN_MODE"] = "server"
os.environ["OPENNAMU_SETUP_TOOL"] = "init"

# 2. Vercel(리눅스) 환경에 맞는 바이너리 다운로드 및 설정
binary_dir = os.path.join(os.getcwd(), "bin")
binary_path = os.path.join(binary_dir, "main.amd64")

if not os.path.exists(binary_dir):
    os.makedirs(binary_dir)

# 바이너리가 없으면 Vercel 서버 내부로 다운로드
if not os.path.exists(binary_path):
    print("Vercel Environment: Downloading Linux Binary...")
    url = "https://raw.githubusercontent.com/opennamu/opennamu/main/bin/main.amd64"
    try:
        urllib.request.urlretrieve(url, binary_path)
        # 리눅스에서 실행 가능하도록 권한 부여 (chmod +x)
        st = os.stat(binary_path)
        os.chmod(binary_path, st.st_mode | stat.S_IEXEC)
        print("Binary Download & Permission Fix Complete.")
    except Exception as e:
        print(f"Download Failed: {e}")

# 3. 백엔드 고랭(Golang) 프로세스 백그라운드 실행
try:
    print("Starting Background Golang Engine...")
    subprocess.Popen([binary_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2) # 엔진이 켜질 때까지 잠시 대기
except Exception as e:
    print(f"Failed to start Golang engine: {e}")

# 4. Vercel이 필수적으로 요구하는 최상위(Top-level) Flask 객체 선언
fast_app = Flask(__name__)

# 오픈나무 실제 코어 로직 임포트 (기존 오픈나무의 route 및 기능을 Flask에 연결)
try:
    # 오픈나무 패키지 경로 추가
    sys.path.append(os.getcwd())
    from route.tool.func import *
    # 오픈나무 내부 라우트 모듈들을 유연하게 불러옵니다.
    import route
except Exception as e:
    print(f"Core logic import warning: {e}")

# 5. Vercel 엔트리 포인트 강제 매핑 (이름 충돌 방지 및 치트키)
app = fast_app
application = fast_app
handler = fast_app

# Vercel 환경이 아닌 로컬에서 직접 켤 때를 위한 처리
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)