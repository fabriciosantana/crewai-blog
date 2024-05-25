#!/bin/bash
# Iniciar backend
cd backend
uvicorn app:app --host 0.0.0.0 --port 8000 &
# Iniciar frontend
cd ../frontend
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
