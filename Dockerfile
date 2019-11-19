FROM python:3
EXPOSE 8080
WORKDIR /code
COPY . /code
RUN pip install -r requirements.txt
CMD [ "python", "-u", "/code/server.py" ]
