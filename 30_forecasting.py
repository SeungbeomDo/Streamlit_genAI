import xlwings as xw
import re
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import matplotlib.pyplot as plt

import base64
import io
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import Workbook

import ast
import random

import streamlit as st
from st_pages import Page, show_pages

#페이지 레이아웃
st.set_page_config(
    page_title="생성형 AI와 인력구조 변화 예측",
    layout="wide",
    initial_sidebar_state="auto",
)

#그래프 제목 스타일
def custom_subheader(text):
    subheader_style = """
    <style>
        .custom-subheader {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol';
            font-size: 16px;
            font-weight: 600;
        }
    </style>
    """
    st.markdown(subheader_style, unsafe_allow_html=True)
    st.markdown(f"<div class='custom-subheader'>{text}</div>", unsafe_allow_html=True)

#직무별 대체 전망 데이터: 대직무별
df = pd.DataFrame({'직무':['생산기술', '대외협력', '환경안전', '연구개발', '구매', '소프트웨어', '경영관리', '인사', '품질/서비스', '영업', '법무', '마케팅', 'SCM/물류', '재무', '디자인', '제조'],
                   '현재인원':[abs(round(x,0)) for x in np.random.randn(16)*10000],
                    '대체후인원':[abs(round(x,0)) for x in np.random.randn(16)*10000]})
df['대체율'] = (df['현재인원']-df['대체후인원'])/df['현재인원']

df_temp = df.copy()

#직무별 인력 변화 전망: 대직무 수준
with st.container():

    st.markdown("---")
    st.subheader("직무별 인력 변화 시나리오")

    custom_subheader('거시 전망: 생성형 AI에 의한 직무별 인력 변화 시나리오')

    select_positions = st.multiselect('조회할 직무들을 선택하세요',
                                    df_temp['직무'].to_list())
    
    selected_scenario = st.selectbox('적용할 시나리오를 선택하세요',
                                     ['1번 시나리오', '2번 시나리오', '3번 시나리오'])

    selected_df_temp = df_temp[df_temp['직무'].isin(select_positions)]
    st.session_state['selected_df_temp'] = selected_df_temp

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x = st.session_state['selected_df_temp']['직무'], y = st.session_state['selected_df_temp']['현재인원'], name = '현재인원(명)'))
    fig.add_trace(go.Bar(x = st.session_state['selected_df_temp']['직무'], y = st.session_state['selected_df_temp']['대체후인원'], name = '대체후인원(명)'))
    fig.add_trace(go.Line(x = st.session_state['selected_df_temp']['직무'], y = st.session_state['selected_df_temp']['대체율'], name = '대체율(우측)'), secondary_y=True)
    fig.update_layout(width=1500, height=500)

    st.plotly_chart(fig)

#기업 내 직무별 인력 변화 전망: 대직무 수준
with st.container():

    st.markdown("---")
    st.subheader("우리 기업의 실제 인력 구조에 위 시나리오를 적용하면 어떨까?")

    custom_subheader('생성형 AI에 의한 우리 기업 내 인력 변화 전망')

    select_positions = st.multiselect('조회할 직무를 선택하세요',
                                    df['직무'].to_list())
    
    selected_scenario = st.selectbox('원하는 시나리오를 선택하세요',
                                    ['1번 시나리오', '2번 시나리오', '3번 시나리오'])

    selected_df = df[df['직무'].isin(select_positions)]
    st.session_state['selected_df'] = selected_df

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x = st.session_state['selected_df']['직무'], y = st.session_state['selected_df']['현재인원'], name = '현재인원(명)'))
    fig.add_trace(go.Bar(x = st.session_state['selected_df']['직무'], y = st.session_state['selected_df']['대체후인원'], name = '대체후인원(명)'))
    fig.add_trace(go.Line(x = st.session_state['selected_df']['직무'], y = st.session_state['selected_df']['대체율'], name = '대체율(우측)'), secondary_y=True)
    fig.update_layout(width=1500, height=500)

    st.plotly_chart(fig)

    st.markdown("---")


