import streamlit as st
import requests
from datetime import datetime, timedelta, timezone

st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRkiysVfhune8FJdE0QiuMLJAx-9auObUpDFA&s", use_column_width=True)

st.title("🎫 한화 직링 생성기")
st.markdown("""
> 🙏 꿈돌이 김대인의 한화 티켓팅 **by 1004**  
> ⚠️ **주의:** 예매 시작 시간인 **11시 정각**에 입장  
> 👉 막혀도 내 탓 아님.
""")


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

# ✅ 이번 달 경기 리스트는 아래에 표시
today = datetime.now()
start_of_month = today.replace(day=1).strftime("%Y%m%d")
end_of_month = (today.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
end_of_month_str = end_of_month.strftime("%Y%m%d")

schedule_url = f"https://mapi.ticketlink.co.kr/mapi/sports/schedules?categoryId={category_id}&teamId={team_id}&startDate={start_of_month}&endDate={end_of_month_str}"

try:
    res = requests.get(schedule_url)
    schedules = res.json()['data']['schedules']
    if schedules:
        st.subheader("📌 이번 달 예정된 경기")
        for s in schedules:
            match_time = datetime.fromtimestamp(s['scheduleDate'] / 1000, tz=timezone(timedelta(hours=9)))
            date_str = match_time.strftime("%m월 %d일 (%a) %H:%M")
            st.write(f"- {date_str}: {s['homeTeam']['teamName']} vs {s['awayTeam']['teamName']} ({s['matchTitle']})")
    else:
        st.write("이번 달에는 예정된 경기가 없습니다.")
except Exception as e:
    st.error(f"⚠️ 경기 정보를 불러오는 데 실패했습니다: {e}")
