# Hugo development server with hot reloading
FROM hugomods/hugo:latest

WORKDIR /src

# Default to development mode
ARG BASE_URL=https://dev-site.ocortez.com/
ENV BASE_URL=${BASE_URL}

EXPOSE 1313

# Run Hugo dev server with live reload
CMD ["hugo", "serve", "--bind", "0.0.0.0", "--port", "1313", "--appendPort=false", "--liveReloadPort=443", "--baseURL", "https://dev-site.ocortez.com/"]
