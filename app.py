import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

from openai import OpenAI

# 加载 .env 文件中的环境变量（本地开发用）
load_dotenv()

# 从环境变量读取 OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("请在 .env 中设置 OPENAI_API_KEY=你的key（线上用环境变量配置）")

client = OpenAI(api_key=OPENAI_API_KEY)

app = Flask(__name__)
CORS(app)  # 简单粗暴：允许所有来源访问，方便前端调用

# ====== 前端页面路由 ======
@app.route("/")
def serve_index():
    # 假设 index.html 和 app.py 在同一目录
    return send_from_directory(".", "index.html")


# ====== 职场吐槽搭子的人设 ======
BASE_SYSTEM_PROMPT = """
你是一个“职场吐槽搭子”，人设是：
- 职场老油条 + 毒舌闺蜜 + 搞事同事
- 永远站在用户一边，替用户说狠话、嘴上帮用户出气
- 风格：犀利、阴阳怪气、懂梗、会吐槽，偏口语
- 你可以辛辣、讽刺、吐槽、发疯式抱怨，但不要使用脏话，不要人身威胁

【重要安全边界】
- 可以骂/怼/吐槽“老板、甲方、领导、同事、客户”等职场角色和行为
- 不允许出现种族、性别、宗教、国籍等歧视性内容
- 不使用辱骂少数群体、侮辱外貌、身体残障等内容
- 不使用具体侮辱性词汇和脏话，可以用“傻得离谱”“脑子进水”“离谱得想报警”等委婉表达
- 不煽动现实暴力、不教别人伤害自己或他人

【语气风格】
- 可以用：哈？啧？绝了？离谱！之类的语气词
- 可以轻微网络用语和梗，但保持可读性
- 长度适中：一般 3~8 句为主，可分段

【输出格式】
- 只输出内容本身，不要解释自己在做什么
- 可以用一两段文字表达吐槽 + 站队 + 安慰
"""


def build_style_prompt(style: str) -> str:
    style = (style or "").lower()

    if style == "reply":
        return """
当前任务：帮用户生成一条“高情商回怼”话术。
要求：
- 表面礼貌、专业，字里行间带刺
- 读起来“好像没骂人”，但对方看完会有点难受
- 适合发在：工作群 / 邮件 / 私信中
"""
    elif style == "resign":
        return """
当前任务：帮用户生成一段“辞职幻想”文案。
要求：
- 用户不一定真的要发出去，重点是写着爽
- 可以走高冷、不屑、云淡风轻的路线，也可以稍微文学一点
- 不要出现真实公司名和真实隐私信息（用“贵司”“这家公司”“这位领导”等代替）
"""
    else:  # 默认 rant
        return """
当前任务：帮用户生成一段“发疯式吐槽”/“情绪宣泄”文本。
要求：
- 站在用户这边，帮用户一起骂、一起吐槽
- 可以阴阳怪气、夸张一点，让用户看了觉得爽
- 不要鼓励违法行为，不要鼓励现实暴力
"""


@app.route("/api/rant", methods=["POST"])
def generate_rant():
    data = request.get_json(force=True, silent=True) or {}

    scenario = data.get("scenario", "").strip()
    target = data.get("target", "").strip()
    style = data.get("style", "rant").strip()
    language = (data.get("language", "zh") or "zh").lower()

    if not scenario:
        return jsonify({"error": "scenario 不能为空"}), 400

    user_prompt_parts = []

    if language.startswith("zh"):
        user_prompt_parts.append("请用中文回答。")
    elif language.startswith("en"):
        user_prompt_parts.append("Please answer in English.")
    else:
        user_prompt_parts.append("请使用用户最容易理解的语言回答，一般用中文。")

    user_prompt_parts.append("下面是用户的吐槽场景：")
    user_prompt_parts.append(scenario)

    if target:
        user_prompt_parts.append(f"用户吐槽的对象（大概身份）：{target}")

    user_prompt_parts.append("请根据上面的情境，生成一段符合设定的内容。")

    style_prompt = build_style_prompt(style)

    try:
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": BASE_SYSTEM_PROMPT + "\n" + style_prompt,
                },
                {
                    "role": "user",
                    "content": "\n".join(user_prompt_parts),
                },
            ],
            temperature=0.9,
            max_tokens=512,
        )

        text = completion.choices[0].message.content.strip()

        return jsonify({
            "success": True,
            "data": {
                "scenario": scenario,
                "target": target,
                "style": style,
                "language": language,
                "reply": text,
            }
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
        }), 500


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
