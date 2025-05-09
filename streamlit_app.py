import streamlit as st
import requests
from datetime import datetime, timedelta, timezone
import calendar
import pandas as pd

st.title("🎫 한화 직링 생성기")
st.markdown("""
> 🙏 제발 티켓팅 좀 성공하자 **by 1004**  
> ⚠️ **주의:** 예매 시작 시간인 **11시 정각**에 입장할 것!
""")

# 고정값
team_id = "63"
category_id = "137"
KST = timezone(timedelta(hours=9))

# 오늘 기준 이번달 계산
today = datetime.now(KST)
year, month = today.year, today.month
start_date = f"{year}{month:02d}01"
last_day = calendar.monthrange(year, month)[1]
end_date = f"{year}{month:02d}{last_day:02d}"

# 경기 정보 불러오기
url = f"https://mapi.ticketlink.co.kr/mapi/sports/schedules?categoryId={category_id}&teamId={team_id}&startDate={start_date}&endDate={end_date}"
res = requests.get(url)
data = res.json().get("data", {}).get("schedules", [])

# 날짜별 경기 정보 매핑
match_map = {}
for match in data:
    date = datetime.fromtimestamp(match["scheduleDate"] / 1000, tz=KST).date()
    opponent = match["awayTeam"]["teamName"]
    match_map[date.day] = f"vs {opponent}"

# 달력 표 생성
cal = calendar.Calendar()
month_days = cal.monthdayscalendar(year, month)  # [[0, 0, 0, 1, 2, 3, 4], ...]

cal_display = []
for week in month_days:
    row = []
    for day in week:
        if day == 0:
            row.append("")  # 공란
        elif day in match_map:
            row.append(f"{day}\n{match_map[day]}")
        else:
            row.append(f"{day}")
    cal_display.append(row)

# 달력 표시
df = pd.DataFrame(cal_display, columns=["월", "화", "수", "목", "금", "토", "일"])
st.subheader(f"📅 {month}월 경기 일정")
st.dataframe(df, height=300)
