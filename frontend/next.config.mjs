const backendInternalUrl =
  process.env.BACKEND_INTERNAL_URL?.replace(/\/$/, "") || "http://127.0.0.1:8000";

const isGithubPages = process.env.GITHUB_PAGES === "true";
const explicitBasePath = process.env.NEXT_PUBLIC_BASE_PATH?.trim() || "";
const normalizedBasePath = explicitBasePath.replace(/^\/|\/$/g, "");
const repositoryName = process.env.GITHUB_REPOSITORY?.split("/")[1] || "";
const basePath =
  normalizedBasePath.length > 0
    ? `/${normalizedBasePath}`
    : isGithubPages && repositoryName
      ? `/${repositoryName}`
      : "";

/** @type {import('next').NextConfig} */
const nextConfig = {
  ...(isGithubPages
    ? {
        output: "export",
        trailingSlash: true,
        basePath,
        assetPrefix: basePath,
        images: {
          unoptimized: true,
        },
      }
    : {}),
  async rewrites() {
    if (isGithubPages) {
      return [];
    }

    return [
      {
        source: "/backend/:path*",
        destination: `${backendInternalUrl}/:path*`,
      },
    ];
  },
};

export default nextConfig;
