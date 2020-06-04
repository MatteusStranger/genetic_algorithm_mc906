
FROM python:3.7.7-slim-stretch
 
WORKDIR /app
ENV PYTHONPATH=/app

RUN apt-get update &&\
    apt-get -y upgrade &&\
    apt-get -y install gcc&&\
    apt -y autoremove

COPY requirements.txt .

RUN  pip install --no-cache-dir -r requirements.txt

COPY . /app 

VOLUME [ ":/app" ]

EXPOSE 8888

RUN cd /usr/local/lib/python3.7/site-packages && \
    python /app/gen_function/setup.py develop

RUN pip install -e gen_function/

CMD ["/bin/bash"]