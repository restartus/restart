# https://medium.com/usf-msds/deploying-web-app-with-streamlit-docker-and-aws-72b0d4dbcf# https://maelfabien.github.io/project/Streamlit/#7
MAINTAINER rich@restart.us
FROM python:3.8
# copy the application
COPY . /app
WORKDIR /app
# install packages
RUN pip install pipenv
RUN pipenv install --system --deploy

EXPOSE 8501
CMD streamlit run dashboard.py
