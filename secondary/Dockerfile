FROM python:3.10.13-slim
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
