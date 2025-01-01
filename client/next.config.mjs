/** @type {import('next').NextConfig} */
const nextConfig = {
    output: "standalone",
    webpack(config) {
        config.module.rules.push({
            test: /\.svg$/,
            use: ['@svgr/webpack'],
        });

        return config;
    },
    env: {
        NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL, // Expose the API URL
    },
};

export default nextConfig;
