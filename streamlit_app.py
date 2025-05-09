import streamlit as st
import requests
from datetime import datetime, timedelta

st.title("🎫 티켓링크 직링 생성기")

# 고정된 값
team_id = "63"         # 한화 이글스
category_id = "137"    # 야구

# 날짜 입력 (달력 형식)
selected_date = st.date_input("경기 날짜 선택")
start_date = selected_date.strftime("%Y%m%d")
end_date = (selected_date + timedelta(days=1)).strftime("%Y%m%d")

if st.button("직링 생성"):
    try:
        url = f"https://mapi.ticketlink.co.kr/mapi/sports/schedules?categoryId={category_id}&teamId={team_id}&startDate={start_date}&endDate={end_date}"
        res = requests.get(url)
        data = res.json()
        schedules = data['data']['schedules']

        if not schedules:
            st.error("⚠️ 해당 날짜에 경기가 없습니다.")
        else:
            schedule_id = schedules[0]['scheduleId']
            link = f"https://www.ticketlink.co.kr/reserve/plan/schedule/{schedule_id}?menuIndex=reserve"
            st.success(f"🔗 직링: {link}")
    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")
