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
wb = xw.Book('P:/2023_생성형 AI와 인력구조 변화 예측/3. 참고자료/230512_전자_직무별 생성형 AI 대체 가능성.xlsx')
sheet = wb.sheets('피벗')
values = sheet['E2:G18'].value
rows = sheet['A2:A18'].value

df = pd.DataFrame(values)
df.columns =  ['현재인원', '대체후인원', '대체율']
df = df.iloc[1:,:]

rows = [x[4:] for x in rows]
rows = [x[:-6] for x in rows]
rows = rows[1:]
df.insert(0, '직무', rows)
df.iloc[4,0] = '마케팅'
df.iloc[10,0] = '품질/서비스'
df.iloc[13,0] = '법무'

df_temp = df.copy()

#직무별 인력 변화 전망: 대직무 수준
with st.container():

    st.markdown("---")
    st.subheader("1) 직무별 인력 변화 시나리오")

    select_positions = st.multiselect('조회할 직무들을 선택하세요',
                                    df_temp['직무'].to_list())
    
    selected_scenario1 = st.selectbox('직급에 부여할 가중치를 선택하세요: 직급이 높을수록 더 많이 대체될까?',
                                     ['20%', '40%', '60%', '80%'])

    selected_scenario2 = st.selectbox('연봉에 부여할 가중치를 선택하세요: 연봉이 높을수록 더 많이 대체될까?',
                                     ['20%', '40%', '60%', '80%'])
    
    selected_scenario3 = st.selectbox('업무 특성에 부여할 가중치를 선택하세요: 단순반복성 업무일수록 더 많이 대체될까?',
                                     ['20%', '40%', '60%', '80%'])

    selected_df_temp = df_temp[df_temp['직무'].isin(select_positions)]
    st.session_state['selected_df_temp'] = selected_df_temp

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x = st.session_state['selected_df_temp']['직무'], y = st.session_state['selected_df_temp']['현재인원'], name = '현재인원(명)'))
    fig.add_trace(go.Bar(x = st.session_state['selected_df_temp']['직무'], y = st.session_state['selected_df_temp']['대체후인원'], name = '대체후인원(명)'))
    fig.add_trace(go.Line(x = st.session_state['selected_df_temp']['직무'], y = st.session_state['selected_df_temp']['대체율'], name = '대체율(우측)'), secondary_y=True)
    fig.update_layout(width=1500, height=500)

    custom_subheader('생성된 시나리오 하에서 직무별 대체율')
    st.plotly_chart(fig)

#기업 내 직무별 인력 변화 전망: 대직무 수준
with st.container():

    st.markdown("---")
    st.subheader("2) 우리 기업의 실제 인력 구조에 위 시나리오를 적용하면 어떨까?")

    custom_subheader('생성형 AI에 의한 우리 기업 내 인력 변화 전망')

    select_positions = st.multiselect('조회할 직무를 선택하세요',
                                    df['직무'].to_list())
    
    selected_scenario1 = st.selectbox('직급에 적용할 가중치를 선택하세요: 직급이 높을수록 더 많이 대체될까?',
                                     ['20%', '40%', '60%', '80%'])

    selected_scenario2 = st.selectbox('연봉에 적용할 가중치를 선택하세요: 연봉이 높을수록 더 많이 대체될까?',
                                     ['20%', '40%', '60%', '80%'])
    
    selected_scenario3 = st.selectbox('업무 특성에 적용할 가중치를 선택하세요: 단순반복성 업무일수록 더 많이 대체될까?',
                                     ['20%', '40%', '60%', '80%'])

    selected_df = df[df['직무'].isin(select_positions)]
    st.session_state['selected_df'] = selected_df

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x = st.session_state['selected_df']['직무'], y = st.session_state['selected_df']['현재인원'], name = '현재인원(명)'))
    fig.add_trace(go.Bar(x = st.session_state['selected_df']['직무'], y = st.session_state['selected_df']['대체후인원'], name = '대체후인원(명)'))
    fig.add_trace(go.Line(x = st.session_state['selected_df']['직무'], y = st.session_state['selected_df']['대체율'], name = '대체율(우측)'), secondary_y=True)
    fig.update_layout(width=1500, height=500)

    custom_subheader('생성된 시나리오 하에서 직무별 대체율')
    st.plotly_chart(fig)

    st.markdown("---")

