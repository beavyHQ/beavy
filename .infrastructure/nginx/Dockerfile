FROM nginx:latest
RUN apt-get update -y
RUN apt-get install -y python-pip
RUN pip install j2cli
COPY start /start
RUN chmod +x /start
COPY nginx.tmpl /nginx.tmpl
CMD /start
EXPOSE 80
