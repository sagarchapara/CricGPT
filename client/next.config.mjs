/** @type {import('next').NextConfig} */
const nextConfig = {
    output: "standalone",
    experimental: {
        // This will make the server listen on all network interfaces
        hostname: '0.0.0.0',
        port: 3000
    },
    webpack(config) {
        config.module.rules.push({
            test: /\.svg$/,
            use: ['@svgr/webpack'],
        });

        return config;
    },
};

export default nextConfig;