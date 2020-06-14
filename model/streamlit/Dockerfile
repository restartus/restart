# https://blog.jcharistech.com/2020/01/14/how-to-deploy-streamlit-apps-to-google-cloud-platformgcp-app-engine/
#

FROM python:3.7
LABEL maintainer="Rich Tong (rich@restart.us)"
# for demo purposes expose jupyter notebook
EXPOSE 8080
# Use bash
#SHELL ["/bin/bash", "-c"]

# Try to do a minimal installation
RUN pip install streamlit altair vega-datasets opencv-python

WORKDIR /app
COPY . /app

CMD streamlit run --server.port 8080 --servicenableCORS false app
