FROM python

WORKDIR /app

COPY main.py requirements.txt Makefile ./

RUN make install

EXPOSE 53

CMD ["make", "run"]