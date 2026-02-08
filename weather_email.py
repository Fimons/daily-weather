import os
import requests
import resend
import random

# ====== 1. 配置区（在 GitHub Secrets 中设置）======
RESEND_API_KEY = os.environ["RESEND_API_KEY"]
FROM_EMAIL = os.environ["FROM_EMAIL"]
TO_EMAIL = os.environ["TO_EMAIL"]

# 城市配置：上海 + 咸宁
CITIES = [
    {"name": "上海", "lat": 31.23, "lon": 121.47},
    {"name": "咸宁", "lat": 29.85, "lon": 114.32}
]

# ====== 2. 励志 & 爱情名言库 ======
QUOTES = [
    # === 温暖励志 ===
    "每一个清晨，都是你重新定义自己的机会。",
    "今天的你，比昨天更接近梦想。",
    "天气会变，但你的坚持不会。",
    "穿暖一点，心也要暖。世界值得你温柔以待。",
    "不是天气决定心情，而是你决定如何面对天气。",
    "冷一点没关系，热血的人从不惧寒冬。",
    "阳光总在风雨后，温暖总在寒潮后。",
    "好好穿衣，好好吃饭，好好爱自己。",
    "新的一天，愿你比昨天更勇敢一点。",
    "即使阴天，心里也可以阳光灿烂。",
    "你努力的样子，比今天的太阳还耀眼。",
    "慢慢来，比较快。今天也是进步的一天。",
    "生活不会辜负每一个认真对待它的人。",
    "微小的坚持，终将成就不凡的你。",

    # === 爱情 / 陪伴 / 温柔 ===
    "有人等你回家，是冬天最暖的事。",
    "最好的爱情，是彼此照亮，又各自发光。",
    "今天也要记得，有人正偷偷想着你。",
    "爱是：我知道外面很冷，但我的怀抱很暖。",
    "和喜欢的人一起看雪，连寒风都变得温柔。",
    "真正的浪漫，是每天清晨说‘早安’，夜晚道‘晚安’。",
    "你不需要完美，你只需要做你自己——就值得被爱。",
    "世界很大，但有人只为你留了一盏灯。",
    "爱不是轰轰烈烈，而是陪你吃早餐、看天气、过平凡日子。",
    "如果今天下雨，记得带伞；如果心里下雨，记得我在这里。",
    "你是我平凡日子里，最不平凡的期待。",
    "愿有人问你粥可温，有人与你立黄昏。",
    "爱是双向奔赴，也是互相提醒：今天降温，多穿点。",
    "在这个世界上，总有人觉得你比阳光还珍贵。",

    # === 轻哲理 / 生活感悟 ===
    "日子再忙，别忘了抬头看看天空。",
    "幸福，有时就是一件厚外套，和一个关心你的人。",
    "慢下来，感受风，感受光，感受此刻的自己。",
    "你值得被世界温柔以待，从今天开始相信这一点。"
]

# 天气代码转中文
def get_weather_desc(code):
    weather_map = {
        0: "晴", 1: "多云", 2: "部分多云", 3: "阴",
        45: "雾", 48: "冻雾",
        51: "小毛毛雨", 53: "中毛毛雨", 55: "大毛毛雨",
        61: "小雨", 63: "中雨", 65: "大雨",
        71: "小雪", 73: "中雪", 75: "大雪", 77: "冰粒",
        80: "阵雨", 81: "中阵雨", 82: "大阵雨",
        85: "阵雪", 86: "大阵雪",
        95: "雷阵雨", 96: "雷阵雨+冰雹", 99: "雷阵雨+大冰雹"
    }
    return weather_map.get(code, "未知")

# 获取单个城市天气
def fetch_weather(lat, lon, city_name):
    print(f"正在获取 {city_name} 天气数据...")
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&daily=weathercode,temperature_2m_max,temperature_2m_min,"
        f"apparent_temperature_max,apparent_temperature_min"
        f"&timezone=Asia/Shanghai"
    )
    resp = requests.get(url).json()
    
    today = resp['daily']['time'][0]
    max_temp = resp['daily']['temperature_2m_max'][0]
    min_temp = resp['daily']['temperature_2m_min'][0]
    max_feels = resp['daily']['apparent_temperature_max'][0]
    min_feels = resp['daily']['apparent_temperature_min'][0]
    weather_code = resp['daily']['weathercode'][0]
    weather_desc = get_weather_desc(weather_code)
    
    avg_feels = (min_feels + max_feels) / 2
    
    return {
        "name": city_name,
        "date": today,
        "weather": weather_desc,
        "min_temp": min_temp,
        "max_temp": max_temp,
        "min_feels": min_feels,
        "max_feels": max_feels,
        "avg_feels": avg_feels
    }

# 智能穿衣建议（基于平均体感温度）
def get_clothing_advice(avg_temp):
    if avg_temp < 0:
        return "极寒！厚羽绒服+围巾+手套+保暖裤，避免长时间外出。"
    elif avg_temp < 5:
        return "厚内衣 + 毛衣 + 羽绒服 + 加绒卫裤"
    elif avg_temp < 10:
        return "中暖内衣 + 毛衣 + 厚棉服 + 加绒卫裤"
    elif avg_temp < 15:
        return "薄内衣 + 毛衣 + 厚外套 + 运动裤"
    elif avg_temp < 20:
        return "T恤 + 卫衣 + 冲锋衣 + 运动裤"
    elif avg_temp < 25:
        return "T恤 + 薄长裤 或 薄裙"
    elif avg_temp < 30:
        return "短袖 + 短裤/裙子，注意防晒"
    else:
        return "高温！轻薄透气衣物，记得补水防中暑"

# ====== 3. 获取两地天气 ======
weathers = []
for city in CITIES:
    w = fetch_weather(city["lat"], city["lon"], city["name"])
    weathers.append(w)

# 使用第一个城市的日期作为标题（两地同一天）
today = weathers[0]["date"]

# ====== 4. 随机名言 + 固定结尾 ======
random_quote = random.choice(QUOTES)
fixed_end = "宝宝爱你~"

# ====== 5. 构建 HTML 邮件内容 ======
weather_blocks = ""
for w in weathers:
    clothing = get_clothing_advice(w["avg_feels"])
    weather_blocks += f"""
    <div style="padding: 16px; border-radius: 10px; margin-bottom: 20px;">
        <h3 style="margin-top: 0; color: #1a73e8;">📍 {w['name']}</h3>
        <p><strong>天气：</strong>{w['weather']}</p>
        <p><strong>气温：</strong>{w['min_temp']}°C ~ {w['max_temp']}°C</p>
        <p><strong>体感温度：</strong>{w['min_feels']:.1f}°C ~ {w['max_feels']:.1f}°C</p>
        
        <div style="background: #e6f0ff; padding: 10px; border-radius: 6px; margin-top: 10px; border-left: 3px solid #4285f4;">
            <strong>👕 穿衣建议：</strong>{clothing}
        </div>
    </div>
    """

# ====== 6. 发送邮件 ======
print("正在发送邮件...")
resend.api_key = RESEND_API_KEY

try:
    email = resend.Emails.send({
        "from": FROM_EMAIL,
        "to": TO_EMAIL,
        "subject": f"🌤️ {today} 天气预报 | 上海 & 咸宁",
        "html": f"""
        <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                    max-width: 650px; margin: 20px auto; padding: 20px; border-radius: 12px; 
                    line-height: 1.6; color: #333;">
            <h2 style="color: #1a73e8; text-align: center; margin-top: 0;">🌡️ {today} 天气预报</h2>
            
            {weather_blocks}

            <blockquote style="border-left: 4px solid #4CAF50; padding-left: 16px; 
                              margin: 24px 0; color: #555; font-style: italic; font-size: 1.05em; line-height: 1.5;">
                “{random_quote}”
            </blockquote>

            <p style="text-align: right; font-weight: bold; color: #e91e63; font-size: 1.1em;">
                {fixed_end}
            </p>

            <hr style="margin: 24px 0; border: 0; border-top: 1px solid #eee;">
            <p style="color: #888; font-size: 0.9em; text-align: center;">
                由 Resend 自动发送 · 数据来源：<a href="https://open-meteo.com/" style="color: #1a73e8; text-decoration: none;">Open-Meteo</a>
            </p>
        </div>
        """
    })
    print("✅ 邮件发送成功！ID:", email["id"])
except Exception as e:
    print("❌ 发送失败:", str(e))
