import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Employee Performance Analysis",
    layout="wide"
)

st.title("Employee Performance Analysis Dashboard")

df = pd.read_csv("employee_dataset_powerbi.csv")

if "Attendance_Percentage" in df.columns:
    df["Attendance_Percentage"] = (
        df["Attendance_Percentage"]
        .astype(str)
        .str.replace("%","")
        .astype(float)
    )

st.sidebar.header("Filters")

department = st.sidebar.multiselect(
    "Department",
    options=df["department"].unique(),
    default=df["department"].unique()
)

filtered_df = df[df["department"].isin(department)]

st.subheader("Dataset Preview")
st.dataframe(filtered_df.head())

col1,col2,col3,col4 = st.columns(4)

col1.metric("Employees", len(filtered_df))
col2.metric("Avg Salary", round(filtered_df["Salary"].mean(),2))
col3.metric("Avg Attendance", round(filtered_df["Attendance_Percentage"].mean(),2))
col4.metric("Avg Performance", round(filtered_df["performance_score"].mean(),2))

st.subheader("Salary Distribution")

fig, ax = plt.subplots()
sns.histplot(filtered_df["Salary"], kde=True, ax=ax)
st.pyplot(fig)

st.subheader("Age Distribution")

fig, ax = plt.subplots()
sns.histplot(filtered_df["age"], kde=True, ax=ax)
st.pyplot(fig)

st.subheader("Department Distribution")

fig, ax = plt.subplots()
filtered_df["department"].value_counts().plot(
    kind="bar",
    ax=ax
)
st.pyplot(fig)

st.subheader("Performance Category Distribution")

fig, ax = plt.subplots()
sns.countplot(
    x="performance_category",
    data=filtered_df,
    ax=ax
)
st.pyplot(fig)

st.subheader("Salary by Department")

fig, ax = plt.subplots(figsize=(8,5))
sns.boxplot(
    x="department",
    y="Salary",
    data=filtered_df,
    ax=ax
)
plt.xticks(rotation=30)
st.pyplot(fig)

st.subheader("Attendance vs Performance")

fig, ax = plt.subplots()
sns.scatterplot(
    x="Attendance_Percentage",
    y="performance_score",
    data=filtered_df,
    ax=ax
)
st.pyplot(fig)

st.subheader("Correlation Heatmap")

numeric_cols = filtered_df.select_dtypes(include="number")

fig, ax = plt.subplots(figsize=(10,6))
sns.heatmap(
    numeric_cols.corr(),
    annot=True,
    cmap="coolwarm",
    ax=ax
)
st.pyplot(fig)

st.subheader("Top 10 Highest Salary Employees")

top_salary = filtered_df.sort_values(
    "Salary",
    ascending=False
).head(10)

st.dataframe(top_salary)

st.subheader("Top 10 Performers")

top_perf = filtered_df.sort_values(
    "performance_score",
    ascending=False
).head(10)

st.dataframe(top_perf)