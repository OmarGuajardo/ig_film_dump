FROM python:3.9.6
WORKDIR /app
RUN echo '{}' > settings.json
RUN mkdir -p /app/static/media
COPY ./requirements.txt /app
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 1234
ENV FLASK_APP=main.py
ENV TZ="America/Los_Angeles"
CMD ["python3", "main.py", "--host", "0.0.0.0"]