# Use python, version 3.6 as the base image.
# We won't install debian packages, so just use the slim variant.
FROM python:3.6

# Install required python packages
# Note: This way of formating the instruction allows to easily
# add/remove/comment packages




ENV PYTHONUNBUFFERED=1


RUN mkdir -p /work
WORKDIR /work


COPY requirements.txt /work/requirements.txt



RUN pip install -r requirements.txt

ADD /data/displaydata.csv  /work/assets/displaydata.csv
ADD /data/trufeed.csv  /work/assets/trufeed.csv
ADD /data/Englishnlp.csv  /work/assets/Englishnlp.csv
ADD /data/Turkishnlp.csv  /work/assets/Turkishnlp.csv
ADD /data/langtype.csv  /work/assets/langtype.csv
ADD /data/finaldf.csv  /work/assets/finaldf.csv

ADD index.py  /work/index.py 
ADD wsgi.py /work/wsgi.py
ADD app.py /work/app.py 



### the applications
ADD apps/app1.py /work/apps/app1.py 
ADD apps/app2.py /work/apps/app2.py
ADD apps/displayAll.py /work/dynamic/displayAll.py
ADD apps/app3.py /work/apps/app3.py 
ADD apps/app4.py /work/apps/app4.py 
ADD apps/app5.py /work/apps/app5.py 
ADD apps/app6.py /work/apps/app6.py 
ADD apps/app7.py /work/apps/app7.py 
ADD apps/app8.py /work/apps/app8.py
ADD apps/loader.py /work/dynamic/loader.py
#ADD apps/__init__.py /work/dynamic/__init__.py  
ADD apps/home.py /work/dynamic/home.py


ADD apps/__init__.py /work/apps/__init__.py  

# statistical models app
ADD apps/dask_dash_app3/ldacomplaints.py  /work/apps/dask_dash_app3/ldacomplaints.py
ADD apps/dask_dash_app3/app_sm.py /work/apps/dask_dash_app3/app_sm.py 
ADD apps/dask_dash_app3/local_plots.py /work/apps/dask_dash_app3/local_plots.py 
ADD apps/dask_dash_app3/precomputing.py /work/apps/dask_dash_app3/precomputing.py 
ADD apps/dask_dash_app3/precomputed.json /work/apps/dask_dash_app3/precomputed.json
# ADD apps/dask_dash_app3/trufeed.csv /work/apps/dask_dash_app3/trufeed.csv
# ADD apps/dask_dash_app3/trufeed.csv /work/apps/dask_dash_app3/data/trufeed.csv


### the css files and images
ADD static/plotly(8).png /work/assets/plotly(8).png
ADD static/plotly(9).png /work/assets/plotly(9).png
ADD static/plotly(10).png /work/assets/plotly(10).png
ADD static/plotly(12).png /work/assets/plotly(12).png
ADD static/6.png /work/assets/6.png
ADD static/7.png /work/assets/7.png
ADD static/8.png /work/assets/8.png
ADD static/9.png /work/assets/9.png
ADD static/10.png /work/assets/10.png
ADD static/custom.css /work/assets/custom.css
ADD static/GUI.css /work/assets/GUI.css
ADD static/searchTermsColor.html /work/assets/searchTermsColor.html
ADD static/turkey1.jpg /work/assets/turkey1.jpg
ADD static/world_map-2.jpg /work/assets/world_map-2.jpg


#RUN rm -rf /var/lib/apt/lists/*
# forward request and error logs to docker log collector
#RUN ln -sf /dev/stdout /var/log/apache2/error.log \
#	&& echo 


## change it to display.py to run secind script
CMD [ "python", "-u" ,"./index.py" ]


# Declare port 8888
EXPOSE 8050
