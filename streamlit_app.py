import streamlit as st
import requests
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
import time


# ✅ 앱 시작
st.title("🍀 모두 티켓팅 성공하길 🍀")
st.image(
    "https://m1.daumcdn.net/cfile271/image/235D7B4A596EE7CE1578D1",
    use_container_width=True
)
st.markdown("""
> 🙏 꿈돌이 김*인의 한화 티켓팅 도전기.   
> ⚠️ 예매 시작 시간 전에 입장 시 막힐 수 있음.  
> 📝 직링 복사하고 주소창 붙여 넣기 후, 11시 땡하면 엔터.  
> 👉 티켓팅 망해도 내 탓 아님.
""")

# 🔐 퀴즈 인증
st.subheader("퀴즈")
answer = st.text_input("꿈돌이 김*인의 생일은? (YYYYMMDD 형식으로 입력)")

if answer.strip() != "20001004":
    st.warning("❌ 정답을 모르는 당신, 이용할 자격이 없다 ❌")
    st.stop()

# ✅ 고정된 팀 정보
team_id = "63"         # 한화 이글스
category_id = "137"    # 야구

# ✅ 날짜 선택
selected_date = st.date_input("📅 경기 날짜 선택")
start_date = selected_date.strftime("%Y%m%d")
end_date = (selected_date + timedelta(days=1)).strftime("%Y%m%d")

# ✅ 링크 생성
if st.button("직링 생성"):
    url = f"https://mapi.ticketlink.co.kr/mapi/sports/schedules?categoryId={category_id}&teamId={team_id}&startDate={start_date}&endDate={end_date}"
    try:
        res = requests.get(url)
        data = res.json()
        schedules = data['data']['schedules']

        if not schedules:
            st.warning("⚠️ 해당 날짜에 경기 정보가 없습니다.")
        else:
            schedule = schedules[0]
            schedule_id = schedule['scheduleId']
            product_id = schedule['productId']
            home_team = schedule['homeTeam']['teamName']
            away_team = schedule['awayTeam']['teamName']
            match_title = schedule['matchTitle']

            # KST 시간대
            KST = timezone(timedelta(hours=9))
            match_time = datetime.fromtimestamp(schedule['scheduleDate'] / 1000, tz=KST).strftime("%Y년 %m월 %d일 %H:%M")

            link = f"https://www.ticketlink.co.kr/reserve/product/{product_id}?scheduleId={schedule_id}"

            st.success(f"🔗 직링 바로가기: {link}")
            st.text_input("📋 직링 복사하기", value=link)
            st.info(f"""
- 🏟️ 경기: {home_team} vs {away_team}  
- 🎯 구간: {match_title}  
- 🕒 시작 시간: {match_time}
            """)
    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")

# ✅ 향후 5주간 한화 홈경기 일정 표시
today = datetime.now()
start_date_range = today.strftime("%Y%m%d")
end_date_range = (today + timedelta(weeks=5)).strftime("%Y%m%d")

schedule_url = f"https://mapi.ticketlink.co.kr/mapi/sports/schedules?categoryId={category_id}&teamId={team_id}&startDate={start_date_range}&endDate={end_date_range}"

try:
    res = requests.get(schedule_url)
    schedules = res.json()['data']['schedules']
    filtered = [s for s in schedules if s['homeTeam']['teamName'] == "한화이글스"]

    if filtered:
        st.subheader("📌 향후 5주간 한화 홈경기 일정")
        for s in filtered:
            match_time = datetime.fromtimestamp(s['scheduleDate'] / 1000, tz=timezone(timedelta(hours=9)))
            date_str = match_time.strftime("%m월 %d일 (%a) %H:%M")
            home = s['homeTeam']['teamName']
            away = s['awayTeam']['teamName']
            section = s['matchTitle']

            st.markdown(f"""
**• {date_str}**  
&nbsp;&nbsp;&nbsp;🏟️ {home} vs {away}  
&nbsp;&nbsp;&nbsp;🎯 구간: {section}
""")
    else:
        st.info("향후 5주간 예정된 한화 홈경기가 없습니다.")
except Exception as e:
    st.error(f"⚠️ 경기 정보를 불러오는 데 실패했습니다: {e}")
