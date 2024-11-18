import streamlit as st
import folium
from folium import plugins
import pandas as pd
import numpy as np
from streamlit_folium import folium_static
import math

# 페이지 설정
st.set_page_config(page_title="디지털 시니어 헬스케어 서포터즈", layout="wide")

# 데이터 정의
centers_data = {
    '권역': ['수도권', '강원권', '충청권', '전라권', '경상권', '제주권'],
    '운영센터수': [15, 0, 8, 7, 10, 0],
    '계획센터수': [0, 5, 0, 0, 0, 3],
    '위도': [37.5665, 37.8228, 36.6372, 35.8161, 35.8714, 33.4996],
    '경도': [126.9780, 128.1555, 127.4927, 127.1089, 128.6014, 126.5312],
    '가동률': [95, 0, 85, 80, 90, 0],
    '이용자수': [4500, 0, 2400, 2100, 3000, 0],
    '의료기관': [25, 8, 15, 12, 18, 5],
    '복지시설': [30, 10, 20, 15, 25, 8],
    '디지털역량': [90, 65, 85, 80, 88, 70]
}

df = pd.DataFrame(centers_data)

# 위경도 변환 함수
def get_circle_coordinates(center_lat, center_lng, radius_km, num_points):
    coordinates = []
    for i in range(num_points):
        angle = math.radians(i * (360 / num_points))
        dx = radius_km * math.cos(angle)
        dy = radius_km * math.sin(angle)
        
        # 위도/경도 변환 (근사값)
        new_lat = center_lat + (dy / 111)  # 1도 = 약 111km
        new_lng = center_lng + (dx / (111 * math.cos(math.radians(center_lat))))
        coordinates.append([new_lat, new_lng])
    
    return coordinates

# 지도 생성 함수
def create_detailed_map():
    m = folium.Map(location=[36.5, 127.5], zoom_start=7)
    
    # 각 권역별 정보창 스타일
    html_template = """
    <div style="width: 300px; padding: 10px; background-color: white; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
        <h4 style="color: #1e3a5f; margin-bottom: 10px;">{권역} 현황</h4>
        <div style="margin-bottom: 5px;">
            <b>센터 현황:</b> 운영 {운영}개소 / 계획 {계획}개소
        </div>
        <div style="margin-bottom: 5px;">
            <b>가동률:</b> {가동률}%
        </div>
        <div style="margin-bottom: 5px;">
            <b>이용자수:</b> {이용자}명
        </div>
        <div style="margin-bottom: 5px;">
            <b>협력기관:</b> 의료기관 {의료}개 / 복지시설 {복지}개
        </div>
        <div style="margin-bottom: 5px;">
            <b>디지털역량:</b> {디지털}%
        </div>
        <div style="background-color: #f8f9fa; padding: 5px; border-radius: 5px; margin-top: 10px;">
            <small>클릭하여 상세 정보 확인</small>
        </div>
    </div>
    """

    # 권역별 원형 표시
    for idx, row in df.iterrows():
        # 운영중인 센터
        if row['운영센터수'] > 0:
            color = '#1e3a5f'
            radius = row['운영센터수'] * 1.5
            fill_color = '#1e3a5f'
            html = html_template.format(
                권역=row['권역'],
                운영=row['운영센터수'],
                계획=row['계획센터수'],
                가동률=row['가동률'],
                이용자=row['이용자수'],
                의료=row['의료기관'],
                복지=row['복지시설'],
                디지털=row['디지털역량']
            )
            
            # 메인 마커
            folium.CircleMarker(
                location=[row['위도'], row['경도']],
                radius=radius,
                popup=folium.Popup(html, max_width=300),
                color=color,
                fill=True,
                fill_color=fill_color,
                fill_opacity=0.7
            ).add_to(m)
            
            # 협력기관 표시 (원형으로 배치)
            circle_coords = get_circle_coordinates(
                row['위도'], row['경도'], 0.1, min(row['의료기관'], 8)
            )
            
            for coord in circle_coords:
                folium.CircleMarker(
                    location=coord,
                    radius=3,
                    color='#2563eb',
                    fill=True,
                    fill_color='#2563eb'
                ).add_to(m)

        # 계획중인 센터
        if row['계획센터수'] > 0:
            color = '#2563eb'
            radius = row['계획센터수'] * 1.5
            fill_color = '#2563eb'
            html = html_template.format(
                권역=row['권역'],
                운영=row['운영센터수'],
                계획=row['계획센터수'],
                가동률=0,
                이용자=0,
                의료=row['의료기관'],
                복지=row['복지시설'],
                디지털=row['디지털역량']
            )
            
            folium.CircleMarker(
                location=[row['위도'], row['경도']],
                radius=radius,
                popup=folium.Popup(html, max_width=300),
                color=color,
                fill=True,
                fill_color=fill_color,
                fill_opacity=0.7
            ).add_to(m)

    # 지도에 범례 추가
    legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; right: 50px; width: 150px; height: 90px; 
                background-color: white;
                border-radius: 5px;
                padding: 10px;
                z-index: 9999;
                font-size: 12px;">
        <p><i class="fa fa-circle fa-1x" style="color:#1e3a5f"></i> 운영중</p>
        <p><i class="fa fa-circle fa-1x" style="color:#2563eb"></i> 계획중</p>
        <p><i class="fa fa-circle fa-1x" style="color:#2563eb"></i> 협력기관</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    return m

# 메인 앱
st.title("디지털 시니어 헬스케어 서포터즈 현황")

# 필터 옵션
col1, col2, col3 = st.columns(3)
with col1:
    view_option = st.selectbox(
        "보기 옵션",
        ["전체 현황", "운영 센터만", "계획 센터만"]
    )
with col2:
    show_facilities = st.checkbox("협력기관 표시", value=True)
with col3:
    show_stats = st.checkbox("통계 정보 표시", value=True)

# 지도 표시
m = create_detailed_map()
folium_static(m)

if show_stats:
    # 하단 통계
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("총 센터 수", f"{df['운영센터수'].sum() + df['계획센터수'].sum()}개소")
    with col2:
        st.metric("운영중 센터", f"{df['운영센터수'].sum()}개소")
    with col3:
        avg_operation = df[df['가동률'] > 0]['가동률'].mean()
        st.metric("평균 가동률", f"{avg_operation:.1f}%")
    with col4:
        st.metric("총 이용자 수", f"{df['이용자수'].sum():,}명")

# 데이터 출처 및 갱신일
st.markdown("---")
st.caption("데이터 갱신일: 2024.03.18")
