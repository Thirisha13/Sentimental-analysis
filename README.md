# Secure Sentiment Analysis App using BERT + LoRA

## Overview

This project is an end-to-end machine learning application that combines Natural Language Processing (NLP) with secure authentication.

It uses a fine-tuned BERT model enhanced with LoRA (Low-Rank Adaptation) for sentiment analysis, integrated with Keycloak-based authentication and a simple UI built using Streamlit.

---

## Features

* User authentication using Keycloak
* Sentiment analysis using BERT (LoRA fine-tuned)
* Role-based access control (e.g., student, teacher)
* Interactive UI using Streamlit
* Real-time sentiment prediction

---

## Project Structure

```
.
├── app.py                              # Main Streamlit application
├── bert-model-lora-optimized.ipynb     # Model training notebook (LoRA fine-tuning)
├── lora_bert_sentiment/                              # model files
│   ├── adapter_config.json
│   ├── tokenizer.json
│   ├── special_tokens_map.json
│   └── tokenizer_config.json
├── requirements.txt
├── README.md
└── .env.example
```

---

## How It Works

1. User logs in via Keycloak authentication
2. Access is granted based on roles overhere student and teachers where teachers are allowed to do sentimental analysis
3. User inputs text into the UI
4. The fine-tuned BERT model processes the text
5. Sentiment (Positive/Negative) is returned with probabilities

---

## Model Details

* Base Model: BERT (bert-base-uncased)
* Fine-tuning: LoRA (Low-Rank Adaptation)
* Task: Sequence Classification (Sentiment Analysis)

The training process is available in:

```
bert-model-lora-optimized.ipynb
```

---

## How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set environment variables

Create a `.env` file based on `.env.example`:

```
KEYCLOAK_SERVER_URL=http://localhost:3000/
KEYCLOAK_CLIENT_ID=your-client-id
KEYCLOAK_CLIENT_SECRET=your-secret
```

### 4. Run the application

```bash
streamlit run app.py
```

---

## Sample Usage

Input:
"I really like this application!"

Output:
Sentiment: Positive
Confidence: 0.98

---

## Security Note

* Sensitive credentials (e.g., Keycloak secrets) are not stored in code
* Environment variables are used for secure configuration

---

## Future Improvements

* Add neutral sentiment class
* Deploy application (Streamlit Cloud or AWS)
* Add REST API using FastAPI
* Improve model performance with larger datasets

---

## Author

Thirisha M

---

## Acknowledgements

* Hugging Face Transformers
* Streamlit
* Keycloak

---
