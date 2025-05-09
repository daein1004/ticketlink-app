import streamlit as st
import requests
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
import time

# ✅ 티켓링크 서버 시간 불러오기 함수 (밀리초 포함)
def get_ticketlink_server_time_with_ms():
    try:
        t_start = time.time()
        res = requests.get("https://www.ticketlink.co.kr")
        t_end = time.time()
        server_dt = parsedate_to_datetime(res.headers["Date"])
        round_trip = (t_end - t_start) / 2
        server_dt_local = server_dt + timedelta(hours=9, seconds=round_trip)
        ms = int((server_dt_local.microsecond) / 1000)
        return server_dt_local.strftime(f"%Y년 %m월 %d일 %H:%M:%S.{ms:03d}")
    except Exception as e:
        return f"❌ 오류: {e}"

st.title("🎫 한화 직링 생성기")
st.image(
    "https://mblogthumb-phinf.pstatic.net/20141010_274/doubledune__1412906537536CPFBI_PNG/%B4%D9%C5%A5%B8%E0%C5%CD%B8%AE_3%C0%CF.E366.140914.9%C8%B8_%B8%BB_%C5%F5%BE%C6%BF%F4_-_%C7%D1%C8%AD_%C0%CC%B1%DB%BD%BA_72%BD%C3%B0%A3.HDTV.H264.720p-WITH_0001407129ms.png?type=w420",
    use_container_width=True
)
st.markdown("""
> 🙏 꿈돌이 김대인의 한화 티켓팅.  
> ⚠️ 예매 시작 시간 전에 입장 시 막힐 수 있음.  
> 👉 티켓팅 망해도 내 탓 아님.
""")

# ✅ 티켓링크 서버 시간 표시
st.subheader("🕒 현재 티켓링크 서버 시간 (KST, 밀리초 포함)")
st.code(get_ticketlink_server_time_with_ms())

# 고정된 팀 정보
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

            st.success(f"🔗 직링: {link}")
            st.info(f"""
- 🏟️ 경기: {home_team} vs {away_team}  
- 🎯 구간: {match_title}  
- 🕒 시작 시간: {match_time}
            """)
    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")

# ✅ 이번 달 경기 리스트 (홈경기만)
today = datetime.now()
start_of_month = today.replace(day=1).strftime("%Y%m%d")
end_of_month = (today.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
end_of_month_str = end_of_month.strftime("%Y%m%d")

schedule_url = f"https://mapi.ticketlink.co.kr/mapi/sports/schedules?categoryId={category_id}&teamId={team_id}&startDate={start_of_month}&endDate={end_of_month_str}"

try:
    res = requests.get(schedule_url)
    schedules = res.json()['data']['schedules']
    filtered = [s for s in schedules if s['homeTeam']['teamName'] == "한화이글스"]

    if filtered:
        st.subheader("📌 이번 달 홈경기 일정")
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
        st.info("이번 달 한화 홈경기는 없습니다.")
except Exception as e:
    st.error(f"⚠️ 경기 정보를 불러오는 데 실패했습니다: {e}")
