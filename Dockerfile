FROM neo4j:2.3.2
FROM python:3.5

RUN pip install requests
RUN pip install aiohttp
RUN pip install beautifulsoup4
RUN pip install py2neo
RUN pip install APScheduler
RUN pip install tornado

COPY . /src

EXPOSE 6464 

CMD ["python", "/src/crawler/server.py"]

