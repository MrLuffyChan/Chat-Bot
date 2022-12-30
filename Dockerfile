FROM python:3.10.9

RUN pip install -U -r requirements.txt

CMD ["python3","main.py"]
