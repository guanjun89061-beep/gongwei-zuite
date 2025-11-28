# 嘴替 · Zuiti

👄 一个帮你骂老板、骂甲方、骂同事的 AI 职场吐槽搭子。

- 后端：Flask + OpenAI API
- 前端：简单 Web 页面
- App：用 Expo + React Native 做一个 WebView 壳，打开线上页面

## 本地运行（后端）

```bash
git clone https://github.com/guanjun89061-beep/gongwei-zuite.git
cd gongwei-zuite
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
set OPENAI_API_KEY=你的key
python app.py
