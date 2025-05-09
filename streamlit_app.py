import streamlit as st
import requests
from datetime import datetime, timedelta, timezone

st.title("🎫 한화 직링 생성기")
st.caption("※ 제발 티켓팅 좀 성공하자 by 1004")

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
            product_id = schedule['productId']
            home_team = schedule['homeTeam']['teamName']
            away_team = schedule['awayTeam']['teamName']
            match_title = schedule['matchTitle']

            # ✅ 한국 시간으로 변환
            KST = timezone(timedelta(hours=9))
            match_time = datetime.fromtimestamp(schedule['scheduleDate'] / 1000, tz=KST).strftime("%Y년 %m월 %d일 %H:%M")

            # 직링 (요구한 형식으로)
            link = f"https://www.ticketlink.co.kr/reserve/product/{product_id}?scheduleId={schedule_id}"

            # 출력
            st.success(f"🔗 직링: {link}")
            st.info(f"""
- 🏟️ 경기: {home_team} vs {away_team}  
- 🎯 구간: {match_title}  
- 🕒 시작 시간: {match_time}
            """)
    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")
