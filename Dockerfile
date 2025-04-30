FROM ubuntu:20.04

# Install vnc, xvfb in order to create a 'fake' display and chrome
RUN 	export DEBIAN_FRONTEND=noninteractive
RUN 	export DISPLAY=0

RUN 	ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime

RUN 	apt-get update &&\
	 	apt-get install -y tzdata &&\ 
	 	dpkg-reconfigure --frontend noninteractive tzdata &&\
	 	apt-get install -y x11vnc xvfb zip wget curl psmisc gconf-service libasound2 libatk1.0-0 libatk-bridge2.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-bin libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils libgbm-dev nginx libcurl3-gnutls

RUN 	curl --silent --location https://deb.nodesource.com/setup_22.x | bash - &&\
		apt-get -y -qq install nodejs &&\
		apt-get -y -qq install build-essential &&\
		fc-cache -f -v

# Install noVNC
RUN apt-get update && apt-get install -y git python3 python3-pip && \
    git clone --depth 1 https://github.com/novnc/noVNC.git /opt/novnc && \
    git clone --depth 1 https://github.com/novnc/websockify /opt/novnc/utils/websockify && \
    ln -s /opt/novnc/vnc.html /opt/novnc/index.html

RUN echo "ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true" | debconf-set-selections && \
  apt-get -y -qq install software-properties-common &&\
  apt-add-repository "deb http://archive.canonical.com/ubuntu $(lsb_release -sc) partner" && \
  apt-get -y -qq --no-install-recommends install \
  fontconfig \
  fonts-freefont-ttf \
  fonts-liberation \
  fonts-noto-color-emoji \
  fonts-roboto \
  fonts-ubuntu \
  fonts-open-sans

RUN wget https://orbita-browser-linux.gologin.com/orbita-browser-latest.tar.gz -O /tmp/orbita-browser.tar.gz

# GOLOGIN INSTALL
RUN cd /tmp &&\
	tar -xzf /tmp/orbita-browser.tar.gz -C /usr/bin &&\
	rm -f /tmp/orbita-browser.tar.gz

RUN apt-get -qq clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# WORKER INSTALL

COPY package.json /opt/orbita/package.json
RUN cd /opt/orbita && npm install
	

# Add the browser user (orbita)
RUN groupadd -r orbita && useradd -r -g orbita -s/bin/bash -G audio,video,sudo -p $(echo 1 | openssl passwd -1 -stdin) orbita  \
  && mkdir -p /home/orbita/Downloads \
  && chown -R orbita:orbita /home/orbita

RUN echo 'orbita ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

RUN mkdir -p /home/orbita/.gologin/browser
RUN mkdir -p /home/orbita/.gologin/browser/fonts
# COPY fonts /home/orbita/.gologin/browser/fonts

RUN rm /etc/nginx/sites-enabled/default
COPY orbita.conf /etc/nginx/conf.d/orbita.conf
RUN chmod 777 /var/lib/nginx -R
RUN chmod 777 /var/log -R
RUN chmod 777 /run -R
#sudo orbita
RUN usermod -a -G sudo orbita

EXPOSE 3000
EXPOSE 6080
EXPOSE 5901

COPY index.js /opt/orbita/index.js
COPY entrypoint.sh /entrypoint.sh

RUN	 chmod 777 /entrypoint.sh \
	&& mkdir /tmp/.X11-unix \
	&& chmod 1777 /tmp/.X11-unix 

USER root
ENTRYPOINT ["/entrypoint.sh"]