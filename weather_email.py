import os #
import requests
import resend

# ====== 1. 配置区（这里填你的信息）======
RESEND_API_KEY = os.environ["RESEND_API_KEY"]
FROM_EMAIL = os.environ["FROM_EMAIL"]
TO_EMAIL = os.environ["TO_EMAIL"]

# 设置你所在城市的经纬度（示例：北京）
LAT = 31.23
LON = 121.47
# 其他城市参考：
# 上海: LAT=31.23, LON=121.47
# 广州: LAT=23.13, LON=113.26
# 深圳: LAT=22.55, LON=114.05
# 成都: LAT=30.57, LON=104.06

# ====== 2. 获取天气数据 ======
print("正在获取天气数据...")
url = (
    f"https://api.open-meteo.com/v1/forecast"
    f"?latitude={LAT}&longitude={LON}"
    f"&daily=weathercode,temperature_2m_max,temperature_2m_min"
    f"&timezone=Asia/Shanghai"
)
resp = requests.get(url).json()

# 提取今天的数据
today = resp['daily']['time'][0]
max_temp = resp['daily']['temperature_2m_max'][0]
min_temp = resp['daily']['temperature_2m_min'][0]
weather_code = resp['daily']['weathercode'][0]

# 天气代码转中文
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
weather_desc = weather_map.get(weather_code, "未知")

print(f"今日天气: {weather_desc}, {min_temp}°C ～ {max_temp}°C")

# ====== 3. 发送邮件 ======
print("正在发送邮件...")
resend.api_key = RESEND_API_KEY

try:
    email = resend.Emails.send({
        "from": FROM_EMAIL,
        "to": TO_EMAIL,
        "subject": f"🌤️ {today} 天气预报 | {weather_desc}",
        "html": f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 20px auto;">
            <h2>🌤️ {today} 天气预报</h2>
            <p><strong>天气：</strong>{weather_desc}</p>
            <p><strong>最高温度：</strong>{max_temp}°C</p>
            <p><strong>最低温度：</strong>{min_temp}°C</p>
            <hr>
            <p><small>由 Resend 自动发送 · 数据来源：<a href="https://open-meteo.com/">Open-Meteo</a></small></p>
        </div>
        """
    })
    print("✅ 邮件发送成功！ID:", email["id"])
except Exception as e:
    print("❌ 发送失败:", str(e))
