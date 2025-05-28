FROM python:3.10-slim

WORKDIR /backend

COPY requirements.txt . 

RUN apt update
RUN apt install -y gcc libmariadb-dev
RUN pip install --no-cache-dir -r requirements.txt

COPY src/backend/ .

EXPOSE 8003

CMD ["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "8003"]

