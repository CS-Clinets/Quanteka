FROM python:3.11
ENV PYTHONUNBUFFERED=1
WORKDIR /quanteka2
COPY requirements.txt /quanteka2
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . .
CMD ["/quanteka2/manage.py", "runserver", "0.0.0.0:8000"]
EXPOSE 8080