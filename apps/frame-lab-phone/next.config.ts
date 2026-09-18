import type { NextConfig } from "next";
import os from "os";

function extraDevOrigins() {
  const hosts = new Set(["127.0.0.1", "localhost"]);
  for (const nets of Object.values(os.networkInterfaces())) {
    for (const net of nets ?? []) {
      if (net.family === "IPv4" && !net.internal) {
        hosts.add(net.address);
      }
    }
  }
  for (const extra of (process.env.ALLOWED_DEV_ORIGINS ?? "").split(",")) {
    const host = extra.trim();
    if (host) hosts.add(host);
  }
  return [
    ...hosts,
    "*.loca.lt",
    "*.localtunnel.me",
    "*.trycloudflare.com",
  ];
}

const nextConfig: NextConfig = {
  allowedDevOrigins: extraDevOrigins(),
};

export default nextConfig;
