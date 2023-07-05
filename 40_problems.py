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

#직무별 역량 평가 설문조사
df = pd.DataFrame({'직무':['생산기술', '대외협력', '환경안전', '연구개발', '구매', '소프트웨어', '경영관리', '인사', '품질/서비스', '영업', '법무', '마케팅', 'SCM/물류', '재무', '디자인', '제조'],
                   'AI 활용 능력(본인평가)':['3.5', '3.2', '3.5', '4.2', '2.7', '4.2', '2.1', '3.1', '2.6', '3.9', '2.2', '3.2', '3.2', '2.8', '1.4', '4.2']})

with st.container():

    st.markdown("---")

    st.subheader("우리 기업은 생성형 AI 시대에 얼마나 대비하고 있을까?")
    custom_subheader('생성형 AI 활용 능력 자가 진단 결과: 본인의 AI 활용 능력은 몇 점이라고 생각하십니까? (5점 만점)')

    select_positions = st.multiselect('조회할 직무를 선택하세요',
                                    df['직무'].to_list())

    selected_df = df[df['직무'].isin(select_positions)]
    st.session_state['selected_df'] = selected_df

    fig = go.Figure()
    fig.add_trace(go.Bar(x = st.session_state['selected_df']['직무'], y = st.session_state['selected_df']['AI 활용 능력(본인평가)'], name = '본인의 AI 활용 능력은 몇 점이라고 생각하십니까? (5점 만점)'))
    fig.update_layout(width=1500, height=500)

    st.plotly_chart(fig)

    st.markdown("---")


df2 = pd.DataFrame({'직무':['생산기술', '대외협력', '환경안전', '연구개발', '구매', '소프트웨어', '경영관리', '인사', '품질/서비스', '영업', '법무', '마케팅', 'SCM/물류', '재무', '디자인', '제조'],
                   '재정 지원 부족':[x.round(0) for x in np.abs(np.random.randn(16)) * 100],
                   '시간 여유 부족':[x.round(0) for x in np.abs(np.random.randn(16)) * 100],
                   '강의 컨텐츠 부족':[x.round(0) for x in np.abs(np.random.randn(16)) * 100],
                   '동기 부족':[x.round(0) for x in np.abs(np.random.randn(16)) * 100]})

with st.container():

    custom_subheader('생성형 AI 활용 교육 설문조사: 사내에서 실시되었던 AI 활용 역량 지원 제도의 가장 큰 문제점은 무엇이라고 생각하십니까?')

    select_positions2 = st.multiselect('조회할 직무들을 선택하세요',
                                    df2['직무'].to_list())

    selected_df2 = df2[df2['직무'].isin(select_positions2)]
    st.session_state['selected_df2'] = selected_df2

    fig2 = go.Figure()
    labels = st.session_state['selected_df2'].iloc[:,1:].columns.to_list()
    values = st.session_state['selected_df2'].iloc[:,1:].sum(axis=0).to_list()
    fig2.add_trace(go.Pie(labels = labels, values = values, name = 'temp'))

    st.plotly_chart(fig2)

    st.markdown("---")

