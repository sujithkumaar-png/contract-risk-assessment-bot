import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  poweredByHeader: false,
  // Keep production build worker use modest on an 8 GB development laptop.
  experimental: { cpus: 1 },
};

export default nextConfig;
