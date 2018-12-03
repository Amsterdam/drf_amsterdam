FROM amsterdam/python

RUN apt-get install -y spatialite-bin libsqlite3-mod-spatialite
COPY . /app/
RUN pip install -r /app/requirements.txt

WORKDIR /app/
