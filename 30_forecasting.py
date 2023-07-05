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
                   '현재인원':['2341.3', '33.2', '149.5', '4607.5', '192.7', '1354.2', '258.1', '304.1', '520.6', '337.9', '67.2', '377.2', '63.2', '87', '168.4', '1242.2'],
                    '대체후인원':['2106.4', '29.9', '134', '4114.4', '169.1', '1177.5', '221.6', '259.8', '444', '287.4', '57.2', '317.5', '52.8', '70.9', '133.9', '973.9']})
df['현재인원'] = [float(x) for x in df['현재인원']]
df['대체후인원'] = [float(x) for x in df['대체후인원']]
df['대체율'] = (df['현재인원'] - df['대체후인원'])/df['현재인원']

#직무별 인력 변화 전망: 대직무 수준
with st.container():

    st.markdown("---")

    custom_subheader('생성형 AI에 의한 직무별 인력 변화 전망 (전자 DX/DS 통합; 대직무별)')

    select_positions = st.multiselect('조회할 직무를 선택하세요',
                                    df['직무'].to_list())

    selected_df = df[df['직무'].isin(select_positions)]
    st.session_state['selected_df'] = selected_df

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x = st.session_state['selected_df']['직무'], y = st.session_state['selected_df']['현재인원'], name = '현재인원(명)'))
    fig.add_trace(go.Bar(x = st.session_state['selected_df']['직무'], y = st.session_state['selected_df']['대체후인원'], name = '대체후인원(명)'))
    fig.add_trace(go.Line(x = st.session_state['selected_df']['직무'], y = st.session_state['selected_df']['대체율'], name = '대체율'), secondary_y=True)
    fig.update_layout(width=1500, height=500)

    st.plotly_chart(fig)

    st.markdown("---")


