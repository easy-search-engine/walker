FROM python:3

WORKDIR /var/walker
ADD requirements.txt ./
RUN pip install -r requirements.txt

CMD [ "scrapy", "crawl", "jbzd" ]
