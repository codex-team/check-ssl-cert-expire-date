FROM python:3
ADD main.py /
ADD config.py /
ADD requirements.txt /
RUN git clone https://github.com/richardpenman/pywhois
RUN pip3 install -r requirements.txt
ENTRYPOINT python3 main.py
