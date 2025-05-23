FROM python:3.13.0

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install -e .

CMD ["python", "src/main.py"]
