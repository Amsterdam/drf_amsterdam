FROM amsterdam/python

COPY . /app/
RUN pip install -r /app/requirements.txt
