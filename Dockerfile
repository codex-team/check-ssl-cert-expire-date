FROM python:3
ADD main.py /
ADD config.py /
RUN git clone https://github.com/richardpenman/pywhois
RUN pip install requests future
ENTRYPOINT python3 main.py
