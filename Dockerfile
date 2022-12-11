RUN pip3 install -U pip

COPY . .

RUN pip3 install -U -r requirements.txt

CMD ["python3","main.py"]
