# Streamlit and building a graphical application

[Streamlit](https://link.medium.com/AtvAhw3Mh7) is a new library that is way
easier than Flask for creating applications.

The complete stack looks like:

1. Python PIP modules for integration into existing systems
2. Streamlit for display which you can easily get running with Docker and Google
   App Engine
3. For backend modules, do a REST api with Flask to create a nice service

## Demo application

### [stock.py](https://link.medium.com/AtvAhw3Mh7)
A stock demonstration that pulls from Yahoo

### [car detection](https://link.medium.com/KWw8FN7Qh7)
This shows how to build for Heroku. But the cool thing is that it shows. Note
that you don't want to check in the weights that are automagically downloaded

```
pip install streamlit opencv-python
# YOLO Detection
streamlit run https://raw.githubusercontent.com/streamlit/demo-self-driving/master/app.py
# Uber pickup 
streamlit run https://raw.githubusercontent.com/streamlit/demo-uber-nyc-pickups/master/app.py
```
