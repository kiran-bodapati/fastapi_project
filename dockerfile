FROM python:3.10
WORKDIR /app
#RUN apt-get update && apt-get install -y python3  python3-pip
RUN mkdir -p /var/log
COPY main.py /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
EXPOSE 8000
EXPOSE 5000
CMD  uvicorn main:app --host 0.0.0.0 --port 8080 --reload > /var/log/application1_outlogs.log 2> /var/log/application1_errlogs.log &\
    uvicorn main:application --host 0.0.0.0 --port 8000 --reload >  /var/log/application2_outlogs.log  2> /var/log/application2.errlogs.log
