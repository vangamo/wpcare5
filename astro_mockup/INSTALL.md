# Installation instructions

## Install bum

<https://bun.sh/docs/installation>

```bash
curl -fsSL https://bun.sh/install | bash

# Added "~/.bun/bin" to $PATH in "~/.bashrc"

source /home/vangamo/.bashrc

bun -v
# 1.0.30
```

## Create Astro project with Bun

<https://docs.astro.build/en/recipes/bun/>

```bash
bunx create-astro@latest my-astro-project-using-bun --template eliancodes/brutal
bunx create-astro@latest astro_mockup --template minimal

# Typescript -> No
# Install dependencies -> Yes
# Initialize repo -> No
```

( Cool Astro template to look in -> [FlowBite](https://astro.build/themes/details/flowbite/) )

## Run project

```bash
# bun run dev?
bunx --bun astro dev
```

## Build project into dist directory

```bash
bunx --bun astro build
```

## Add Sass

<https://docs.astro.build/en/guides/styling/#sass-and-scss>

```bash
bun install -d sass
```
