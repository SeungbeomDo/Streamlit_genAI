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
    [Page("dashboard.py", "0. Main"), 
     Page("10_literature.py", "1. 문헌 데이터베이스"), 
     Page("20_simulation.py", "2. 직무별 대체 시뮬레이션"),
     Page("99_exam.py", "9. 연습용 페이지") 
    ]
    )

st.set_page_config(
    page_title="생성형 AI와 인력구조 변화 예측",
    layout="wide",
    initial_sidebar_state="auto",
)

st.title("생성형 AI와 인력구조 변화 예측")

st.markdown('---')
st.subheader("<페이지 설명>")
st.write("1. 문헌 데이터베이스 : 생성형 일자리와 HR 이슈를 분석한 기사 및 논문 비교분석 조회")
st.write("2. 직무별 대체 시뮬레이션 : 직무별 대체 시뮬레이션 맞춤형 생성")



