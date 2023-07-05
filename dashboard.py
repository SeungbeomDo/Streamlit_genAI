import xlwings as xw
import re
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
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

show_pages(
    [Page("dashboard.py", "Main"), #보고서 제목, 목차, 요약 등을 담는 페이지
     Page("10_currentstate.py", "배경"), #검토 배경: 생성형 AI의 정의, 산업적 영향에 대한 관심 증가한다는 양적 근거(키워드에 생성형 AI가 들어간 기사 개수 그래프?)
     Page("20_casestudy.py", "Case study: 인력 대체 사례"), #기업별 인력 대체 사례: 국가별 산업별로 클릭하면 기업이 나오고, 그 기업의 케이스를 요약해서 전달?
     Page("30_forecasting.py", "향후 인력 대체 전망"), #직종별, 국가별 인력 대체와 고용 증가 전망 순위 매긴 barplot, 효율화율 barplot
     Page("40_problems.py", "계열사별 대비 필요사항과 대비 실태") #계열사별로 대비해야 할 사항(인력 수급, 스킬 재교육 등)과 각 사항에 대한 대비 실태?
    ]
    )

st.set_page_config(
    page_title="생성형 AI와 인력구조 변화 예측",
    layout="wide",
    initial_sidebar_state="auto",
)

st.title("생성형 AI와 인력구조 변화 예측")
st.write("삼성글로벌리서치 인재경영연구실")

st.markdown('---')
st.subheader("요약")
st.write('본 프로젝트는 생성형 AI의 도입이 기업 내 인력구조에 미칠 영향을 산업별 직무별로 검토하였다 ... ')

st.markdown('---')
st.subheader("목차")
st.write("1. 배경")
st.write("2. Case study: 인력 대체 사례")
st.write("3. 향후 인력 대체 전망")
st.write("4. 계열사별 대비 실태")



