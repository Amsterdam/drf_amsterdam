FROM amsterdam/python
MAINTAINER datapunt@amsterdam.nl

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

RUN mkdir -p /static \
	&& mkdir /data \
	&& chown datapunt /data \
	&& chown datapunt /static

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

USER datapunt
COPY ./app/ /app/
COPY ./deploy/ /deploy/

RUN pwd
RUN python manage.py collectstatic --noinput

# Production no waits / migrates etc.
CMD ["/deploy/docker-run.sh"]
