FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=America/New_York

#Install only necessary runtime packages
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get install -y tzdata && \
    dpkg-reconfigure --frontend noninteractive tzdata &&\
    apt-get install -y ca-certificates x11vnc xvfb zip wget curl nginx gnupg dumb-init git psmisc supervisor gconf-service libasound2 libatk1.0-0 libatk-bridge2.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-bin libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils libgbm-dev libcurl3-gnutls

RUN echo "ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true" | debconf-set-selections && \
    apt-get -y -qq install software-properties-common &&\
    apt-add-repository "deb http://archive.canonical.com/ubuntu $(lsb_release -sc) partner" && \
    apt-get -y -qq --no-install-recommends install \
    fontconfig \
    fonts-freefont-ttf


COPY . /app
WORKDIR /app

COPY requirements.txt /tmp/
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt && rm /tmp/requirements.txt

RUN apt-get -qq clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# ln python3 to python
RUN ln -s /usr/bin/python3 /usr/bin/python

# Copy nginx config
RUN rm -f /etc/nginx/sites-enabled/default
COPY .docker/app.conf /etc/nginx/conf.d/app.conf

# Ensure permissions for nginx, logs
RUN chmod -R 777 /var/lib/nginx /var/log /run

RUN wget https://orbita-browser-linux.gologin.com/orbita-browser-latest.tar.gz -O /tmp/orbita.tar.gz && \
tar -xzf /tmp/orbita.tar.gz -C /usr/bin && \
rm -f /tmp/orbita.tar.gz

EXPOSE 3500
EXPOSE 5901
EXPOSE 8000
EXPOSE 9000

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN mkdir /tmp/.X11-unix && chmod 1777 /tmp/.X11-unix 

USER root
ENTRYPOINT ["/entrypoint.sh"]
