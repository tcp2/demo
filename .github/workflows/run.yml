name: VNC with Ngrok in Docker

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  setup-vnc:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v2
      - name: Start Chrome with noVNC
        run: |
          docker run -d \
            -p 5980:5980 \
            -e RESOLUTION=1280x720x24 \
            --name browser \
            nkpro/chrome-novnc
          sleep 8

      # Install Ngrok
      - name: Install ngrok
        run: |
          curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
          echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
          sudo apt update && sudo apt install ngrok
      
      # Start ngrok tunnel for VNC and noVNC
      - name: Start ngrok tunnels for remote access
        env:
          NGROK_AUTH_TOKEN: 2QbyRGbKo6nke3jchCvGzNLRVCx_5WdiY2dfgqmbnwBUU3Bzv
        run: |
          run: |
          curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
          echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
          sudo apt update && sudo apt install -y ngrok jq
          ngrok authtoken $NGROK_AUTH_TOKEN
          ngrok http 5980 --log=stdout > ngrok.log &

      # Create connection instruction file
      - name: Wait and show access URL
        run: |
          sleep 10
          curl -s http://127.0.0.1:4040/api/tunnels | jq -r '.tunnels[0].public_url' > url.txt
          echo "::notice::🌐 Access Chrome via noVNC at: $(cat url.txt)"

      - name: Keep session alive
        run: tail -f ngrok.log
