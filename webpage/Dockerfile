FROM python:3
RUN pip install --no-cache-dir  tornado  gviz_api mysqlclient
RUN mkdir demo
COPY . /demo
WORKDIR /demo
CMD [ "python", "main.py" ]
