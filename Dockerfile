FROM --platform=linux/amd64 mcr.microsoft.com/playwright:v1.44.1-jammy 

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y x11vnc xvfb
RUN apt-get -y clean;
RUN mkdir ~/.vnc
RUN x11vnc --version

WORKDIR /app
RUN npm i -g pnpm
COPY package.json ./
RUN pnpm install -P
COPY . ./

RUN x11vnc -storepasswd secretpassword ~/.vnc/passwd 
CMD xvfb-run --server-num 1 --auth-file /tmp/xvfb1.auth pnpm start & \
  x11vnc -usepw -display WAIT:1 -forever -auth /tmp/xvfb1.auth

EXPOSE 5900