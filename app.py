import streamlit as st
import folium
from folium import plugins
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_folium import folium_static

# 페이지 기본 설정
st.set_page_config(
    page_title="디지털 시니어 헬스케어 서포터즈 현황",
    page_icon="🏥",
    layout="wide"
)

# 제목과 설명
st.title("디지털 시니어 헬스케어 서포터즈 현황")
st.markdown("### 지역별 거점 센터 분포 및 운영 현황")

# 데이터 생성
centers_data = {
    '권역': ['수도권', '강원권', '충청권', '전라권', '경상권', '제주권'],
    '운영센터수': [15, 0, 8, 7, 10, 0],
    '계획센터수': [0, 5, 0, 0, 0, 3],
    '위도': [37.5665, 37.8228, 36.6372, 35.8161, 35.8714, 33.4996],
    '경도': [126.9780, 128.1555, 127.4927, 127.1089, 128.6014, 126.5312],
    '가동률': [95, 0, 85, 80, 90, 0],
    '이용자수': [4500, 0, 2400, 2100, 3000, 0]
}

df = pd.DataFrame(centers_data)

# 2단 레이아웃
col1, col2 = st.columns([2, 1])

with col1:
    # 지도 생성
    st.subheader("거점 센터 위치")
    m = folium.Map(location=[36.5, 127.5], zoom_start=7)

    # 운영중인 센터
    for idx, row in df[df['운영센터수'] > 0].iterrows():
        folium.CircleMarker(
            location=[row['위도'], row['경도']],
            radius=row['운영센터수'] * 1.5,
            popup=f"{row['권역']}: {row['운영센터수']}개소 (가동률: {row['가동률']}%)",
            color='#1e3a5f',
            fill=True,
            fill_color='#1e3a5f'
        ).add_to(m)

    # 계획중인 센터
    for idx, row in df[df['계획센터수'] > 0].iterrows():
        folium.CircleMarker(
            location=[row['위도'], row['경도']],
            radius=row['계획센터수'] * 1.5,
            popup=f"{row['권역']}: {row['계획센터수']}개소 (계획)",
            color='#2563eb',
            fill=True,
            fill_color='#2563eb'
        ).add_to(m)

    folium_static(m)

with col2:
    # 운영 현황 차트
    st.subheader("센터 운영 현황")
    
    # 막대 차트
    fig_bar = go.Figure(data=[
        go.Bar(name='운영중', x=df['권역'], y=df['운영센터수'], marker_color='#1e3a5f'),
        go.Bar(name='계획중', x=df['권역'], y=df['계획센터수'], marker_color='#2563eb')
    ])
    
    fig_bar.update_layout(barmode='stack', height=300)
    st.plotly_chart(fig_bar, use_container_width=True)

    # 가동률 게이지 차트
    st.subheader("권역별 가동률")
    for idx, row in df[df['가동률'] > 0].iterrows():
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = row['가동률'],
            title = {'text': row['권역']},
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {'axis': {'range': [None, 100]},
                    'bar': {'color': "#1e3a5f"}}
        ))
        fig_gauge.update_layout(height=150)
        st.plotly_chart(fig_gauge, use_container_width=True)

# 하단 통계
st.markdown("---")
col3, col4, col5, col6 = st.columns(4)

with col3:
    st.metric("총 센터 수", f"{df['운영센터수'].sum() + df['계획센터수'].sum()}개소")
with col4:
    st.metric("운영중 센터", f"{df['운영센터수'].sum()}개소")
with col5:
    avg_operation = df[df['가동률'] > 0]['가동률'].mean()
    st.metric("평균 가동률", f"{avg_operation:.1f}%")
with col6:
    st.metric("총 이용자 수", f"{df['이용자수'].sum():,}명")

# 주요 성과 지표
st.markdown("### 주요 성과 지표 (2024년 기준)")
col7, col8, col9 = st.columns(3)

with col7:
    st.markdown("""
    - 건강지표 개선: 30%
    - 의료비 절감: 20%
    - 디지털 역량: 90%
    """)
with col8:
    st.markdown("""
    - 서포터즈 수: 2,000명
    - 협력기관: 120개
    - 만족도: 85%
    """)
with col9:
    st.markdown("""
    - 사회참여: 40% 증가
    - 돌봄부담: 50% 감소
    - 정책반영: 진행중
    """)

# 데이터 출처 및 갱신일
st.markdown("---")
st.caption("데이터 갱신일: 2024.03.18")
