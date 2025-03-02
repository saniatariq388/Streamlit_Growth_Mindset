import streamlit as st
import pandas as pd
import os
from io import BytesIO

import random



st.set_page_config(page_title="🚀 Personal Growth Tracker", layout='wide')
st.title("🚀 Personal Growth Tracker")
st.write("Manage your goals, to-do list, and track your progress!")

# Sidebar for user biodata
st.sidebar.header("👤 Enter Your Biodata")
name = st.sidebar.text_input("Full Name")
age = st.sidebar.number_input("Age", min_value=1, max_value=100)
gender = st.sidebar.radio("Gender", ["Male", "Female"])
skills = st.sidebar.text_area("Your Skills (comma separated)")
goal = st.sidebar.text_area("Your Short-Term Goal")
image = st.sidebar.camera_input("Upload Your Photo")
date = st.sidebar.date_input("Select Your Birth Date")

if st.sidebar.button("Save Biodata"):
    st.sidebar.success(f"✅ Biodata Saved for {name}")



st.header("📝 Quotes Of The Day")

quotes = [
    "Failure is not the opposite of success; it&opass part of success.",
    "Your mindset determines your success.",
    "Challenges are opportunities in disguise!"
]
st.info(random.choice(quotes))



sentiment_mapping = [":material/thumb_down:", ":material/thumb_up:"]
selected = st.feedback("thumbs")
if selected is not None:
    st.markdown(f"You selected: {sentiment_mapping[selected]}")


# Notes Section
st.header("📝 Quick Notes")
notes = st.text_area("Write your notes here...")
if st.button("💾 Save Notes"):
    st.success("✅ Notes Saved!")

# Progress Tracker
st.header("📊 Daily Progress Tracker")
progress = st.slider("How much progress did you make today?", 0, 100, 50)
st.progress(progress / 100)
st.success("🚀 Keep Growing Every Day!")

st.header("� Write Your Growth Goal for Today:")
goal = st.text_area("🚀 Write Your Growth Goal for Today:")
if goal:
    st.write(f"💡 Your Goal: {goal}")
    st.success("You're on the right track! Keep going. 🔥")


uploaded_files =st.file_uploader("Upload your file", type=["csv", "xlsx"], accept_multiple_files=True)


if uploaded_files:
   for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()


        if file_ext == ".csv":
           df = pd.read_csv(file)
        elif file_ext == ".xlsx":
           df = pd.read_excel (file)
        else:
            st.error("Unsupported file type: {file_ext}")
            continue
        # display about file info
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size/1024}")

        # show 5 rows of our df
        st.write("Preveiw the Head of the Dataframe")
        st.dataframe(df.head())

        # options for data cleaning
        st.subheader("🍊Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
           col1, col2 = st.columns(2)

           with col1:
              if st.button(f"✂Remove Duplicates from {file.name}"):
                 df.drop_duplicates(inplace=True)
                 st.write("Duplicates Removed")

           with  col2:
              if st.button(f"🌸Fill Missing Values for {file.name}"):
                  numeric_cols  = df.select_dtypes(include=['number']).columns
                  df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].main())
                  st.write("Missing Values have been Filled!")  


        # choose the Specfic columns to  keep or create
        st.subheader("🍒Select Columns to Convert")
        columns = st.multiselect(f"Choose Columns for{file.name}",df.columns, default=df.columns)
        df = df[columns]

        # create some visualizations
        st.subheader("⛎ Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
           st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])

        # convert the file--> CSV TO EXCEL
        st.subheader("Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:",["CSV","Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
           buffer = BytesIO()
           if conversion_type == "CSV":
              df.to_csv(buffer,index=False)
              file_name = file.name.replace(file_ext,".csv")
              mime_type = "text/csv"

           elif conversion_type == "Excel":
              file_name = file.name.replace(file_ext,".xlsx")
              mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
           buffer.seek(0)

             #    download button
           st.download_button(
              label=f"⏬ Download {file.name} as {conversion_type}",
              data=buffer,
              filename=file_name,
              mime=mime_type
            )
   st.success(f"🥙 All files processed!")
   
if st.button("Submit "):
      st.balloons()
      


