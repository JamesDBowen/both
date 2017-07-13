FROM python
 RUN mkdir /app
 RUN apt-get update
 RUN apt-get install -y libenchant1c2a
 WORKDIR /app
 ADD requirements.txt /app/
 ADD startup.sh /app/
 RUN pip install -r requirements.txt
 RUN django-admin.py startproject both
 WORKDIR /app/both
 COPY ./app/ /app/both/both
 EXPOSE 8000
 EXPOSE 8005

 
 ENTRYPOINT /app/startup.sh
