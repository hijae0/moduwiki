from django.shortcuts import render
from . import util

# 홈 페이지: 모든 위키 목록을 보여줌
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# 상세 페이지: 특정 위키 내용을 보여줌
def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "요청하신 페이지가 존재하지 않습니다."
        })
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": content
    })