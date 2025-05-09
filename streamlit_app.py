import streamlit as st
import requests
from datetime import datetime, timedelta

st.title("🎫 티켓링크 직링 생성기")
st.caption("※ 한화 이글스 기준, 날짜 선택 시 직링 및 경기 정보를 자동 추출합니다.")

# 고정된 팀 정보
team_id = "63"         # 한화 이글스
category_id = "137"    # 야구

# 날짜 선택
selected_date = st.date_input("📅 경기 날짜 선택")
start_date = selected_date.strftime("%Y%m%d")
end_date = (selected_date + timedelta(days=1)).strftime("%Y%m%d")

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
            home_team = schedule['homeTeam']['teamName']
            away_team = schedule['awayTeam']['teamName']
            match_title = schedule['matchTitle']
            match_time = datetime.fromtimestamp(schedule['scheduleDate'] / 1000).strftime("%Y년 %m월 %d일 %H:%M")

            # 직링
            link = f"https://www.ticketlink.co.kr/reserve/plan/schedule/{schedule_id}?menuIndex=reserve"

            # 출력
            st.success(f"🔗 직링: {link}")
            st.info(f"""
- 🏟️ 경기: {home_team} vs {away_team}  
- 🎯 구간: {match_title}  
- 🕒 시작 시간: {match_time}
            """)
    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")
