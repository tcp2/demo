import { GologinApi } from "gologin";

const SCREEN_WIDTH = process.env.SCREEN_WIDTH;
const SCREEN_HEIGHT = process.env.SCREEN_HEIGHT;

const params = {
  token: process.env.TOKEN,
  profile_id: process.env.PROFILE_ID,
  remote_debugging_port: 3500,
  executablePath: "/usr/bin/orbita-browser/chrome",
  extra_params: [
    "--start-maximized",
    "--disable-dev-shm-usage",
    "--no-sandbox",
    "--no-zygote",
    "--window-position=0,0",
    `--window-size=${SCREEN_WIDTH},${SCREEN_HEIGHT}`,
  ],
};

const gl = GologinApi(params);

async function main() {
  const { browser } = await gl.launch({
    cloud: false,
    headless: false,
  });
}

main();
