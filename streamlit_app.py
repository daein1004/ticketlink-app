import streamlit as st
import requests

st.title("🎫 티켓링크 직링 생성기")

team_id = st.text_input("팀 ID (예: 63)")
category_id = st.text_input("종목 ID (예: 137)")
date = st.text_input("경기 날짜 (yyyymmdd 형식)")

if st.button("직링 생성"):
    url = f"https://mapi.ticketlink.co.kr/mapi/sports/schedules?categoryId={category_id}&teamId={team_id}&startDate={date}&endDate={date}"
    try:
        res = requests.get(url)
        data = res.json()
        schedule_id = data['data']['schedules'][0]['scheduleId']
        link = f"https://www.ticketlink.co.kr/reserve/plan/schedule/{schedule_id}?menuIndex=reserve"
        st.success(f"🔗 직링: {link}")
    except:
        st.error("⚠️ 해당 날짜에 경기가 없거나 오류가 발생했습니다.")

