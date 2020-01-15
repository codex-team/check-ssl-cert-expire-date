FROM python:3
ADD main.py /
ADD config.py /
ADD requirements.txt /
RUN pip3 install -r requirements.txt
RUN pip3 install git+https://github.com/richardpenman/pywhois
ENTRYPOINT python3 main.py
