import streamlit as st
import requests
import os

# We use an environment variable so Kubernetes can inject the address later
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

st.title("🤖 AI Sentiment Analyzer V2 ")
st.write("Enter a sentence to see if it's Positive, Negative, or Neutral.")

user_input = st.text_area("Type here...")

if st.button("Analyze"):
    if user_input:
        try:
            response = requests.post(f"{BACKEND_URL}/analyze", json={"text": user_input})
            if response.status_code == 200:
                data = response.json()
                st.success(f"Sentiment: **{data['sentiment']}**")
                st.info(f"Confidence Score: {data['score']}")
            else:
                st.error("Error from API")
        except Exception as e:
            st.error(f"Could not connect to backend at {BACKEND_URL}")
            st.error(e)
    else:
        st.warning("Please type something first.")