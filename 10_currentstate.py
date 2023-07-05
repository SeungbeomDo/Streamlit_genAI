import xlwings as xw
import re
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import datetime
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots

import base64
import io
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import Workbook

import ast
import random

import streamlit as st
from st_pages import Page, show_pages

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

st.markdown("---")

def date_range(start, end):
    start = datetime.datetime.strptime(start, "%Y-%m-%d")
    end = datetime.datetime.strptime(end, "%Y-%m-%d")
    dates = [(start + datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end-start).days+1)]
    return dates

df = pd.DataFrame({'date':date_range('2020-01-01', '2023-06-30'), 
                              'issues':[x**2 for x in np.arange(len(date_range('2020-01-01', '2023-06-30')))]})

st.subheader("생성형 AI가 일자리를 대체할 것이라는 언론 보도 증가")

with st.container():

    st.markdown("---")

    custom_subheader("뉴스 기사 수 (Key word : 생성형 AI & 일자리)")

    select_date_start = st.date_input('조회를 시작할 날짜를 선택하세요', datetime.date(2020,1,1))
    select_date_end = st.date_input('조회를 종료할 날짜를 선택하세요', datetime.date(2023,6,30))

    st.session_state['date_start'] = select_date_start
    st.session_state['date_end'] = select_date_end

    if st.session_state['date_start'] < st.session_state['date_end']:
        pass
    else: 
        # st.write('종료날짜는 시작날짜보다 최소한 하루 뒤여야 합니다.', )
        st.markdown(":red[종료날짜는 시작날짜보다 최소한 하루 뒤여야 합니다.]")

    selected_df = df[(df['date']>=str(select_date_start))&(df['date']<=str(select_date_end))]
    st.session_state['selected_df'] = selected_df

    fig = go.Figure()
    fig.add_trace(go.Line(x = st.session_state['selected_df']['date'], y = st.session_state['selected_df']['issues']))
    st.plotly_chart(fig)

    st.markdown("---")


