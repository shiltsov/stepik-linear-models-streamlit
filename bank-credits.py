import pandas as pd 
import streamlit as st 
#import plotly_express as px
import seaborn as sns
from matplotlib import pyplot as plt

st.set_page_config(layout="centered")

st.title("Кредиты: брать или не брать?")
st.image("1.png", caption="... о вреде капитализма и кредитования ... ", width=700)


df = st.cache_data(pd.read_csv)("datasets/bank-mix.csv")
#st.write(df.head())

st.sidebar.header("Распределение признака")
column_distr = st.sidebar.selectbox('Выберите признак', ["age", "child_total","dependants"])

st.sidebar.header("Корреляция признаков")
st.sidebar.text("Можно выбрать часть признаков")
cols_corr = st.sidebar.multiselect('Столбцы для матрицы корреляций', df.columns, max_selections=6, default=['age','gender'])

st.sidebar.header("Зависимость целевой переменной от 2-х других")
df.notarget = df.columns[df.columns != 'target']
cols_deptarget = st.sidebar.multiselect('Переменные для построения зависимости', df.notarget, max_selections=2, default=['age','personal_income'])


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
fig, ax = plt.subplots()
ax = sns.scatterplot(df, x = df[cols_deptarget[0]], y = df[cols_deptarget[1]], c=df['target'])
ax.set_title("зависимость ЦП от " + column_distr)
st.pyplot(fig)