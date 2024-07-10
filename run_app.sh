#!/bin/bash

# Run ollama
ollama run mistral:latest &

# wait for ollama to roll
sleep 5

# Run Streamlit
streamlit run app.py