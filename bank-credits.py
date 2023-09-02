import pandas as pd 
import streamlit as st 
#import plotly_express as px
import seaborn as sns
from matplotlib import pyplot as plt

st.set_page_config(layout="centered")
st.title("Анализ откликов на РК по кредитам")


df = st.cache_data(pd.read_csv)("datasets/final.csv")

categorial = ['GENDER', 'EDUCATION', 'MARITAL_STATUS', 'SOCSTATUS_WORK_FL', 'SOCSTATUS_PENS_FL', 'FAMILY_INCOME',
              'REG_ADDRESS_PROVINCE', 'FACT_ADDRESS_PROVINCE',
              'POSTAL_ADDRESS_PROVINCE', 'FL_PRESENCE_FL', 'GEN_INDUSTRY', 'GEN_TITLE', 'JOB_DIR']
numeric =    ['AGE', 'CHILD_TOTAL', 'DEPENDANTS', 'OWN_AUTO', 'credits', 'closed', 'PERSONAL_INCOME', 'WORK_TIME']

st.sidebar.header("Распределение признака")
column_distr = st.sidebar.selectbox('Выберите признак', numeric)

st.sidebar.header("Корреляция признаков")
st.sidebar.text("Можно выбрать часть признаков")
cols_corr = st.sidebar.multiselect('Столбцы для матрицы корреляций', numeric, max_selections=6, default=['AGE','PERSONAL_INCOME'])

st.sidebar.header("Зависимость целевой переменной от 2-х других")
cols_deptarget = st.sidebar.multiselect('Переменные для построения зависимости', categorial + numeric, max_selections=2, default=['AGE','PERSONAL_INCOME'])

st.sidebar.header("доля в таргете для бина или категориального признака")
column_distr_target = st.sidebar.selectbox('Выберите признак', categorial)

new_df = df[column_distr]

st.success("Задание: построены графики распределений числовых признаков (не менее, чем по двум признакам)")
st.text("сделаны по 3-м с возможностью выбора")


plt.style.use("ggplot")

fig, ax = plt.subplots()
ax = sns.histplot(new_df, bins=20)
ax.set_title("Распределение " + column_distr)

st.pyplot(fig)

st.success("Задание: построена матрица корреляций")
st.text("Сделаем и матрицу и heatmap")

#col1, col2 = st.columns(2)
if len(cols_corr) ==0:
    st.error("не выбрано ни одно поле")
else: 
    st.write(df[cols_corr].corr())
    fig, ax = plt.subplots()
    ax = sns.heatmap(df[cols_corr].corr(), annot=True)
    st.pyplot(fig)
    
st.success("Задание: построены графиков зависимостей целевой переменной и признаков (не менее, чем два графика)")
st.warning("у нас таргет категориальный, поэтому красивых скаттерплотов не получится по одной переменной. Поэтому рискну сделать по 2-м переменным а таргет подсвечу цветом")


if len(cols_deptarget) == 2:
    fig, ax = plt.subplots()
    ax = sns.scatterplot(df, x = df[cols_deptarget[0]], y = df[cols_deptarget[1]], c=df['TARGET'])
    ax.set_title("зависимость ЦП от " + "/".join(cols_deptarget))
    st.pyplot(fig)
    
st.success("Еленой в чате было предложено: Можно просто гистограмму построить. Для каждой категории или бина значений признака долю 1 в таргете ")
fig, ax = plt.subplots()
sns.histplot(data=df, x=column_distr_target, hue="TARGET", multiple="dodge", shrink=.8)
ax.tick_params(axis='x', rotation=90)

ax.set_title("Доля таргета в " + column_distr_target)

st.pyplot(fig)

st.success("Характеристики распределения числовых признаков")
st.write(df[numeric].describe())


st.success("Числовые характеристики категориальных признаков")
for priznak in categorial:
    st.write(df[priznak].value_counts())



st.success("Данные о пропусках")
st.write(df.isna().sum())


st.title("Кредиты: брать или не брать?")
st.image("1.png", caption="... о вреде капитализма и кредитования ... ", width=700)