import streamlit as st

st.set_page_config(page_title="Sportska Analitika", layout="wide")

st.title("Dobrodošli u bazu za analizu")
st.write("Ovdje krećemo sa izgradnjom novog sistema od nule.")

sport = st.selectbox("Izaberi sport za početnu analizu:", ["Fudbal (3+ golovi)", "Košarka (Margine poena)"])

if st.button("Pokreni sistem"):
    st.success(f"Sistem spreman za modul
