# https://medium.com/usf-msds/deploying-web-app-with-streamlit-docker-and-aws-72b0d4dbcf# https://maelfabien.github.io/project/Streamlit/#7
FROM python:3.7
EXPOSE 8501
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD streamlit run dashboard.py
