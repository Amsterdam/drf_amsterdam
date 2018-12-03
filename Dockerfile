FROM amsterdam/python

RUN apt-get install -y spatialite-bin sqlite
COPY . /app/
RUN pip install -r /app/requirements.txt

WORKDIR /app/
