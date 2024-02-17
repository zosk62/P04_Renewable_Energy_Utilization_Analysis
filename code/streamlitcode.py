#!/usr/bin/env python
# coding: utf-8

# In[29]:


import streamlit as st
import pandas as pd

### 시각화 라이브러리
import matplotlib
import matplotlib.pyplot as plt # 차트나 그림이 들어있다
import seaborn as sns # 파스텔 색감

### 폰트 환결설정 라이브러리
from matplotlib import font_manager, rc
plt.rc("font", family = "Malgun Gothic")

### 그래프 내에 마이너스(-) 표시 기호 적용하기
plt.rcParams["axes.unicode_minus"] = False

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.subplots as sp


from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from sqlalchemy import create_engine
import pymysql
import numpy as np
import os

import googleapiclient.discovery
from konlpy.tag import Okt

import jpype
from collections import Counter
from wordcloud import WordCloud
from datetime import datetime
from streamlit_option_menu import option_menu


# In[30]:


import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from sqlalchemy import create_engine
import pymysql

import matplotlib.pyplot as plt
import numpy as np
plt.rcParams['font.family'] = 'Malgun Gothic'

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

### 그래프 내에 한글이 포함된 경우 폰트 처리가 필요함
# - 한글 깨짐 방지를 위해서
### 폰트 환경설정 라이브러리
from matplotlib import font_manager, rc
plt.rc("font", family = "Malgun Gothic")
### Mac
# plt.rc("font", family = "AppleGothic")

### 그래프 내에 마이너스(-) 표시 기호 적용하기
plt.rcParams["axes.unicode_minus"] = False

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

### 그래프 내에 한글이 포함된 경우 폰트 처리가 필요함
# - 한글 깨짐 방지를 위해서
### 폰트 환경설정 라이브러리
from matplotlib import font_manager, rc
plt.rc("font", family = "Malgun Gothic")
### Mac
# plt.rc("font", family = "AppleGothic")

### 그래프 내에 마이너스(-) 표시 기호 적용하기
plt.rcParams["axes.unicode_minus"] = False
import pandas as pd
import os

import googleapiclient.discovery
from konlpy.tag import Okt

import jpype
from collections import Counter
from wordcloud import WordCloud


# In[42]:


# this data is from data extracted from a database

def step1_func():
    ## total_energy()
    # 데이터 불러오기 1
    file_path = "./data/신·재생에너지_발전량_비재생폐기물_제외.csv"
    energy_output = pd.read_csv(file_path)
    
    # 데이터 전처리
    # 각각의 신재생에너지를 하위요소로 나눈 것을 삭제 
    total_energy_output = energy_output["에너지원별(3)"] == "소계"
    total_energy_output = energy_output[total_energy_output]
    
    # 사용하지 않는 행 삭제
    exclude = [1,2,3,6]
    total_energy_output = total_energy_output.drop(index=exclude)
    
    # 사용하지 않는 컬럼 삭제
    total_energy_output = total_energy_output.loc[:, total_energy_output.columns != '에너지원별(1)']
    total_energy_output = total_energy_output.loc[:, total_energy_output.columns != '에너지원별(3)']
    total_energy_output = total_energy_output.loc[:, total_energy_output.columns != '에너지원별(4)']
    
    total_energy_output.replace('-', 0, inplace=True)
    total_energy_output = total_energy_output.reset_index(drop=True)
    
    # 데이터 불러오기 2
    file_path = "./data/신·재생에너지_보급용량_발전신규.csv"
    supply_energy = pd.read_csv(file_path)
    
    ### 데이터 전처리
    # 각각의 신재생에너지를 하위요소로 나눈 것을 삭제 
    total_supply_energy = supply_energy["에너지원별(3)"] == "소계"
    total_supply_energy = supply_energy[total_supply_energy]
    
    # 사용하지 않는 컬럼 삭제
    total_supply_energy = total_supply_energy.loc[:, total_supply_energy.columns != '에너지원별(1)']
    total_supply_energy = total_supply_energy.loc[:, total_supply_energy.columns != '에너지원별(3)']
    total_supply_energy = total_supply_energy.loc[:, total_supply_energy.columns != '에너지원별(4)']
    
    # 사용하지 않는 행 삭제
    exclude = [1,2,3,6]
    total_supply_energy = total_supply_energy.drop(index=exclude)
    total_supply_energy.replace('-', 0, inplace=True)
    total_supply_energy = total_supply_energy.reset_index(drop=True)
    
    ## 체크박스 생성
    check1 = st.checkbox('연도별 신재생에너지 발전량 그래프 보기', value=True)
    check2 = st.checkbox('연도별 신재생에너지 보급현황 그래프 보기', value=True)

    fig = go.Figure()   
    
    if check1:
        years = total_energy_output.columns[1:]
        subset = total_energy_output[total_energy_output['에너지원별(2)'] == "소계"]
        values = subset.iloc[:, 1:].values.astype(float)
        fig.add_trace(go.Bar(x=years,
                             y=values.flatten(),
                             name="발전량"))
    
        
    if check2:
        years = total_energy_output.columns[1:]
        subset = total_supply_energy[total_supply_energy['에너지원별(2)'] == "소계"]
        values = subset.iloc[:, 1:].values.astype(float).flatten()
        fig.add_trace(go.Scatter(x=years,
                                 y=values,
                                 mode='lines+markers',
                                 name='보급현황',
                                 marker_color='red'
                                ))
    
    fig.update_layout(xaxis={'title': '지역'},
                      yaxis={'title': '에너지'})
    
    # 그래프 제목 설정
    fig.update_layout(title_text="연도별 신재생에너지 발전량과 보급현황 비교(2012-2021)")
    
    # x축에 모든 연도가 나오게 설정
    fig.update_xaxes(dtick=1)
    
    # 그래프 보여주기
    st.plotly_chart(fig)
    
    st.text("""
    ⦁ 분석
    신재생에너지 발전량이 해마다 높아지는 반면, 실제로 보급되는 양은 현저히 낮게 나타났다. 
    이로 인해 미사용 된 전력량이 상당히 많을 것으로 예상된다. 
        """)
        
    # 1-3. 2021년 지역별 발전량과 전력소비량----------------------------------------------------------------------------------------------------
    st.info("1-3. 2021년 지역별 발전량과 전력소비량")
     ### 발전량 데이터 불러오기
    file_path = "./data/2021_지역별_신·재생에너지_발전량_비재생폐기물_제외.csv"
    regional_energy_output_2021 = pd.read_csv(file_path)

    # 데이터 전처리
    total_regional_energy_output_2021 = regional_energy_output_2021["에너지원별(3)"] == "소계"
    total_regional_energy_output_2021 = regional_energy_output_2021[total_regional_energy_output_2021]
    exclude = [1,2,3,6]
    total_regional_energy_output_2021 = total_regional_energy_output_2021.drop(index=exclude)
    total_regional_energy_output_2021 = total_regional_energy_output_2021.loc[:, total_regional_energy_output_2021.columns != '에너지원별(1)']
    total_regional_energy_output_2021 = total_regional_energy_output_2021.loc[:, total_regional_energy_output_2021.columns != '에너지원별(3)']
    total_regional_energy_output_2021 = total_regional_energy_output_2021.loc[:, total_regional_energy_output_2021.columns != '에너지원별(4)']
    total_regional_energy_output_2021 = total_regional_energy_output_2021.loc[:, total_regional_energy_output_2021.columns != '시점']
    total_regional_energy_output_2021 = total_regional_energy_output_2021.loc[:, total_regional_energy_output_2021.columns != '전국']
    total_regional_energy_output_2021.replace('-', 0, inplace=True)
    total_regional_energy_output_2021 = total_regional_energy_output_2021.reset_index(drop=True)
    
    # 데이터 전처리
    # 각각의 신재생에너지를 하위요소로 나눈 것을 삭제 
    total_regional_energy_output_2021 = regional_energy_output_2021["에너지원별(2)"] == "소계"
    total_regional_energy_output_2021 = regional_energy_output_2021[total_regional_energy_output_2021]
    
    total_regional_energy_output_2021 = total_regional_energy_output_2021.loc[:, total_regional_energy_output_2021.columns != '에너지원별(2)']
    total_regional_energy_output_2021 = total_regional_energy_output_2021.loc[:, total_regional_energy_output_2021.columns != '에너지원별(3)']
    total_regional_energy_output_2021 = total_regional_energy_output_2021.loc[:, total_regional_energy_output_2021.columns != '에너지원별(4)']
    total_regional_energy_output_2021 = total_regional_energy_output_2021.loc[:, total_regional_energy_output_2021.columns != '시점']
    total_regional_energy_output_2021 = total_regional_energy_output_2021.loc[:, total_regional_energy_output_2021.columns != '전국']
    df_transposed = total_regional_energy_output_2021.transpose()

    result_df = pd.DataFrame(columns=["지역", "신재생 발전량"])
    result_df["지역"] = total_regional_energy_output_2021.columns[1:]
    result_df["신재생 발전량"] = total_regional_energy_output_2021.iloc[0, 1:].values
    
    result_df = result_df.astype({"신재생 발전량" : "int"})

    ### 지역별_전력소비량
    file_path = "./data/regional_power_consumption.txt"
    regional_power_consumption_2021 = pd.read_csv(file_path,
                         ### 구분자 알려주기
                        delimiter = "\t",
                        names=["region", "power_consumption"])

    ### 컬럼명 한글로 바꾸기
    # 컬럼명 변경
    new_columns = {'region': '지역', 'power_consumption': '전력소비량'}
    regional_power_consumption_2021.rename(columns=new_columns, inplace=True)

    total_regional_energy_2021 = pd.merge(left=result_df,
                                          right=regional_power_consumption_2021,
                                          how="left",
                                          left_on="지역",
                                          right_on="지역")
    total_regional_energy_2021["신재생 발전 비율(%)"] = (total_regional_energy_2021["신재생 발전량"] / total_regional_energy_2021["전력소비량"]) * 100
    
    # 두 개의 y축을 가진 subplot 생성
    # 체크박스 생성
    check1 = st.checkbox('전력소비량 그래프 보기', value=True)
    check2 = st.checkbox('신재생 발전량 그래프 보기', value=True)
    
    # 두 개의 y축을 가진 subplot 생성
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # 첫 번째 그래프 (전력소비량) 추가, 막대그래프로 표현
    if check1:
        fig.add_trace(
            go.Bar(x=total_regional_energy_2021['지역'], y=total_regional_energy_2021['전력소비량'], name='전력소비량'),
            secondary_y=False,
        )
    
    # 두 번째 그래프 (신재생 발전량) 추가
    if check2:
        fig.add_trace(
            go.Scatter(x=total_regional_energy_2021['지역'], y=total_regional_energy_2021['신재생 발전량'], name='신재생 발전량'),
            secondary_y=True,
        )
    
    # x축 제목 설정
    fig.update_xaxes(title_text="지역")
    
    # y축 제목 설정
    fig.update_yaxes(title_text="전력소비량", secondary_y=False)
    fig.update_yaxes(title_text="신재생 발전량", secondary_y=True)
    
    # 그래프 제목 설정
    fig.update_layout(title_text="2021년 지역별 신재생에너지 발전량과 전력소비량")

    # 그래프 출력
    st.plotly_chart(fig)

    st.text("""
    ⦁ 분석
    신재생에너지의 발전량을 전력소비량과 비교해 보았을 때, 일부 지역에서는 상대적으로 낮은 전력소비량이 나타났다.
    이를 통해 사용되지 않는 전력, 즉 잉여 전력이 발생하는 것으로 보인다.
        """)

    # 1-4 2019년 지역별 신재생에너지 잉여전력-------------------------------------------------------------------------
    st.info("1-4. 2019년 지역별 신재생에너지 잉여전력")

    # 데이터 불러오기
    file_path = "./data/한국전력공사_법정동별_상계거래_잉여전력량_20191231.csv"
    ing = pd.read_csv(file_path, encoding="euc-kr")

    # 데이터 전처리
    df = pd.DataFrame(columns=["시도","잉여전력량"])
    df["시도"] = ing["시도"]
    df["잉여전력량"] = ing["잉여전력량"]
    df_g = df.groupby("시도").sum().reset_index()
    df_g["시도"] = ["강원","경기","경남","경북","광주","대구","대전","부산","서울","세종","울산","인천","전남","전북","제주","충남","충북"]

    all_df = pd.DataFrame(columns=["시도", "잉여전력량(MWh)"])

    all_df["시도"] = ing["시도"]
    # - KWh -> MWh
    all_df["잉여전력량(MWh)"] = ing["잉여전력량"] / 1000
    
    # 그룹화
    sum_df = all_df.groupby("시도")["잉여전력량(MWh)"].sum().reset_index()
    sum_df.sum()
    
    # 잉여전력량 총합 - 반올림 - 정수처리
    sum_all_region = all_df["잉여전력량(MWh)"].sum().round().astype(int)
    sum_all_region.astype(str)
    
    # 임계값 설정 (예: 전체의 3%)
    threshold = 0.03 * sum_all_region
    
    # 임계값 이하인 지역을 '기타'로 변경
    sum_df['시도'] = sum_df.apply(lambda row: row['시도'] if row['잉여전력량(MWh)'] >= threshold else '기타', axis=1)
    
    # '기타'로 변경된 지역의 잉여전력량 합계 재계산
    sum_df = sum_df.groupby('시도')['잉여전력량(MWh)'].sum().reset_index()
    
    # 파이 차트 생성
    labels = sum_df['시도'].values
    values = sum_df['잉여전력량(MWh)'].values
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.8)])
    fig.update_layout(
        title_text="2019년 총 잉여전력량 및 지역별 비율",
        annotations=[
            dict(text='총 잉여전력량', showarrow=False, x=0.5, y=0.55, font=dict(size=20, color='black', family='Courier New, monospace')),
            dict(text=str(sum_all_region) + '(MWh)', showarrow=False, x=0.5, y=0.45, font=dict(size=20, color='black', family='Courier New, monospace'))
            ]
    )

    # 그래프 보여주기
    st.plotly_chart(fig)

    st.text("""
    ⦁ 분석
    2019년 한 해 동안 발생한 잉여 전력량은 약 1038000(MWh)에 이르렀는데, 이는 백만MWh를 넘는 엄청난 양의 잉여 전력량이 발생한 것으로 나타났다. 
        """) 
    return df_g

def step2_func(df_g):
        # 데이터 불러오기1
    file_path = "./data/지역별_신·재생에너지_발전량_비재생폐기물_제외__2019년_4_4분기__20231208092633.csv"
    df = pd.read_csv(file_path)

    # 데이터 전처리
    df["제주"] = df["제주"].str.replace("-", "0")
    jeju_df = pd.DataFrame(columns=["시점", "에너지원", "발전량(MWh)"])
    jeju_df["시점"] = df["시점"]
    jeju_df["에너지원"] = df["에너지원별(2)"]
    jeju_df["발전량(MWh)"] = df["제주"]
    jeju_df["에너지원"] = jeju_df["에너지원"].str.replace(" (MWh)", "").str.strip()

    # '발전량(MWh)' 열의 데이터 타입을 float에서 int로 변경
    jeju_df['발전량(MWh)'] = jeju_df['발전량(MWh)'].astype(float).astype(int)
    
    # 연도별로 발전량 합산
    grouped_df = jeju_df.groupby('시점')['발전량(MWh)'].sum().reset_index()

    # 데이터 불러오기2
    file_path = "./data/제주_신·재생에너지_보급용량_발전신규.csv"
    jeju_energy_supply_capacity = pd.read_csv(file_path)

    # 데이터 전처리
    total_jeju_energy_supply_capacity = jeju_energy_supply_capacity["에너지원별(3)"] == "소계"
    total_jeju_energy_supply_capacity = jeju_energy_supply_capacity[total_jeju_energy_supply_capacity]
    
    # 사용하지 않는 컬럼 삭제
    total_jeju_energy_supply_capacity = total_jeju_energy_supply_capacity.loc[:, total_jeju_energy_supply_capacity.columns != '에너지원별(1)']
    total_jeju_energy_supply_capacity = total_jeju_energy_supply_capacity.loc[:, total_jeju_energy_supply_capacity.columns != '에너지원별(3)']
    total_jeju_energy_supply_capacity = total_jeju_energy_supply_capacity.loc[:, total_jeju_energy_supply_capacity.columns != '사업/자가구분별(1)']

    total_jeju_energy_supply_capacity.replace('-', 0, inplace=True)
    total_jeju_energy_supply_capacity = total_jeju_energy_supply_capacity.reset_index(drop=True)
    
  
    ## 체크박스 생성
    check1 = st.checkbox('제주 지역 연도별 신재생에너지 발전량 그래프 보기', value=True)
    check2 = st.checkbox('제주 지역 연도별 신재생에너지 보급현황 그래프 보기', value=True)
    
    fig = go.Figure()
    
    if check1:
        # 막대 그래프 추가
        fig.add_trace(go.Bar(name='발전량', x=grouped_df['시점'], y=grouped_df['발전량(MWh)']))
    
    if check2:
        years = total_jeju_energy_supply_capacity.columns[1:]
        subset = total_jeju_energy_supply_capacity[total_jeju_energy_supply_capacity['에너지원별(2)'] == "소계"]
        values = subset.iloc[:, 1:].values.astype(float).flatten()
        fig.add_trace(go.Scatter(x=years,
                                 y=values,
                                 mode='lines+markers',
                                 name='보급현황',
                                 marker_color='red'
                                ))

    # 레이아웃 설정
    fig.update_layout(
        title_text="제주 지역 연도별 신재생에너지 발전량과 보급현황 비교(2012-2021)",
        xaxis_title='연도',
        yaxis_title='에너지',
        barmode='group'
    )
    
    # x축에 모든 연도가 나오게 설정
    fig.update_xaxes(dtick=1)
    
    # 그래프 보여주기
    st.plotly_chart(fig)

    st.text("""
    ⦁ 분석
    제주는에서의 신재생에너지 발전량은 증가하는 반면, 보급량은 큰 변화없이 낮은 수준을 보이는 것으로 나타났다.
    이러한 현상은 '제주 제 6차 지역에너지계획'의 시행에 따른 신재생에너지 보급 설비 확대가 주요 원인인 것으로 분석된다. 
        """)
    
    # 2-2 제주 지역 연도별 태양광에너지 발전량과 보급현황 비교------------------------------------------------------------------------
    st.info("2-2 제주 지역 연도별 태양광에너지 발전량과 보급현황 비교")

    sun_power = jeju_df[jeju_df['에너지원'] == '태양광']

    ## 체크박스 생성
    check1 = st.checkbox('제주 지역 연도별 태양광에너지 발전량 그래프 보기', value=True)
    check2 = st.checkbox('제주 지역 연도별 태양광에너지 보급현황 그래프 보기', value=True)
    
    fig = go.Figure()
    
    #그래프 그리기
    if check1:
        fig.add_trace(go.Bar(x=sun_power["시점"], y=sun_power["발전량(MWh)"], name='발전량', marker=dict(color='blue')))
    
    if check2:
        years = total_jeju_energy_supply_capacity.columns[1:]
        subset = total_jeju_energy_supply_capacity[total_jeju_energy_supply_capacity['에너지원별(2)'] == "태양광"]
        values = subset.iloc[:, 1:].values.astype(float).flatten()
        fig.add_trace(go.Scatter(x=years,
                                 y=values,
                                 mode='lines+markers',
                                 name='보급현황',
                                 marker_color='red'))
    
    fig.update_layout(
        title_text="제주 지역 연도별 태양광에너지 발전량과 보급현황 비교",
        xaxis=dict(
            title='연도',
            tickmode='array',
            tickvals=sun_power["시점"],
            ticktext=sun_power["시점"],
        ),
        yaxis_title='에너지량 (MWh)'
    )

    # 그래프 보여주기
    st.plotly_chart(fig)
   
    # 2-3 제주 지역 연도별 풍력에너지 발전량과 보급현황 비교------------------------------------------------------------------------
    st.info("2-3 제주 지역 연도별 풍력에너지 발전량과 보급현황 비교")
    
    wind_power = jeju_df[jeju_df['에너지원'] == '풍력']

    ## 체크박스 생성
    check1 = st.checkbox('제주 지역 연도별 풍력에너지 발전량 그래프 보기', value=True)
    check2 = st.checkbox('제주 지역 연도별 풍력에너지 보급현황 그래프 보기', value=True)
    fig = go.Figure()
    
    #그래프 그리기
    if check1:
        fig.add_trace(go.Bar(x=wind_power["시점"], y=wind_power["발전량(MWh)"], name='발전량', marker=dict(color='blue')))
    
    if check2:
        years = total_jeju_energy_supply_capacity.columns[1:]
        subset = total_jeju_energy_supply_capacity[total_jeju_energy_supply_capacity['에너지원별(2)'] == "풍력"]
        values = subset.iloc[:, 1:].values.astype(float).flatten()
        fig.add_trace(go.Scatter(x=years,
                                 y=values,
                                 mode='lines+markers',
                                 name='보급현황',
                                 marker_color='red'))
    
    fig.update_layout(
        title_text="제주 지역 연도별 풍력에너지 발전량과 보급현황 비교",
        xaxis=dict(
            title='연도',
            tickmode='array',
            tickvals=wind_power["시점"],
            ticktext=wind_power["시점"],
        ),
        yaxis_title='에너지량 (MWh)'
    )
    
    # 그래프 보여주기
    st.plotly_chart(fig)
    
    # 2-4 2015년부터 2023년 제주 풍력 출력 제한------------------------------------------------------------------------
    st.info("2-4. 연도별 제주 재생에너지 제어 횟수")
    curtailment_2015_2016 = pd.read_csv("./data/2015_2016_한국전력거래소_월별_시간별_제주_태양광_풍력_제어량_및_제어_횟수.csv", encoding="euc_kr")
    curtailment_2017_2022 = pd.read_csv("./data/2017_2022_한국전력거래소_월별_시간별_제주_태양광_풍력_제어량_및_제어_횟수.csv", encoding="euc_kr")
    curtailment_2023= pd.read_csv("./data/한국전력거래소_시간별_제주_태양광_풍력_제어량_및_제어횟수_20230923.csv", encoding="euc_kr")

    # 데이터 전처리
    wind_curtailment_2015_2016 = curtailment_2015_2016["구분"] == "풍력"
    wind_curtailment_2015_2016 = curtailment_2015_2016[wind_curtailment_2015_2016]
    wind_curtailment_2015_2016 = wind_curtailment_2015_2016.drop(wind_curtailment_2015_2016.columns[4:28], axis=1)
  
    wind_curtailment_2017_2022 = curtailment_2017_2022["구분"] == "풍력"
    wind_curtailment_2017_2022 = curtailment_2017_2022[wind_curtailment_2017_2022]
    wind_curtailment_2017_2022 = wind_curtailment_2017_2022.drop(wind_curtailment_2017_2022.columns[3:27], axis=1)
    
    # 문자열을 날짜 형식으로 변환
    wind_curtailment_2017_2022['기준일'] = pd.to_datetime(wind_curtailment_2017_2022['기준일'])
    
    # 연도만 추출하여 새로운 컬럼 생성
    wind_curtailment_2017_2022['연도'] = wind_curtailment_2017_2022['기준일'].dt.year
    wind_curtailment_2017_2022['일자'] = wind_curtailment_2017_2022['기준일'].dt.month * 100 + wind_curtailment_2017_2022['기준일'].dt.day
    
    # 기준일 컬럼 삭제
    wind_curtailment_2017_2022 = wind_curtailment_2017_2022.drop(wind_curtailment_2017_2022.columns[1], axis=1)
    
    # 컬럼 맞추기
    wind_curtailment_2017_2022 = wind_curtailment_2017_2022[['구분', '연도',	'일자', '연도별 시행회차', '총제어량']]

    # 2023 데이터 전처리
    wind_curtailment_2023 = curtailment_2023["구분"] == "풍력"
    wind_curtailment_2023 = curtailment_2023[wind_curtailment_2023]
    wind_curtailment_2023 = wind_curtailment_2023.drop(wind_curtailment_2023.columns[3:27], axis=1)
    
    # 문자열을 날짜 형식으로 변환
    wind_curtailment_2023['기준일'] = pd.to_datetime(wind_curtailment_2023['기준일'])
    
    # 연도만 추출하여 새로운 컬럼 생성
    wind_curtailment_2023['연도'] = wind_curtailment_2023['기준일'].dt.year
    wind_curtailment_2023['일자'] = wind_curtailment_2023['기준일'].dt.month * 100 + wind_curtailment_2023['기준일'].dt.day
    
    # 기준일 컬럼 삭제
    wind_curtailment_2023 = wind_curtailment_2023.drop(wind_curtailment_2023.columns[1], axis=1)
    
    # 컬럼 맞추기
    wind_curtailment_2023 = wind_curtailment_2023[['구분', '연도', '일자', '연도별 시행회차', '총제어량']]
    
    # 데이터프레임 중복제거하고 합치기
    wind_curtailment_2015_2023 = pd.concat([wind_curtailment_2015_2016, wind_curtailment_2017_2022]).drop_duplicates(subset=['연도', '연도별 시행회차'])
    wind_curtailment_2015_2023 = pd.concat([wind_curtailment_2015_2023, wind_curtailment_2023]).drop_duplicates(subset=['연도', '연도별 시행회차'])

    # 데이터프레임 오름차순 정렬
    wind_curtailment_2015_2023 = wind_curtailment_2015_2023.sort_values(by=['연도', '연도별 시행회차'])

    # 연도별로 그룹화
    wind_curtailment_2015_2023 = wind_curtailment_2015_2023.groupby('연도').agg({'총제어량': 'sum', '연도별 시행회차': 'count'}).reset_index()
    wind_curtailment_2015_2023 = wind_curtailment_2015_2023.rename(columns={'총제어량': '연도별 총제어량', '연도별 시행회차': '연도별 시행 횟수'})

    # 2017_2022 데이터 전처리
    solar_curtailment_2017_2022 = curtailment_2017_2022["구분"] == "태양광"
    solar_curtailment_2017_2022 = curtailment_2017_2022[solar_curtailment_2017_2022]
    solar_curtailment_2017_2022 = solar_curtailment_2017_2022.drop(solar_curtailment_2017_2022.columns[3:28], axis=1)
    
    # 문자열을 날짜 형식으로 변환
    solar_curtailment_2017_2022['기준일'] = pd.to_datetime(solar_curtailment_2017_2022['기준일'])
    
    # 연도만 추출하여 새로운 컬럼 생성
    solar_curtailment_2017_2022['연도'] = solar_curtailment_2017_2022['기준일'].dt.year
    
    # 기준일 컬럼 삭제
    solar_curtailment_2017_2022 = solar_curtailment_2017_2022.drop(solar_curtailment_2017_2022.columns[1], axis=1)
    
    # 컬럼 맞추기
    solar_curtailment_2017_2022 = solar_curtailment_2017_2022[['구분', '연도', '연도별 시행회차']]

    # 2023 데이터 전처리
    solar_curtailment_2023 = curtailment_2023["구분"] == "태양광"
    solar_curtailment_2023 = curtailment_2023[solar_curtailment_2023]
    solar_curtailment_2023 = solar_curtailment_2023.drop(solar_curtailment_2023.columns[3:29], axis=1)
    
    # 문자열을 날짜 형식으로 변환
    solar_curtailment_2023['기준일'] = pd.to_datetime(solar_curtailment_2023['기준일'])
    
    # 연도만 추출하여 새로운 컬럼 생성
    solar_curtailment_2023['연도'] = solar_curtailment_2023['기준일'].dt.year
    
    # 기준일 컬럼 삭제
    solar_curtailment_2023 = solar_curtailment_2023.drop(solar_curtailment_2023.columns[1], axis=1)
    
    # 컬럼 맞추기
    solar_curtailment_2023 = solar_curtailment_2023[['구분', '연도', '연도별 시행회차']]

    solar_curtailment_total = pd.concat([solar_curtailment_2017_2022, solar_curtailment_2023], axis=0, ignore_index=True)

    solar_curtailment_total = solar_curtailment_total.groupby('연도').agg({'연도별 시행회차': 'count'}).reset_index()

    solar_curtailment_total = solar_curtailment_total.rename(columns={'연도별 시행회차': '연도별 시행 횟수'})

    # 체크박스 추가
    options = st.multiselect('그래프 선택', ['풍력 제어 시행 횟수', '태양광 제어 시행 횟수'], ['풍력 제어 시행 횟수', '태양광 제어 시행 횟수'])
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    if '풍력 제어 시행 횟수' in options:
        fig.add_trace(go.Scatter(x=wind_curtailment_2015_2023['연도'],
                                 y=wind_curtailment_2015_2023['연도별 시행 횟수'],
                                 name='풍력 제어 시행 횟수', mode='lines+markers+text',
                                 text=wind_curtailment_2015_2023['연도별 시행 횟수'],
                                 textposition='top center'),
                      secondary_y=False)
        
    if '태양광 제어 시행 횟수' in options:
        fig.add_trace(go.Scatter(x=solar_curtailment_total['연도'],
                                 y=solar_curtailment_total['연도별 시행 횟수'],
                                 name='태양광 제어 시행 횟수', mode='lines+markers+text',
                                 text=solar_curtailment_total['연도별 시행 횟수'],
                                 textposition='top center', line=dict(color='red')),
                      secondary_y=True)
    
    fig.update_layout(title_text="연도별 제주 재생에너지 제어 횟수")
    fig.update_xaxes(dtick=1)
        
    # 그래프 출력
    st.plotly_chart(fig)

    st.text("""
    ⦁ 분석
    제주의 태양광, 풍력 등 신재생에너지 보급용량이 급속도로 늘어나면서, 정부의 지시에 따른 재생에너지 출력제한 횟수가 증가하는 추세로 분석된다.
    이는 변동성 큰 재생에너지인 태양광과 풍력의 출력량 예측이 어려워져 전력 수급 균형과 전력계통의 안정 유지가 어려워지기 때문인 것으로 보인다.
        """)
     
    # 2-5 2019년 지역별 신재생에너지 손실액-------------------------------------------------------------------------
    st.info("2-5. 2019년 지역별 신재생에너지 손실액")

    # 데이터 불러오기
    df = pd.read_csv("./data/신재생에너지_정산단가_20231212155541.csv")

    df_2019 = df[df['시점'] == '2019']
    df_2019 = df_2019.loc[:, df_2019.columns != '시점']
    df_2019 = df_2019.reset_index(drop=True)
    # 0번째 행의 값들로 평균 계산
    average_values = round(df_2019.iloc[0, 0:].astype(float).mean(), )
    df_g["손실액"] = df_g["잉여전력량"] * average_values

    # 첫 번째 그래프 생성
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_g["시도"], y=df_g[df_g.columns[1]], name='잉여전력량'))
    
    # 두 번째 그래프 추가
    fig.add_trace(go.Line(x=df_g["시도"], y=df_g[df_g.columns[2]], name='손실액', yaxis='y2', mode='lines+markers', marker_color='red' ))
    
    # y축 설정 (오른쪽 y축을 두 번째 그래프에 맞춤)
    fig.update_layout(
        yaxis=dict(
            title='잉여전력량'
        ),
        yaxis2=dict(
            title='손실액',
            titlefont=dict(
                color='red'
            ),
            tickfont=dict(
                color='red'
            ),
            overlaying='y',
            side='right'
        )
    )
    
    # 그래프 제목 설정
    fig.update_layout(title_text='잉여전력량과 손실액')

    
    # 그래프 출력
    st.plotly_chart(fig)

    st.text("""
        ⦁ 분석
        잉여 전력량의 발생으로 인해 전국적으로 큰 손실액이 발생하고 있음이 나타났다.
            """)

    file_path = "./data/한국전력공사_법정동별_상계거래_잉여전력량_20191231.csv"
    ing = pd.read_csv(file_path, encoding="euc-kr")

    df = pd.DataFrame(columns=["시도","잉여전력량","손실액"])
    df["시도"] = ing["시도"]
    df["잉여전력량"] = ing["잉여전력량"]
    df_g = df.groupby("시도").sum().reset_index()
    df_g["시도"] = ["강원","경기","경남","경북","광주","대구","대전","부산","서울","세종","울산","인천","전남","전북","제주","충남","충북"]
    df_g["손실액"] = df_g["잉여전력량"]*81
    df_g = df_g.loc[:, df_g.columns != '잉여전력량'].copy()

    # 잉여전력량 총합 - 반올림 - 정수처리
    sum_all_region = df_g["손실액"].sum()
    
    # 임계값 설정 (예: 전체의 3%)
    threshold = 0.03 * sum_all_region
    
    # 임계값 이하인 지역을 '기타'로 변경
    df_g['시도'] = df_g.apply(lambda row: row['시도'] if row['손실액'] >= threshold else '기타', axis=1)
    
    # '기타'로 변경된 지역의 잉여전력량 합계 재계산
    df_g = df_g.groupby('시도')['손실액'].sum().reset_index()
    
    # 파이 차트 생성
    labels = df_g['시도'].values
    values = df_g['손실액'].values
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.8)])
    fig.update_layout(
        title_text="2019년 잉여전력으로 인한 지역별 손실액",
        annotations=[
             dict(text='총 손실액', showarrow=False, x=0.5, y=0.55, font=dict(size=20, color='black', family='Courier New, monospace')),
            dict(text=str(sum_all_region) + '원', showarrow=False, x=0.5, y=0.45, font=dict(size=20, color='black', family='Courier New, monospace'))
            ]
    )

    # 그래프 출력
    st.plotly_chart(fig)

    st.text("""
        ⦁ 분석
        잉여 전력으로 인한 2019년 한 해 총 손실액은 약 841억원으로 분석되었다.
        이런 막대한 손실액이 발생하는 것으로 보아 정부에서는 잉여 전력을 활용할 수 있는 다양한 방안을 적극적으로 모색하고 있을 것으로 예상된다.
            """)


def tab5_func():
    file_path = "./data/신·재생에너지_발전량_비재생폐기물_제외.csv"
    energy_output = pd.read_csv(file_path)
    
    # 데이터 전처리
    # 각각의 신재생에너지를 하위요소로 나눈 것을 삭제 
    total_energy_output = energy_output["에너지원별(3)"] == "소계"
    total_energy_output = energy_output[total_energy_output]
    
    # 사용하지 않는 행 삭제
    exclude = [1,2,3,6]
    total_energy_output = total_energy_output.drop(index=exclude)
    
    # 사용하지 않는 컬럼 삭제
    total_energy_output = total_energy_output.loc[:, total_energy_output.columns != '에너지원별(1)']
    total_energy_output = total_energy_output.loc[:, total_energy_output.columns != '에너지원별(3)']
    total_energy_output = total_energy_output.loc[:, total_energy_output.columns != '에너지원별(4)']
    
    total_energy_output.replace('-', 0, inplace=True)
    total_energy_output = total_energy_output.reset_index(drop=True)

    file_path = "./data/신·재생에너지_보급용량_발전신규.csv"
    supply_energy = pd.read_csv(file_path)
    
    ### 데이터 전처리
    # 각각의 신재생에너지를 하위요소로 나눈 것을 삭제 
    total_supply_energy = supply_energy["에너지원별(3)"] == "소계"
    total_supply_energy = supply_energy[total_supply_energy]
    
    # 사용하지 않는 컬럼 삭제
    total_supply_energy = total_supply_energy.loc[:, total_supply_energy.columns != '에너지원별(1)']
    total_supply_energy = total_supply_energy.loc[:, total_supply_energy.columns != '에너지원별(3)']
    total_supply_energy = total_supply_energy.loc[:, total_supply_energy.columns != '에너지원별(4)']
    
    # 사용하지 않는 행 삭제
    exclude = [1,2,3,6]
    total_supply_energy = total_supply_energy.drop(index=exclude)
    total_supply_energy.replace('-', 0, inplace=True)
    total_supply_energy = total_supply_energy.reset_index(drop=True)
    
    file_path = "./data/지역별_신·재생에너지_발전량_비재생폐기물_제외__2019년_4_4분기__20231208092411.csv"
    gj_energy = pd.read_csv(file_path)


    
    # 데이터 전처리
    new_gj_energy = gj_energy.loc[:, gj_energy.columns != '에너지원별(1)'].copy()
    new_gj_energy["광주"] = new_gj_energy["광주"].replace("-",0) 
    
    # 그래프 그리기
    fig = go.Figure()
    
    new_gj_energy["광주"] = new_gj_energy["광주"].astype(int)
    
    df_yearly = new_gj_energy.pivot(index="시점", columns="에너지원별(2)", values="광주")
    
    # 각 열별로 선 그래프 그리기
    for col in df_yearly.columns:
        fig.add_trace(go.Scatter(
            x=df_yearly.index,
            y=df_yearly[col],
            mode='lines+markers',  # 선 그래프와 마커 동시에 표시
            name=col
        ))
    
    # 그래프 제목 설정
    fig.update_layout(title_text="광주 신재생에너지 발전량")
    
    # x축, y축 제목 설정
    fig.update_xaxes(title_text="년도")
    fig.update_yaxes(title_text="에너지량(MWh)")
    
    # x축에 모든 연도가 나오게 설정
    fig.update_xaxes(dtick=1)
    
    # 그래프 보여주기
    st.plotly_chart(fig)
        
    ### 2. 광주 토지 이용현황 -------------------------------------------------------------------------------------------
    st.info("2. 광주 토지 이용현황")
    data = [137.42, 23.1, 238.47, 102.19]
    labels = ['기개발지', '개발가능지역', '개발억제지', '개발불능지역']
    
    # 그래프 객체 생성
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=data,
        textinfo='label',
        hole=.3,  # 도넛 차트로 만들기 위한 설정, 필요없다면 삭제
        rotation=90,  # 시작 각도 설정
    )])
    
    # 그래프 제목 설정
    fig.update_layout(title_text="광주 토지 이용 현황")
    
    # 그래프 보여주기
    st.plotly_chart(fig)
    
    # 3. 신재생에너지 발전량 비율-----------------------------------------------------------------------------------------------------
    st.info("3. 연도별 신재생에너지 발전량 비율")
    # 연도 리스트
    years = [str(year) for year in range(2021, 2011, -1)]
    
    # 드롭다운 메뉴 생성
    selected_year = st.selectbox('신재생에너지 발전량 비율을 알고싶은 연도를 선택하세요:', years)
    
    # 선택된 연도의 데이터만 선택
    data_selected_year = total_energy_output[['에너지원별(2)', selected_year]]
    
    # 그래프 객체 생성
    fig = go.Figure(data=[go.Pie(
        labels=data_selected_year['에너지원별(2)'],
        values=data_selected_year[selected_year],
        textinfo='label',  # 각 조각에 라벨 표시
        hole=.3  # 도넛 차트로 만들기 위한 설정, 필요없다면 삭제
    )])
    
    # 그래프 제목 설정
    fig.update_layout(title_text=f"{selected_year}년 신재생에너지 발전량 비율")
    
    # 그래프 출력
    st.plotly_chart(fig)
        
    # 4.신재생에너지 보급현황 비율-------------------------------------------------------------------------------
    st.info("4. 연도별 신재생에너지 보급현황 비율")
    # 연도 리스트
    years = [str(year) for year in range(2021, 2011, -1)]
    
    # 드롭다운 메뉴 생성
    selected_year = st.selectbox('신재생에너지 보급현황 비율을 알고싶은 연도를 선택하세요:', years)
    
    # 선택된 연도의 데이터만 선택
    data_selected_year = total_supply_energy[['에너지원별(2)', selected_year]]
    
    # 그래프 객체 생성
    fig = go.Figure(data=[go.Pie(
        labels=data_selected_year['에너지원별(2)'],
        values=data_selected_year[selected_year],
        textinfo='label',  # 각 조각에 라벨 표시
        hole=.3  # 도넛 차트로 만들기 위한 설정, 필요없다면 삭제
    )])
    
    # 그래프 제목 설정
    fig.update_layout(title_text=f"{selected_year}년 신재생에너지 보급현황 비율")
    
    
    # 그래프 출력
    st.plotly_chart(fig)
    
    # 5. 2021년 지역별 신재생에너지 발전량과 보급현황 비교---------------------------------------------------------------------------
    st.info("5. 2021년 지역별 신재생에너지 발전량과 보급현황 비교")
    
    ### 보급현황 데이터 불러오기
    file_path = "./data/2021_지역별_신·재생에너지_보급용량_발전누적.csv"
    energy_supply_capacity = pd.read_csv(file_path)
    
    # 데이터 전처리
    regional_energy_supply_capacity = energy_supply_capacity["에너지원별(3)"] == "소계"
    regional_energy_supply_capacity = energy_supply_capacity[regional_energy_supply_capacity]
    regional_energy_supply_capacity = regional_energy_supply_capacity.loc[:, regional_energy_supply_capacity.columns != '에너지원별(1)']
    regional_energy_supply_capacity = regional_energy_supply_capacity.loc[:, regional_energy_supply_capacity.columns != '에너지원별(3)']
    regional_energy_supply_capacity = regional_energy_supply_capacity.loc[:, regional_energy_supply_capacity.columns != '사업/자가구분별(1)']
    regional_energy_supply_capacity = regional_energy_supply_capacity.loc[:, regional_energy_supply_capacity.columns != '전국']
    regional_energy_supply_capacity = regional_energy_supply_capacity.loc[:, regional_energy_supply_capacity.columns != '시점']
    regional_energy_supply_capacity.replace('-', 0, inplace=True)
    regional_energy_supply_capacity = regional_energy_supply_capacity.reset_index(drop=True)
    
    # regional_energy_supply_capacity
    
    ### 발전량 데이터 불러오기
    file_path = "./data/2021_지역별_신·재생에너지_발전량_비재생폐기물_제외.csv"
    regional_energy_output_2021 = pd.read_csv(file_path)
    
    # 데이터 전처리
    total_regional_energy_output_2021 = regional_energy_output_2021["에너지원별(3)"] == "소계"
    total_regional_energy_output_2021 = regional_energy_output_2021[total_regional_energy_output_2021]
    exclude = [1,2,3,6]
    total_regional_energy_output_2021 = total_regional_energy_output_2021.drop(index=exclude)
    total_regional_energy_output_2021 = total_regional_energy_output_2021.loc[:, total_regional_energy_output_2021.columns != '에너지원별(1)']
    total_regional_energy_output_2021 = total_regional_energy_output_2021.loc[:, total_regional_energy_output_2021.columns != '에너지원별(3)']
    total_regional_energy_output_2021 = total_regional_energy_output_2021.loc[:, total_regional_energy_output_2021.columns != '에너지원별(4)']
    total_regional_energy_output_2021 = total_regional_energy_output_2021.loc[:, total_regional_energy_output_2021.columns != '시점']
    total_regional_energy_output_2021 = total_regional_energy_output_2021.loc[:, total_regional_energy_output_2021.columns != '전국']
    total_regional_energy_output_2021.replace('-', 0, inplace=True)
    total_regional_energy_output_2021 = total_regional_energy_output_2021.reset_index(drop=True)
    
    # total_regional_energy_output_2021
    
    # 데이터 프레임에서 '에너지원별(2)' 열을 제외한 나머지 열을 가져옵니다.
    regions1 = total_regional_energy_output_2021.columns[1:]
    regions2 = regional_energy_supply_capacity.columns[1:]
    
    # '에너지원별(2)' 열의 첫 번째 행 (소계)의 값을 가져옵니다.
    values1 = total_regional_energy_output_2021.loc[0, regions1].values
    values2 = regional_energy_supply_capacity.loc[0, regions2].values
    
    # 지역 리스트
    regions = total_regional_energy_output_2021.columns[1:].tolist()
    
    st.subheader('2021년 신재생에너지 발전량을 더 자세히 보고싶다면?')
    # 드롭다운 메뉴 생성
    selected_region = st.selectbox('2021년 신재생에너지 발전량을 알고싶은 지역을 선택하세요:', regions)
    
    # 선택된 지역의 데이터만 선택
    data_selected_region = total_regional_energy_output_2021[selected_region]
    
    # 그래프 객체 생성
    fig = go.Figure()
    
    # 에너지 타입별로 데이터 그룹화 및 그래프 생성
    for energy_type in total_regional_energy_output_2021['에너지원별(2)'].unique():
        subset = total_regional_energy_output_2021[total_regional_energy_output_2021['에너지원별(2)'] == energy_type]
        fig.add_trace(go.Bar(
            x=subset['에너지원별(2)'],
            y=subset[selected_region],
            name=energy_type
        ))
    
    # 그래프 설정
    fig.update_layout(
        barmode='stack',
        title_text=f"{selected_region} 지역의 2021년 신재생에너지 발전량",
        xaxis_title="에너지원별",
        yaxis_title="에너지 발전량"
    )
    
    # 그래프 출력
    st.plotly_chart(fig)
    
    # 6. 2021년 지역별 신재생에너지 보급현황 비율---------------------------------------------------------------------------
    st.info("6. 2021년 지역별 신재생에너지 보급현황 비율")
    
    # 지역 리스트
    regions = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', '경기지역', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주']
    
    # 드롭다운 메뉴 생성
    selected_region = st.selectbox('지역을 선택하세요:', regions)
    
    # 선택된 지역 데이터를 숫자로 변환
    regional_energy_supply_capacity[selected_region] = pd.to_numeric(regional_energy_supply_capacity[selected_region])
    
    # 비율이 1% 이상인 데이터만 필터링
    filtered_data = regional_energy_supply_capacity[regional_energy_supply_capacity[selected_region]/regional_energy_supply_capacity[selected_region].sum() > 0.01]
    
    # 파이 차트 생성
    fig = go.Figure(data=[go.Pie(
        labels=filtered_data['에너지원별(2)'],
        values=filtered_data[selected_region],
        hole=.3
    )])
    
    # 차트 제목 설정
    fig.update_layout(
        title_text=f"2021년 {selected_region} 신재생 에너지보급현황 비율"
    )
    
    # 차트 출력
    st.plotly_chart(fig)
    
    # 16 2023년 전국 풍력발전소 ---------------------------------------------------------------------------
    st.info("16. 2023년 전국 풍력발전소")
    df = pd.read_csv("./data/전국풍력발전소현황정보(2023년).csv")
    
    st.map(df, latitude='wgs84_lltd_ycrd', longitude='wgs84_lltd_xcrd')
    



### ------- STEP 3  




    
def Gwangju_data():
    
    st.text( "🌐📊Data extracted from [Data.go.kr](https://www.data.go.kr/) 💡🔍)")
    file_path = "./data/광주광역시_신재생에너지보급_현황_20220916.csv"
    df= pd.read_csv(file_path, encoding = "euc-kr") 
    return df

def gwangju_status(grouped_data):
    colors = sns.color_palette('husl', n_colors=len(grouped_data))
    plt.figure(figsize=(8, 5))
    sns.color_palette("rocket", as_cmap=True)
    sns.barplot(grouped_data, x='시군구', y='발전소_개수',  hue='시군구', dodge=False, err_kws={'color': '0.2'}, capsize=0.2, legend=False, palette=colors)
    # sns.lineplot(grouped_data, x='시군구', y='발전소_개수', estimator="max", errorbar=None)
    plt.xlabel('시군구', fontweight="bold")
    plt.ylabel('발전소_개수', fontweight="bold")
    plt.title('Number of Power Plants by District', fontsize=17, fontweight="bold")
    plt.xticks(ha='right')
    plt.tight_layout()
# Save the plot
    plt.savefig("./img/영화별 평점 평균 막대그래프.png")
    plt.show()
    st.pyplot(plt)
        
def data_cleaning(df):    
    # st.info("Total of 350 cells in the dataset contained null values. They have been handled accordingly.")
    df_new = df.copy()
    df_new['사업개시일자'] = df_new['사업개시일자'].fillna(df_new['허가일자'])
    df_new['허가일자'] = df_new['허가일자'].fillna(df_new['사업개시일자'])
    df_new.info()
    duplicated_rows = df_new[df_new.duplicated()]
    print("Rows with duplicated values:")
    print(duplicated_rows.sort_values(by='데이터기준일자'))
    num_duplicated_rows = df_new.duplicated().sum()
    df_new['허가일자'] = pd.to_datetime(df_new['허가일자'],errors='coerce')
    df_new['사업개시일자'] = pd.to_datetime(df_new['사업개시일자'], errors='coerce')
    current_date = pd.to_datetime(datetime.now())
    future_mask = (df_new['허가일자'] > current_date) | (df_new['사업개시일자'] > current_date)
    future_mask.value_counts()
    df_new['사업개시일자'].fillna(df_new['허가일자'], inplace=True)
    null_rows = df_new[df_new['허가일자'].isnull() | df_new['사업개시일자'].isnull()]
    df_new.drop(df_new.loc[future_mask].index, inplace=True)
    save_path = "./data/gwangju_new_data.csv"    
    # df_new.to_csv(save_path, index=False)
    # save_path="./data/gwangju_new_data.csv"     
    return df_new

def grouped_data():
    save_path="./data/gwangju_new_data.csv"
    df2=pd.read_csv(save_path)
    grouped_result = df2.groupby('시군구').agg({'발전소명': 'count', '용량(kW)': 'sum'}).reset_index()
    grouped_result.columns = ['시군구', '발전소_개수', '총_용량']
    # grouped_result
    return grouped_result


def plot1(grouped_data):
    fig, axs = plt.subplots(1, 2, figsize=(15, 5))

    # Flatten the array of subplots
    axs = axs.flatten()
    
    # Define the data for each plot
    data = [('발전소_개수', grouped_data['발전소_개수'], 'b'), ('총_용량', grouped_data['총_용량'], 'r')]
    
    # Create a bar plot for each column
    for ax, (label, series, color) in zip(axs, data):
        ax.bar(grouped_data['시군구'], series, color=color, alpha=0.6, label=label)
        ax.set_xlabel('시군구')
        ax.set_ylabel(label, color=color)
        ax.tick_params('y', colors=color)
    
    # Display
    plt.tight_layout()
    plt.show()
    plt.savefig("./img/01.png")
    # st.info("""
    # The analysis results showcase the total count of power plants and the overall capacity in each 'City County' (시군구). This detailed breakdown provides valuable insights into the distribution of power generation resources across different regions.
    # """)
    st.pyplot(plt)

def plot1_analysis():
    
     selected_value = st.selectbox('Select the langue too view the analysis:', ['English','Korean'])
     if selected_value == 'English':
        st.text("""

        - The data analysis reveals significant variations in the distribution of power plants and their total capacity across different 'City County' (시군구).
        - 광산구 leads with a total of 1,038 power plants, contributing to a massive total capacity of 213,267.356 kW.  
        - Interestingly, 광산구 is known to have the largest land area and the lowest population density among all regions in Gwangju. 
        - This could be a contributing factor to its high number of power plants and total capacity, as larger land area may provide more space for power plant installations.
        - Contrarily, the 남구, 동구, 북구, and 서구 have substantially fewer power plants, with 54, 31, 377, and 154 respectively. 
        - Their total capacities are also relatively lower, with 남구 at 9,710.195 kW, 동구 at 2,868.405 kW, 북구 at 48,683.890 kW, and 서구 at 13,823.350 kW.
        - The disparity in the number of power plants and total capacity indicates potential areas for infrastructure development and investment, particularly in the 남구, 동구, and 서구 regions. 
        - Considering 광산구's example, a detailed study on the correlation between land area, population density, and the location of power plants could provide valuable insights for strategic planning and resource allocation.

        """)
     elif selected_value == 'Korean':
        st.text("""
                - 데이터 분석을 통해 다양한 '시 군'(시군구)에 걸쳐 발전소 분포와 총 용량에 상당한 차이가 있음이 드러났습니다.
         - 광구는 총 1,038개의 발전소를 보유하고 있으며, 총 용량 213,267.356kW의 막대한 발전에 기여하고 있습니다.
         - 흥미롭게도 광구는 광주 전체 지역 중 국토 면적이 가장 크고, 인구 밀도가 가장 낮은 것으로 알려져 있습니다.
         - 토지 면적이 넓을수록 발전소 설치 공간이 넓어지기 때문에 발전소 수와 총 용량이 많은 이유가 될 수 있습니다.
         - 이에 비해 남구, 동구, 북구, 서구는 각각 54기, 31기, 377기, 154기로 발전소 수가 상당히 적다.
         - 전체 용량도 남구 9,710.195kW, 동구 2,868.405kW, 북구 48,683.890kW, 서구 13,823.350kW로 상대적으로 낮다.
         - 발전소 수와 총 용량의 차이는 특히 남구, 동구, 서구 지역에서 인프라 개발 및 투자 잠재 지역을 나타냅니다.
         - 램프구의 사례를 고려해 볼 때, 토지 면적, 인구 밀도, 발전소 위치 간의 상관 관계에 대한 자세한 연구는 전략 계획 및 자원 배분에 대한 귀중한 통찰력을 제공할 수 있습니다.
                """)
    


def pichart(grouped_data):
    
    st.success("📊 Visualizing Power Plant Distribution in 'City County' Regions")
      
    colors = sns.color_palette('husl', n_colors=len(grouped_data))
    
    # Create a figure and a grid of subplots
    fig, axs = plt.subplots(1, 2, figsize=(15, 5))
    
    # Flatten the array of subplots
    axs = axs.flatten()
    
    # Define the data for each plot
    data = [('발전소_개수', grouped_data['발전소_개수']), ('총_용량', grouped_data['총_용량'])]
    
    # Create a pie chart for each column
    for ax, (label, series) in zip(axs, data):
        # Create a pie chart with custom colors and explode a slice
        explode = [0.1 if i == series.idxmax() else 0 for i in range(len(series))]
        ax.pie(series, labels=grouped_data['시군구'], autopct='%1.1f%%', colors=colors, explode=explode, startangle=90)
        ax.set_title(label)
    
    # Display
    plt.tight_layout()
    plt.legend()
    plt.savefig("./img/영화별 평점 평균 원형그래프.png")
    
    plt.show()
    st.pyplot(plt)

def various_p(df_new):
    # data = {'발전소_개수': grouped_data['발전소_개수'], '총_용량': grouped_data['총_용량']}
    # df_new['원동력종류'].value_counts()
    
    mylabels2=["태양광","연료전지", "소수력", "기력발전", "매립가스(LFG)", "증기터빈", "바이오가스"]
    counts= df_new['원동력종류'].value_counts()
    percentage= counts/counts.sum()*100
    plt.figure(figsize=(8, 4))
    plt.bar(mylabels2, percentage, color= 'skyblue')
    plt.xlabel("ff")
    plt.ylabel("dd")
    plt.title("hhh")
    plt.show()
    plt.savefig("./img/03.png")
    # st.info("""
    #     The following code segment generates a bar chart that visualizes the distribution of different types of 
    #     power sources ('원동력종류') in the data set. The types of power sources include '태양광', 
    #     '연료전지', '소수력', '기력발전', '매립가스(LFG)', '증기터빈', and '바이오가스'. 
    #     The y-axis represents the percentage of each power source type relative to the total number of power plants.
    #     This visualization aids in understanding the prevalence of different power sources in the data set.
    #     """)
    st.pyplot(plt)
    
def various_P_analysis():    
    selected_value = st.selectbox('Select the language of the analysis', ['English', 'Korean'])
    if selected_value == 'English':
        st.text("""
        1. The bar chart visualizes the distribution of different types of power sources ('원동력종류') used in the power plants. 
        2. The most prominent power source is '태양광' (solar power), which accounts for approximately 99.33% of the total. 
        3. This indicates a significant reliance on solar power for electricity generation in the regions under study.
        4. The other power sources, including '연료전지' (fuel cells), '소수력' (mini hydro), '기력발전' (steam turbine), 
           '매립가스(LFG)' (landfill gas), '증기터빈' (steam turbine), and '바이오가스' (biogas), each constitute 
           a very small fraction of the total, with percentages around or below 0.24%.
        5. This overwhelming dominance of solar power suggests that the regions could benefit from diversifying their 
           power sources to enhance energy security and resilience.
        6. However, it also reflects a strong commitment to renewable and environmentally friendly energy sources.
        """)
    elif selected_value == 'Korean':
        st.text("""
        1. 데이터 분석을 통해 다양한 '시 군'(시군구)에 걸쳐 발전소 분포와 총 용량에 상당한 차이가 있음이 드러났습니다.
        2. 광구는 총 1,038개의 발전소를 보유하고 있으며, 총 용량 213,267.356kW의 막대한 발전에 기여하고 있습니다.
        3. 흥미롭게도 광구는 광주 전체 지역 중 국토 면적이 가장 크고, 인구 밀도가 가장 낮은 것으로 알려져 있습니다.
        4. 토지 면적이 넓을수록 발전소 설치 공간이 넓어지기 때문에 발전소 수와 총 용량이 많은 이유가 될 수 있습니다.
        5. 이에 비해 남구, 동구, 북구, 서구는 각각 54기, 31기, 377기, 154기로 발전소 수가 상당히 적다.
        6. 전체 용량도 남구 9,710.195kW, 동구 2,868.405kW, 북구 48,683.890kW, 서구 13,823.350kW로 상대적으로 낮다.
        7. 발전소 수와 총 용량의 차이는 특히 남구, 동구, 서구 지역에서 인프라 개발 및 투자 잠재 지역을 나타냅니다.
        8. 램프구의 사례를 고려해 볼 때, 토지 면적, 인구 밀도, 발전소 위치 간의 상관 관계에 대한 자세한 연구는 
           전략 계획 및 자원 배분에 대한 귀중한 통찰력을 제공할 수 있습니다.
        """)


def logchart(df_new):
    mylabels2 = ["태양광", "연료전지", "소수력", "기력발전", "매립가스(LFG)", "증기터빈", "바이오가스"]
    counts = df_new['원동력종류'].value_counts()
    percentage = counts / counts.sum() * 100
    
    # Choose a color map for distinct colors
    colors = plt.cm.get_cmap('tab10', len(mylabels2))
    
    # Plot a bar graph with a log scale on the y-axis
    plt.figure(figsize=(7, 5))
    for label, count, color in zip(mylabels2, counts, colors(range(len(mylabels2)))):
        plt.bar(label, count, color=color)
    
    plt.yscale('log')  # Set the y-axis to log scale
    plt.xlabel('원동력종류')
    plt.ylabel('Percentage (log scale)')
    plt.show()
    plt.savefig("./img/04.png")
    # st.info("""
    #     In light of the significant dominance of solar power in our previous analysis, the data for other power sources was relatively indiscernible due to their small proportions. To better visualize and understand the distribution of these minor power sources, a logarithmic analysis has been conducted. 

    #     Logarithmic scales can help reveal patterns and trends in data that would otherwise be hard to read in a linear scale, especially when dealing with data that spans several orders of magnitude. 

    #     By using a logarithmic scale, we can more effectively compare and interpret the small but still important contributions of the '연료전지' (fuel cells), '소수력' (mini hydro), '기력발전' (steam turbine), '매립가스(LFG)' (landfill gas), '증기터빈' (steam turbine), and '바이오가스' (biogas) power sources.
    #     """)
    st.pyplot(plt)

def count_per_year(df_new):
    df_new['사업개시일자']= pd.to_datetime(df_new['사업개시일자'])	
    df_new['사업개시년도']=df_new['사업개시일자'].dt.year
    df_new['사업개시월']=df_new['사업개시일자'].dt.month
    df_new['사업개시일']=df_new['사업개시일자'].dt.day
    grouped_data2 = df_new.groupby('사업개시년도').agg({'발전소명': 'count', '용량(kW)': 'sum'}).reset_index()
    grouped_data2.columns = ['사업개시년도', '발전소_개수', '총_용량']
    df_new['사업개시년도'] = df_new['사업개시년도'].astype(int)
    fig, axs = plt.subplots(1, 2, figsize=(15, 5))

    data = {'발전소_개수': grouped_data2['발전소_개수'], '총_용량': grouped_data2['총_용량']}

    custom_palette = sns.color_palette(['#8c6bb1', '#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3', '#fdb462'])

    # Create a donut chart for each column
    for i, (label, series) in enumerate(data.items()):
        # Plot a pie chart with a hole in the center (donut chart)
        wedges, texts, autotexts = axs[i].pie(series, labels=grouped_data2['사업개시년도'], autopct='%1.1f%%', startangle=90,
                                              colors=custom_palette, wedgeprops=dict(width=0.3), shadow=True)
    
        # Make the labels vertical
        for j, (text, autotext) in enumerate(zip(texts, autotexts)):
            percentage = series.iloc[j] / series.sum() * 100
            if percentage < 5 or grouped_data2['사업개시년도'].iloc[j] < 2013:
                text.set_text('')
                autotext.set_text('')
            else:
                text.set_rotation('vertical')
                autotext.set_rotation('vertical')

        axs[i].set_title(label)

# Display
    plt.tight_layout()
    plt.show()
    plt.savefig("./img/05.png")
    # st.text("""
    #     The provided code segment performs several data processing and visualization tasks. 
    #     It initially transforms the '사업개시일자' column into a datetime format, extracts the year,
    #     month, and day components, and stores them in new columns. The data is grouped by the '사업개시년도', 
    #     calculating the count of power plants and their total capacity for each year.
    #     Finally, it generates a subplot with two pie charts, visualizing the distribution 
    #     of the number of power plants and their total capacity per start year. 

    #     """)
    st.pyplot(plt)

def count_per_year_analysis():
     
    selected_value = st.selectbox('Select the language for the analysis', ['English','Korean'])
    if selected_value == 'English':
        st.text("""
        1. The number of power plants has been consistently increasing over the years, indicating continuous growth and expansion in the power generation industry.
        2. Significant jumps in the number of power plants and their total capacity occurred in 2014, 2018, and 2022. These may be attributed to favorable government policies or advancements in power generation technologies during those years.
        3. 2022 witnessed the highest number of power plants, while 2019 recorded the highest total capacity. This suggests that while the number of power plants has consistently increased, their individual capacities may vary significantly.
        4. Despite a slight decrease in the number of power plants in 2020, both the number of power plants and their capacities rebounded in 2021 and 2022, demonstrating the resilience and robust growth of the power generation industry.
        """)
    elif selected_value == 'Korean':
        st.text("""
        1. 연도별 발전소 수가 꾸준히 증가하면서 발전 산업이 계속해서 성장하고 확장되고 있다는 것을 나타냅니다.
        2. 2014년, 2018년, 2022년에 발전소 수와 총 용량에서 큰 증가가 있었습니다. 이는 해당 연도에 유리한 정부 정책이나 발전 기술의 발전과 관련이 있을 것으로 예상됩니다.
        3. 2022년은 가장 많은 발전소 수를 기록했으며, 2019년은 가장 높은 총 용량을 기록했습니다. 이는 발전소 수는 꾸준히 증가함에도 불구하고 개별 발전소의 용량이 상당히 다를 수 있음을 시사합니다.
        4. 2020년에 발전소 수가 약간 감소했지만, 2021년과 2022년에는 발전소 수와 용량이 모두 회복되어 발전 산업의 탄탄한 성장과 회복력을 보여주고 있습니다.
        """)
    
# ***************** below functions are related to crawling data
def crawl_data():
    if st.session_state.crawl_data_executed:
        st.warning("Web crawling has already been executed.")
        return
       
    driver = webdriver.Chrome()
    driver.get("https://recloud.energy.or.kr/main/main.do")
    
    install_trend_path ="#sub-header > div.header_inner.fix > div > ul > li:nth-child(3) > a > span"
    install_trend_element = driver.find_element(By.CSS_SELECTOR, install_trend_path)
    time.sleep(4)
    install_trend_element.click()
    # print(install_trend_elements.text)
    
    
    install_trend_handle = driver.window_handles[-1]       
    driver.switch_to.window(install_trend_handle)
    time.sleep(4)
    
    acc_inst_path = "#sub-container > div > div > fieldset > div > ul.tab_sty.sty02.fix.mt45 > li:nth-child(2) > a"
    acc_install_element= driver.find_element(By.CSS_SELECTOR, acc_inst_path)
    acc_install_element.click()
    install_trend_handle = driver.window_handles[-1]       
    driver.switch_to.window(install_trend_handle)
    time.sleep(4)
    
    column_names = []
    for col in range(1, 7):
        col_selector = f"#datatable > thead > tr > th:nth-child({col})"
        column_name = driver.find_element(By.CSS_SELECTOR, col_selector).text
        column_names.append(column_name)
    
    # print(f"Row names = {column_names}")
    
    row_names = []
    for row in range(1, 19):
        row_selector = f"#datatable > tbody > tr:nth-child({row}) > th"
        row_name = driver.find_element(By.CSS_SELECTOR, row_selector).text
        row_names.append(row_name)
    
    # print(f"Row names = {row_names}")
    
    data = []
    for c_row in range(1, 19):
        row_data = []
        for c_col in range(2, 7):
            cell_selector = f"#datatable > tbody > tr:nth-child({c_row}) > td:nth-child({c_col})"
    #         row_data.append(element.text)
            cell_value = driver.find_elements(By.CSS_SELECTOR, cell_selector)
            if cell_value:
                for element in cell_value:
                    row_data.append(element.text)
            else:
                row_data.append(None)  
        data.append(row_data)


    ## data is done webcrawling
    driver.close()

    column_names.remove('구분')
    df0 = pd.DataFrame(data, columns=column_names, index=row_names)
    st.success('👏 Web crawling has started successfully.This may take a few moments.📀')
    # st.text('👉 Data extraction is in progress. This may take a few moments.')
   

    st.text("""🔍 Below is the data meticulously acquired from a dependable web crawling source.""")
    
    st.dataframe(df0)

    df10=df0.reset_index(drop=True)
    df1 = df10.copy() 
    df1.drop('발전소 개소\n(2022년까지 누적)', axis=1, inplace=True)
    df2 = df1.copy()
    df2.columns = df2.columns.str.replace(r'[^0-9]', '', regex=True)
    for year in range(2019, 2023):
        df2[str(year)] = df2[str(year)].replace(',', '', regex=True).astype(float)
    
    df3 = pd.DataFrame({'구분': row_names})
    result_df = pd.concat([df3, df2], axis=1)
    save_path="./data/inst_data.csv"
    result_df.to_csv(save_path, index=False, encoding="euc-kr")
    st.text("""🔄 Below is the processed data""")
    with st.expander('Click to View the processed dataframe 📊', expanded=True):    
        st.dataframe(result_df)
    st.success("📞 Data connection to server established! 🌐")
    db_connection_info = "mysql+pymysql://gjuser:dbdb@localhost:3308/gjdb"
    
    ### Database 컨넥션(연결)하기
    db_connection = create_engine(db_connection_info)
#     db_connection

    host = "localhost"
    user = "gjuser"
    password = "dbdb"
    db = "gjdb"
    port=3308
    # charset = "UTF8"
    cursorclass = pymysql.cursors.DictCursor # 조회시 컬럼명을 동시에 보여줄지 여부 설정
    autocommit = True # 자동 반영

    try:
        conn = pymysql.connect(host=host,
                               user=user,
                               password=password,
                               db=db,
                               port=port,
                               # charset=charset,
                               autocommit=autocommit,
                               cursorclass=cursorclass)
    
        print("DB connection successful >>> ", conn)

    except Exception as e:
        print("DB Server Checking...", e)

    try:
        result_df.to_sql(name="solar_Inst_trend",
                   con=db_connection,
                   index=False,
                   if_exists="append")
        print("Data successfully written to database")

    except Exception as e:
        print("Error writing data to database: ", e)
        
    
    st.info("💾 Data has been successfully saved to the server! 🎉")
    st.text("📊 Ready to explore the analytical insights? Click the next tab to view captivating graphs and data analysis! ⚡")
    st.session_state.crawl_data_executed = True
    
    return df0


def crawl_graph_1(df3):
    db_connection_info = "mysql+pymysql://gjuser:dbdb@localhost:3308/gjdb"
    
    ### Database 컨넥션(연결)하기
    db_connection = create_engine(db_connection_info)
#     db_connection

    host = "localhost"
    user = "gjuser"
    password = "dbdb"
    db = "gjdb"
    port=3308
    # charset = "UTF8"
    cursorclass = pymysql.cursors.DictCursor # 조회시 컬럼명을 동시에 보여줄지 여부 설정
    autocommit = True # 자동 반영

    try:
        conn = pymysql.connect(host=host,
                               user=user,
                               password=password,
                               db=db,
                               port=port,
                               # charset=charset,
                               autocommit=autocommit,
                               cursorclass=cursorclass)
    
        print("DB connection successful >>> ", conn)

    except Exception as e:
        print("DB Server Checking...", e)
        
    cur = conn.cursor()
    sql = " Select * From solar_Inst_trend "
    rs_cnt = cur.execute(sql)
    print(f"{rs_cnt}건이 조회 되었습니다.")
    rows = cur.fetchall()
    
    df3 = pd.DataFrame(rows)
    st.success("📊 Power plant installation trends across cities.")
    # st.dataframe(df3)
    #&&&&&
    cities = df3['구분'].tolist()
    column_dict = dict(zip(df3.columns, df3.values.T.tolist()))
    
    selected_columns = df3.loc[:, '2019':'2022']
    transposed_df = selected_columns.transpose()
    index=cities
    df4 = df3.set_index('구분')
    df5 = df3.set_index('구분')[['2019', '2020', '2021', '2022']]
    df6 = df3.set_index('구분', drop=False)[['2019', '2020', '2021', '2022']].rename_axis(None)
    df_last_row = df3.iloc[-1:]  # 마지막 행을 선택하여 새로운 데이터프레임에 저장
    df7 = df6.iloc[:-1] 
    df7.head()

    plt.figure(figsize=(25, 35))
    ax = df7.plot.bar(rot=85)
    
    # Set the title and labels
    ax.set_title("Yearly Installation of Power Plants")
    ax.set_xlabel("City")
    ax.set_ylabel("Number of Power Plants")
    
    # Show the plo
    plt.savefig("./img/05.png")
    st.pyplot(plt)
    return df7

def crawl_graph_1_Analysis():
    with st.expander("Expand to view the Analysis 📊", expanded=True):
        selected_value = st.selectbox('Select a language to view the Crawl Graph Analysis: ', ['English','Korean'])
        if selected_value == 'English':
            st.text("""
            1. 경기도, 강원도, 충청북도, 충청남도, 전라북도, 전라남도, and 경상북도 have consistently shown high numbers of solar power installations from 2019 to 2022.
            2. 전라북도 had the highest number of installations in 2019 with 12,477 installations, which has decreased to 3,930 installations in 2022.
            3. Metropolitan cities such as 서울특별시, 부산광역시, 대구광역시, 인천광역시, 광주광역시, 대전광역시, 울산광역시, and 세종특별자치시 have shown relatively lower numbers of installations, possibly due to space constraints or urban planning considerations.
            4. Notably, 부산광역시 and 경상남도 have seen an increase in installations from 2021 to 2022, indicating a growing interest or investment in solar power in these regions.
            5. There has been a general decrease in the number of new installations from 2019 to 2022. However, the total cumulative number of installations remains high, demonstrating South Korea's substantial solar power capacity.
            6. It's also assumed that the number of installations may have a close relationship with land availability and population density. A higher value in this regard could indicate a greater potential for solar power installations.
            7. This trend signifies South Korea's continued commitment to renewable energy sources.
            """)
        elif selected_value == 'Korean':
            st.text("""
            1. 경기도, 강원도, 충청북도, 충청남도, 전라북도, 전라남도 및 경상북도는 2019년부터 2022년까지 지속적으로 높은 수의 태양광 발전 설비를 보여주고 있습니다.
            2. 전라북도는 2019년에 12,477개의 설치로 가장 많았으며, 2022년에는 3,930개로 감소했습니다.
            3. 서울특별시, 부산광역시, 대구광역시, 인천광역시, 광주광역시, 대전광역시, 울산광역시 및 세종특별자치시와 같은 대도시는 공간 제약이나 도시 계획 고려로 인해 상대적으로 적은 수의 설치를 보여주고 있습니다.
            4. 특히, 부산광역시와 경상남도는 2021년부터 2022년까지 설치 수가 증가하면서 이 지역에서 태양광 발전에 대한 관심이나 투자가 증가하고 있음을 나타냅니다.
            5. 2019년부터 2022년까지 신규 설치 수는 일반적으로 감소하고 있습니다. 그러나 누적 설치 수는 여전히 높아 대한민국의 상당한 태양광 발전 능력을 보여주고 있습니다.
            6. 이 추세는 대한민국이 재생 에너지에 대한 계속된 헌신을 나타냅니다.
            7. 또한 설치 수가 토지 이용 가능성 및 인구 밀도와 밀접한 관련이 있을 것으로 가정됩니다. 이러한 측면에서 높은 값은 태양광 발전 설비의 더 큰 잠재력을 나타낼 수 있습니다.
            """)
   
      





def crawl_graph_2(df7):
    ax = df7.plot.bar(stacked=True, rot=85, figsize=(20, 10))

    ax.set_title("Yearly Installation of Power Plants", fontsize=20)
    ax.set_xlabel("City", fontsize=20)
    ax.set_ylabel("Number of Power Plants", fontsize=20)
    ax.legend(fontsize=20)
    plt.xticks(fontsize=14) 
    plt.yticks(fontsize=14)
    
    plt.show()
    plt.savefig("./img/06.png")
    st.success("📊 Accumulated installation of solar cells (2019-2022) across cities.")
    st.pyplot(plt) 
    
def word_cloud():
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY="AIzaSyCGHrcNmSoUKoRGosiIShFLW9o69acZwi4"
    
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)
    
    request = youtube.commentThreads().list(
        part="snippet",
        videoId="5E9zOGX3oMo",
        maxResults=500
    )
    
    comments = []
    
    # Execute the request.
    response = request.execute()
    
    # Get the comments from the response.
    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']
        public = item['snippet']['isPublic']
        comments.append([
            comment['authorDisplayName'],
            comment['publishedAt'],
            comment['likeCount'],
            comment['textOriginal'],
            public
        ])
    
    while (1 == 1):
      try:
       nextPageToken = response['nextPageToken']
      except KeyError:
       break
      nextPageToken = response['nextPageToken']
      # Create a new request object with the next page token.
      nextRequest = youtube.commentThreads().list(part="snippet", videoId="5E9zOGX3oMo", maxResults=500, pageToken=nextPageToken)
      # Execute the next request.
      response = nextRequest.execute()
      # Get the comments from the next response.
      for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']
        public = item['snippet']['isPublic']
        comments.append([
            comment['authorDisplayName'],
            comment['publishedAt'],
            comment['likeCount'],
            comment['textOriginal'],
            public
        ])
    
    df = pd.DataFrame(comments, columns=['author', 'updated_at', 'like_count', 'text','public'])
    df.info() 
    max_like_count = df['like_count'].max()
    max_like_text = df[df['like_count'] == max_like_count]['text'].values[0]
    print(max_like_text)
    max_like_index = df[df['like_count'] == max_like_count].index[0]
    print(max_like_index)
    save_path="./data/all_comments.csv"
    df.to_csv(save_path, index=False)
    save_path="./data/all_comments.csv"
    df1=pd.read_csv(save_path)    
    okt = Okt()
    all_comment = []
    
    for cmt in df["text"] :
        # print(okt.nouns(cmt))
        ### extend() : 리스트에 값만 추출하여 확장해서 추가하는 방식
        #  - append() : 리스트에 형태(type) 자체를 추가하는 방식
        all_comment.extend(okt.nouns(cmt))
    
    all_comment2 = [w for w in all_comment if len(w) > 1]
    # all_comment2
    all_comment_count = Counter(all_comment2)

    all_top_70 = {}
    for k, v in all_comment_count.most_common(70):
        all_top_70[k] = v
    
    all_top_70 = {k:v for k, v in all_comment_count.most_common(70)}
    # all_top_70
    cmap = plt.get_cmap('viridis')

# Extract values and keys
    values = list(all_top_70.values())
    keys = list(all_top_70.keys())
    
    # Normalize values to use in colormap
    norm = plt.Normalize(min(values), max(values))
    
    # Create a figure and axis
    plt.figure(figsize=(20, 10))
    
    # Title
    plt.title("all 리뷰의 단어 상위 (50개) 빈도 시각화", fontsize=17)
    
    # Bar graph with gradient color
    for key, value in zip(keys, values):
        # Additional condition to skip "태양광" or "전기"
        if key == "태양광" or key == "전기":
            continue
        
        color = cmap(norm(value))
        plt.bar(key, value, color=color)
    
    # x-axis and y-axis labels
    plt.xlabel("리뷰 명사")
    plt.ylabel("빈도(count)")
    
    # Adjust x-axis labels rotation
    plt.xticks(rotation=70)
    
    # Show the graph
    plt.show()
    
    st.success('📊 Graphical view of the top 50 word frequencies! 📈')
    st.pyplot(plt)
    # selected_value = st.selectbox('Select Language', ['English','Korean'])
    # if selected_value == 'English':
    #     st.info("""In the context of this analysis, the chosen YouTube video has been selected, 
    #         and all accompanying comments have been systematically extracted and stored in a CSV file. 
    #         Subsequent to this extraction, a comprehensive word analysis has been conducted to discern
    #         patterns and facilitate psychological analysis.""")
    # elif selected_value == 'Korean':
    #     st.text("""
    #             이 분석의 맥락에서는 선택된 YouTube 비디오가 선별되었으며, 그와 관련된 모든 댓글들이 체계적으로 추출되어
    #             CSV 파일에 저장되었습니다. 이러한 추출 후에는 패턴을 파악하고 심리 분석을 용이하게 하기 위해 포괄적인
    #             단어 분석이 진행되었습니다.
    #             """)


    exclude_words = ["태양광", "전기"]

    
    # Filter out excluded words
    filtered_top_70 = {word: count for word, count in all_top_70.items() if word not in exclude_words}
    
    # WordCloud configuration
    plt.figure(figsize=(8, 8))
    plt.title("리뷰 단어 워드클라우드 시각화")
    font_path = "C:/Windows/Fonts/malgunsl.ttf"
    wc = WordCloud(
        font_path=font_path,
        background_color="ivory",
        width=800,
        height=600
    )
    
    # Generate WordCloud from filtered frequencies
    cloud = wc.generate_from_frequencies(filtered_top_70)
    
    # Display WordCloud image
    plt.imshow(cloud)
    plt.axis("off")
    plt.savefig("./img/리뷰_단어_워드클라우드_시각화.png")
    plt.show()
    
    st.success('🌈 Word cloud visualization of review word frequencies! 📊')

    st.pyplot(plt)
    
    with st.expander("Expand to see the Analysis 📊", expanded=True):
        selected_value = st.selectbox('Select a language to view the Word Cloud Analysis: ', ['English','Korean'])
        if selected_value == 'English':
            st.text("1. Key words such as 'government', 'generation', 'power', 'production', 'facilities', 'issues', 'policy', 'momentum', 'Moon Jae-in', 'storage', etc., represent topics related to energy generation in Korea.\n"
            "2. Government and Generation Policy: Words like 'government' and 'policy' have high frequencies, and the mention of 'Moon Jae-in' suggests opinions related to the role of the Korean government and policy formulation for energy generation.\n"
            "3. Words like 'generation', 'power', 'production', 'energy', etc., emerged as significant keywords related to energy generation in Korea, indicating the country's focus and importance on energy generation and power production.\n"
            "4. Energy Generation Facilities and Storage Technology: Words like 'facilities', 'power plant', 'hydrogen', 'regeneration', 'nuclear power', 'transmission', 'facilities', 'renewable energy', etc., indicate keywords related to energy generation facilities. The mention of 'storage' reflects an interest in energy storage technology.\n"
            "5. Regional Issues: Words like 'Jeolla-do', 'Honam region', 'Honam', etc., represent issues related to Korea's regional characteristics. There is a possibility that issues related to energy generation in specific regions are mentioned.\n"
            "6. Environment and Issues: The word 'environment' along with words like 'issues', 'inadequate', 'coal', 'pollution', etc., reflects concerns and issues related to environmental problems and inadequate policies in the context of energy generation.\n"
            "7. Other Issues: Words like 'price', 'increase', 'efficiency', 'permit', 'plan', 'deficit', etc., indicate issues related to the economic aspects of energy generation. Terms like price, efficiency, and permits showcase the relevance between energy policy and economic activities.\n"
            "8. Through the above analysis, it is evident that the provided word cloud reflects various topics and issues related to energy generation in Korea. This analysis can help understand opinions and issues related to energy policy formulation and serve as a basis for more effective policies and improvement strategies."
            )
        elif selected_value == 'Korean':
            st.text("""
            1. 주요 단어들인 '정부', '발전', '전력', '생산', '시설', '문제', '정책', '기세', '문재인', '저장' 등은 한국의 에너지 발전과 관련된 주제들을 나타내고 있습니다.
            2. 정부와 발전 정책: '정부'와 '정책'이라는 단어들이 빈도수가 높게 나타나며, '문재인'이라는 인물도 언급되었습니다. 이는 한국 정부의 역할과 에너지 발전에 대한 정책 수립과 관련된 의견들을 나타냅니다.
            3. '발전', '전력', '생산', '에너지' 등의 단어들은 한국의 에너지 발전과 관련된 주요 키워드로 나타났습니다. 이는 한국에서 에너지 발전과 전력 생산에 대한 관심과 중요성을 보여줍니다.
            4. 에너지 발전 시설과 저장 기술: '시설', '발전소', '수소', '재생', '원전', '송전', '설비', '신재생에너지' 등의 단어들은 에너지 발전 시설과 관련된 키워드로 나타났습니다. '저장'이라는 단어는 에너지 저장 기술에 대한 관심을 보여줍니다.
            5. 지역과 관련된 이슈: '전라도', '호남지방', '호남' 등의 단어들은 한국의 지역적인 특성과 관련된 이슈를 나타냅니다. 지역별 에너지 발전과 관련된 문제들이 언급되었을 가능성이 있습니다.
            6. 환경과 문제: '환경'이라는 단어와 함께 '문제', '부실', '석탄', '오염' 등의 단어들이 나타났습니다. 이는 에너지 발전과 관련하여 환경 문제와 부실한 정책 등에 대한 우려와 이슈를 반영합니다.
            7. 기타 이슈: '가격', '인상', '효율', '허가', '계획', '적자' 등의 단어들은 에너지 발전과 관련된 경제적인 측면과 이슈들을 나타냅니다. 가격, 효율, 허가 등의 단어들은 에너지 정책과 경제 활동 사이의 관련성을 보여줍니다.
            8. 위의 분석을 통해 주어진 워드 클라우드 결과에는 한국의 에너지 발전과 관련된 다양한 주제와 이슈들이 반영되어 있음을 알 수 있습니다. 이러한 분석을 통해 에너지 정책 수립과 관련된 의견 및 이슈들을 파악할 수 있으며, 이를 바탕으로 보다 효과적인 정책과 개선 방안을 모색할 수 있습니다.
            """)

    # return max_like_text

# def max_comment():
    


def main():
    if 'crawl_data_executed' not in st.session_state:
        st.session_state.crawl_data_executed = False

    with st.sidebar:
        # selected = option_menu("Main Menu", 
        #                    ["Home", "Team", "Graph", "Wordcloud", "🌐 Crawl Zone"], 
        #                    icons=['House check', 'person-hearts','kanban', 'wordpress', 'youtube'],
        #                    menu_icon="menu-button",
        #                    default_index=0)
        selected = option_menu(
                menu_title='KLP Energy Platform',
                options=['Home','☁️ WordCloud','🌐 Crawl Zone','🌤️ Gwangju RE','Team'],
                icons=['house-fill','Youtube', 'File earmark word fill','Server','person-circle'],
                menu_icon='chat-text-fill',
                default_index=1,
                styles={
                                "container": {"padding": "5!important","background-color":'black'},
                    "icon": {"color": "white", "font-size": "23px"}, 
                    "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#02ab21"},}
                
                )


    if selected == "Home":
        st.write("Welcome to the Home page!")
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["💡Main", "💡STEP1", "💡STEP2", "💡STEP3", "💡데이터 분석 모아모아"])

        with tab1:
            st.header("💡Main")

        with tab2:
            st.header("💡STEP 1")
            # 1-1 지역별 신재생에너지 발전소 현황----------------------------------------------------------------------------
            st.info("1-1. 지역별 신재생에너지 발전소 현황")
            st.image('./img/06.png', use_column_width = True)
        
            # 1-2 연도별 신재생에너지 발전량과 보급현황 비교----------------------------------------------------------------------------
            st.info("1-2. 연도별 신재생에너지 발전량과 보급현황 비교(2012-2021)")
            df_g=step1_func()

        with tab3:
            st.header("💡STEP 2")
            # 2-1 제주 지역 연도별 신재생에너지 발전량과 보급현황 비교------------------------------------------------------------------------
            st.info("2-1. 제주 지역 연도별 신재생에너지 발전량과 보급현황 비교")  
            step2_func(df_g)

        with tab4:
            st.header("💡STEP 3")
            st.subheader("🌱방안 1 : HVDC 해저케이블")
            st.text("""
            HVDC란? 
            초고압 직류 송전 시스템(High Voltage Direct Current)
            발전소에서 생산되는 교류전력을 직류로 변환시켜 송전하는 시스템이다.
            직류는 교류와 달리 전자파가 발생하지 않아 환경에 대한 부정적 영향을 최소화 시킬 수 있다.
            """)
            st.text("""
            국내 설치된 HVDC 해저 전력망
            HVDC 1 제주-해남 HVDC 해저 전력망
            HVDC 2 서제주-진도 HVDC 해저 전력망
            HVDC 3 동제주-완도 HVDC 해저 전력망
            전남 완도와 제주도 간 90km를 해저케이블로 연결
            제주지역에 전력을 안정적으로 공급할 수 있고 재생에너지를 육지로 전송 가능하게 해준다.
            """)
            st.text("""
            기존 HVDC 1, 2호기와 신설된 HVDC 3호기의 차이
            기존 1, 2호기의 경우 전류형 HVDC를 사용한 반면, 제3호기의 경우는 전압형 HVDC를 도입하였다.
            전류형 기술은 무효전력 보상을 위한 별도의 설비를 필요로 하기 때문에 시스템 구성이 복잡하고 설치면적이 크다는 단점이 있었지만,
            3호기의 경우 무효전력이 자체 보상되어 시스템 구성이 간단하고 설치면적이 전류형의 약 60%로 줄어들었습니다. 
            3호기의 가장 큰 특징으로는 실시간 양방향 전환이 가능하다는 점
            기존에는 송전 방향을 바꾸기 위해서는 대기시간 확보가 필요하였기 때문에 어려움을 겪었지만, 3호기를 통해 제주 신재생 보급정책으로 급증한 에너지를 육지로 쉽게 공급이 가능할 것이라 예상된다.
            """)
            
            st.subheader("🌱방안 2 : P2H(Power To Heat) / P2G(Power to Gas)")
            st.text("""
            P2H(Power To Heat)란?
            전력을 열에너지로 전환하는 기술로
            전력이 과잉 생산되었을 때, 열에너지로 전환하여 사용자에서 공급 에너지를 저장한다.
            """)
            st.text("""
            P2G(Power To Gas)란?
            신재생에너지원으로 생산된 전기에너지를 수소 또는 메탄으로 전환하는 기술이다.
            """)
            
            st.subheader("🌱방안 3 : 제주 '플러스 전력수요관리' 제도")
            st.text("""
            플러스 전력수요관리(DR·Demand Response) 제도란?
            전력수요관리(DR)는 전력거래소와 계약한 기업이 국가의 요구 만큼 전기 사용을 줄이면 정부가 이를 금액으로 보상해주는 제도이다.
            제주는 이러한 제도를 “플러스 전력수요관리제도”로 변환하였는데,
            이는 "전기차 충전"을 통해 전력 수요를 높임으로써 재생에너지 사업자의 출력제한을 최소화 하는 것을 기대하고 있다.
            """)
        with tab5:
            st.subheader("💡데이터 분석 모아모아")
            
            # 1. 연도별 광주 신재생에너지 발전량----------------------------------------------------------------------------------------------
            st.info("1. 연도별 광주 신재생에너지 발전량")
            tab5_func()        

    ### *********************** 광주 데이터********************
    elif selected == "🌤️ Gwangju RE":
        
        
        st.header("🌍 광주 지역별 신재생에너지 발전소 현황") 
        

        data = Gwangju_data()
        with st.expander("Explore the Data 📊"):
            st.dataframe(data)
            

        # st.info("데이터 전처리")
        df_new = data_cleaning(data)
        # with st.expander("cleaned_Data"):
        #     st.dataframe(df_new)
        # st.info("Total of 350 cells in the dataset contained null values. They have been handled accordingly.")
        # print(f"df_new {df_new}")
        grouped_result = grouped_data()
        # st.info("""
        #     1. Deal with Missing Values: Missing values in 'Business Start Date' and 'Permission Date' were filled with each other's data.
        #     2. Deal with Duplicates and Outliers: Duplicated rows were identified and future dates were removed.
        #     3. Data Transformation and Enrichment: The data was grouped by 'City County', calculating the count of 'Power Plant Name' and the sum of 'Capacity (kW)' for each group for further data analysis.
        #     """)

        st.text("Data was grouped by 'City County' to count the number of 'Power Plant Names' and sum the 'Capacity (kW)' for each group.")
        col1, col2= st.columns([2, 2])
        with col1:
            checkbox1 = st.checkbox("📊 Show processed renewable energy data",  value=True)
            if checkbox1:
                st.dataframe(grouped_result)

        with col2:
            checkbox2 = st.checkbox("🗺️ Visualize power plant distribution in Gwangju", value=True)
            if checkbox2:
                gwangju_status(grouped_result)

        
        
        # st.text("the total count of power plants and the overall capacity in each 'City County' (시군구)")


        
        show_plot1_checkbox = st.checkbox("🏭 Total Power Plants & Capacity by 'City County' (시군구)",  value=True)
        if show_plot1_checkbox:
            # plot1(grouped_result)
            pichart(grouped_result)

        with st.expander("View the Analysis", expanded=True):
            plot1_analysis()

        # show_pichart_checkbox = st.checkbox("pichart plot 보기")
        # if show_pichart_checkbox:
        #     pichart(grouped_result)

        # with st.expander("Analysis 보기"):
        #     plot1_analysis()

        checkbox1 = st.checkbox("View Log Chart of Processed Renewable Energy Data 📊",  value=True)
        if checkbox1:
            st.text("Displaying count log view...")
            logchart(df_new)


        st.text("📊 Analysis of the Graph")
        with st.expander("🔍 View the Analysis", expanded=True):        
            various_P_analysis()

        # with st.expander("View the Analysis", expanded=True):
        #     various_P_analysis()
        
        # show_various_p_checkbox = st.checkbox("various p 보기")
        # if show_various_p_checkbox:
        #     various_p(df_new)

        # with st.expander("Analysis of various power plant 보기"):
        #     various_P_analysis()

        # show_logchart_checkbox = st.checkbox("logchart 보기")
        # if show_logchart_checkbox:
        #     logchart(df_new)

        count_per_year_checkbox = st.checkbox("View Power Plant Count and Capacity per Year", value=True)
        if count_per_year_checkbox:
            count_per_year(df_new)

        with st.expander("View the Analysis of the Power Plant Count and Capacity per Year", expanded=True):
            count_per_year_analysis()

  ## *****************************************************
    ##**************************************************************
    
    elif selected == "☁️ WordCloud":
        st.subheader("🧠💭 워드 클라우드로 사람의 심리를 2초만에 분석하기!")
        st.subheader('🎯 Objective and Methodology 📊')
        with st.expander("View the Analysis", expanded=True):
            
            selected_value = st.selectbox('View in', ['English', 'Korean'])
            if selected_value == 'English':
                st.text("""
                📝 For this analysis, a specific YouTube video was selected, and its content, along with all associated comments, 
                were systematically extracted and stored in a CSV file. Following the extraction process, a thorough 
                word analysis was conducted to identify patterns and enable psychological analysis.
                """)
            elif selected_value == 'Korean':
                st.text("""
                    📝 이 분석을 위해 특정 YouTube 동영상이 선택되었으며, 해당 동영상의 콘텐츠와 모든 관련 댓글은 체계적으로 추출되어 CSV 파일에 저장되었습니다. 
                    추출 과정 이후에는 철저한 단어 분석이 수행되어 패턴을 식별하고 심리 분석을 가능하게 했습니다.
                    """)
        
        col1, col2= st.columns([1, 1])
        with col1:            
            st.image('./yt.png')
            

        with col2:
            st.subheader("The Comment with the most like is: ")
            st.warning("인증 필요한 산업에 전력을 최대한 보내줘야지.....")
       
        word_cloud()

     
               
 ## *****************************************************hhh
    ##**************************************************************

    elif selected == "🌐 Crawl Zone":
        tab1, tab2= st.tabs(["📂Data Collection", "💹Graphical Analysis"])
        with st.container():
            
            
            with tab1:             
                st.header("📂Commence Data Extraction")
                # st.subheader('Step 1️⃣ : Push the button below to start data crawling.')  
                # checkbox_start_crawling = st.checkbox("❗start_crawling")
                # if  checkbox_start_crawling:             
                                            
                df0 = crawl_data()
                # st.text('👉 Data extraction is in progress. This may take a few moments.')  
                    
                

        with tab2:             
                st.header("📊 Graphical Analysis")
                # st.text('👉 Explore insightful graphs based on the crawled data.')
                df7=crawl_graph_1(df0)
                crawl_graph_2(df7)
                # st.text('👉 👉 Analyzing the graph to unveil patterns and trends.')
                crawl_graph_1_Analysis()
                
        
        
        m = st.markdown(
                """
                <style>
                    button[data-testid="baseButton-secondary"]{  
                        background-color: #C7B8B8;
                    }
                </style>""",
                unsafe_allow_html=True,
            )



 ## *****************************************************
    ##**************************************************************
 
    elif selected == "Team":
            st.header("Meet Our Awesome Team! 👋🚀")
            st.image('./member.png')
            st.markdown("""
            Welcome to our fantastic team! We're a group of passionate individuals dedicated to making a positive impact. 
            Together, we collaborate, innovate, and bring our unique skills to the table. Meet the faces behind the magic!
            """)


if __name__ == '__main__':
    main()



# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




