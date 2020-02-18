FROM python:3

MAINTAINER Jason Ashby "jashby2@gmail.com"

WORKDIR /usr/src/app

RUN apt-get -y update && \
    apt-get install -y sqlite3

# node/npm install
RUN curl -sL https://deb.nodesource.com/setup_13.x | bash -
RUN apt-get install -y nodejs

COPY . /usr/src/app

RUN mkdir -p /usr/src/app/uploads && chmod 750 /usr/src/app/uploads

RUN pip install --no-cache-dir -r requirements.txt

RUN npm install

# create bundle.js with webpack
RUN npm run --silent prod

# create tables
RUN cat backend/nmap_tables.sql | sqlite3 backend/nmap.db

CMD [ "python", "./server.py" ]
