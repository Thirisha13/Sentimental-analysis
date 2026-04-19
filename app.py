import streamlit as st
from streamlit_authenticator import Authenticate
from keycloak import KeycloakOpenID
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
from datetime import datetime, timedelta
from transformers import logging
import traceback
import jwt 
import requests

logging.set_verbosity_error()

# Keycloak Configuration
KEYCLOAK_SERVER_URL = "http://localhost:3000/"
KEYCLOAK_REALM_NAME = "master"
KEYCLOAK_CLIENT_ID = "test-client"
KEYCLOAK_CLIENT_SECRET = "Your client secret here"

# Roles Allowed to Use the App
ALLOWED_ROLES = {"student", "teacher"}

# Keycloak OpenID Client
keycloak_openid = KeycloakOpenID(
    server_url=KEYCLOAK_SERVER_URL,
    client_id=KEYCLOAK_CLIENT_ID,
    realm_name=KEYCLOAK_REALM_NAME,
    client_secret_key=KEYCLOAK_CLIENT_SECRET
)
# Load BERT Sentiment Analysis Model and Tokenizer
MODEL_PATH = "./lora_bert_sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

# Sentiment Analysis Function
def analyze_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probabilities = F.softmax(logits, dim=1)
        predicted_label = torch.argmax(probabilities, dim=1).item()
    return "Positive" if predicted_label == 1 else "Negative", probabilities[0].tolist()

# App Title
st.title("BERT Sentiment Analysis ")
st.subheader("                  -By Thirisha.M")

# Check Authentication
username = st.session_state.get("authenticated_username", None)

if username:
    # User is already authenticated
    access_token = st.session_state.get("access_token")
    st.success(f"Welcome back, {username}!")
    st.subheader("Sentiment Analysis")
    
    # Sentiment Analysis Section
    user_input = st.text_area("Enter a sentence to analyze", placeholder="Type your sentence here...")
    if st.button("Analyze"):
        if user_input.strip():
            sentiment, probabilities = analyze_sentiment(user_input)
            st.write(f"**Sentiment:** {sentiment}")
            st.write(f"**Probabilities:** Negative: {probabilities[0]:.2f}, Positive: {probabilities[1]:.2f}")
        else:
            st.warning("Please enter a sentence to analyze.")
    
    # Logout Section
    if st.button("Logout"):
        del st.session_state["authenticated_username"]
        st.success("Logged out successfully!")
        st.rerun()
else:
    # Login Section
    st.subheader("User Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        try:
            print(username, password)
            token = keycloak_openid.token(username, password)
            user_roles = set(keycloak_openid.decode_token(token['access_token'])["resource_access"].get(KEYCLOAK_CLIENT_ID, {}).get("roles", []))
            
            print(f'User Roles : {user_roles}')

            userinfo = keycloak_openid.userinfo(token["access_token"])

            print(userinfo)

            # Check User Roles
            if ALLOWED_ROLES & user_roles:
                # Set session cookie
                expiration = datetime.utcnow() + timedelta(days=1)  # Cookie expires in 1 day
                # Save username in session state
                st.session_state["authenticated_username"] = username
                st.success(f"Welcome, {userinfo['preferred_username']}!")
                
                # Reload the page to access the app
                st.rerun()
            else:
                st.error("Unauthorized: You do not have the required permissions to access this app.")
        except Exception as e:
            traceback.print_exc()
            st.error("Unauthenticated: Invalid username or password.")
