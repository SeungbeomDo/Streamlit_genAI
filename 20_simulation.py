#라이브러리 임포트
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

#페이지 config
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

#데이터 임포트: 직무별 기능 중요도 데이터프레임
df_position_skill = pd.DataFrame({'직무':['영업', '인사', '연구개발', '경영관리', '재무', '법무', '대외협력', '디자인', '제조', '생산기술'], 
                                 '감각능력':[abs(round(x,0)) for x in np.random.randn(10)], 
                                 '인지능력':[abs(round(x,0)) for x in np.random.randn(10)], 
                                 '자연어처리':[abs(round(x,0)) for x in np.random.randn(10)], 
                                 '사회적능력':[abs(round(x,0)) for x in np.random.randn(10)], 
                                 '육체적능력':[abs(round(x,0)) for x in np.random.randn(10)]})

df_position_skill.iloc[:, 1:] = df_position_skill.iloc[:, 1:].sub(df_position_skill.iloc[:, 1:].mean(1), axis=0).div(df_position_skill.iloc[:, 1:].std(1), axis=0)
df_position_skill.iloc[:, 1:] = abs(df_position_skill.iloc[:, 1:])
df_position_skill.iloc[:, 1:] = df_position_skill.iloc[:, 1:].div(df_position_skill.iloc[:, 1:].sum(1), axis=0)

#데이터 임포트: 직무별 현재 인원 데이터프레임
df_position_volume = pd.DataFrame({'직무':['영업', '인사', '연구개발', '경영관리', '재무', '법무', '대외협력', '디자인', '제조', '생산기술'],
                                   '현재인원':[abs(round(x,0)) for x in np.random.randn(10)*10000]})

#직무별 대체 시뮬레이션
with st.container():

    st.subheader("5대 기능 영역에 따른 직무별 대체율 시뮬레이션")

    with st.container():
        col_a, col_b = st.columns([0.42, 0.58])

        with col_a:
            st.write("(1) 조회하고 싶은 <직무>들을 선택해주세요(복수 선택 가능).")
            with st.form('inputs for simulation 1'):

                selected_position_p2 = st.multiselect("조회할 직무들을 선택하세요.", df_position_skill['직무'].to_list())
                selected_skill_p2 = df_position_skill[df_position_skill['직무'].isin(selected_position_p2)]
                st.session_state['selected_skill_p2'] = selected_skill_p2

                st.form_submit_button("직무별 기술 중요도 확인")

        with col_b:
            st.write("(2) 각 <직무 기능>의 대체가능성을 평가해주세요(0~1 사이의 실수).")
            with st.form('inputs for simulation 2'):

                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    selected_weight_1 = st.number_input("<감각능력>", 0.0, 1.0)
                with col2:
                    selected_weight_2 = st.number_input("<인지능력>", 0.0, 1.0)
                with col3:
                    selected_weight_3 = st.number_input("<자연어처리>", 0.0, 1.0)
                with col4:
                    selected_weight_4 = st.number_input("<사회적능력>", 0.0, 1.0)
                with col5:
                    selected_weight_5 = st.number_input("<육체적능력>", 0.0, 1.0)    

                selected_weights = [selected_weight_1, selected_weight_2, selected_weight_3, selected_weight_4, selected_weight_5]
                st.session_state['selected_weights'] = selected_weights
                st.session_state['rate'] = np.dot(st.session_state['selected_skill_p2'].iloc[:, 1:], st.session_state['selected_weights'])

                st.form_submit_button("시뮬레이션 생성")
        
    with st.container():
        col_c, col_d = st.columns(2)

        with col_c:
            custom_subheader('직무별 기능 중요도')
            trace1 = go.Bar(x = st.session_state['selected_skill_p2']['직무'], y = st.session_state['selected_skill_p2']['감각능력'], name = '감각능력')
            trace2 = go.Bar(x = st.session_state['selected_skill_p2']['직무'], y = st.session_state['selected_skill_p2']['인지능력'], name = '인지능력')
            trace3 = go.Bar(x = st.session_state['selected_skill_p2']['직무'], y = st.session_state['selected_skill_p2']['자연어처리'], name = '자연어처리')
            trace4 = go.Bar(x = st.session_state['selected_skill_p2']['직무'], y = st.session_state['selected_skill_p2']['사회적능력'], name = '사회적능력')
            trace5 = go.Bar(x = st.session_state['selected_skill_p2']['직무'], y = st.session_state['selected_skill_p2']['육체적능력'], name = '육체적능력')    
            layout = go.Layout(barmode = 'stack')
            fig = go.Figure(data = [trace1, trace2, trace3, trace4, trace5], layout = layout)
            fig.update_layout(width=500, height=500)
            st.plotly_chart(fig) 

        with col_d:
            selected_volume = df_position_volume[df_position_volume['직무'].isin(selected_position_p2)]
            selected_volume['대체후인원'] = round(selected_volume['현재인원'] * (1 - st.session_state['rate']), 0)
            st.session_state['selected_volume'] = selected_volume
            st.session_state['volume_changed'] = selected_volume
            fig2 = make_subplots(specs=[[{"secondary_y": True}]])
            fig2.add_trace(go.Bar(x = st.session_state['selected_volume']['직무'], y = st.session_state['selected_volume']['현재인원'], name = '현재인원(명)'))
            fig2.add_trace(go.Bar(x = st.session_state['selected_volume']['직무'], y = st.session_state['volume_changed']['대체후인원'], name = '대체후인원(명)'))
            fig2.add_trace(go.Line(x = st.session_state['selected_volume']['직무'], y = st.session_state['rate'], name = '대체율(우측)'), secondary_y=True)
            fig2.update_layout(width=500, height=500)

            custom_subheader('직무별 대체율 시뮬레이션')
            st.plotly_chart(fig2)

    st.markdown('---')

