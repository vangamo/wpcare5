# use the official Bun image
# see all versions at https://hub.docker.com/r/oven/bun/tags
FROM oven/bun:1.0.20
WORKDIR /usr/src/app
RUN chown -R bun:bun /usr/src/app
USER bun

# copy Astro config files
COPY --chown=bun:bun astro_frontend/astro.config.mjs astro_frontend/tsconfig.json .

# install requirements
COPY --chown=bun:bun astro_frontend/package.json astro_frontend/bun.lockb .
RUN bun install

# run the app

EXPOSE 4321/tcp
#ENTRYPOINT [ "bunx", "--bun", "astro", "dev", "--host" ]
