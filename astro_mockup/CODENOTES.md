# Notes about programming with Astro

(First, check the [Installation notes](./INSTALL.md))

## Pages

Each page of the site is a file inside `./src/pages` dir.

This files must have 2 sections:

- First section between the first `---` and the second (and last) `---` belongs to JavaScript code.
- Second section (after the second `---`) is for HTML code.

## Adding styles

There are two tytpes of styles:

- Styles per file. It's the most used. You have to open an `<style>` element into the page/component file, within HTML section. If you want to use Scss code, it must have the lang attribute: `<style lang="scss"></style>`.
- Global styles. You can create a `./src/styles/` dir and create css/Sass files inside. Then, you must

## Adding vanilla JS scripts

JS code can be inserted into a page/component into HTML section like an `<script>` element.

Also, you can extract the JS code into a file (i.e. `./src/scripts/file.js`) and import it into the script element:

```html
<script>
  import '../scripts/file.js';
</script>
```

## Components

Components are like pages. Usually, component files goes into `./src/components/` dir (but they can be elsewhere).

After, components must be imported into a page, layout or other component with an import sentence:

```js
  import Component from '../components/Component.astro`;
```

and then, used like an HTML elemento (JSX style!):

```js
  <some_html_code>
    <Component>
  </some_html_code>
```

## Layout files

Layout are like pages too. You can create them into `./src/layouts/` dir. Also have two sections.

Layout files must be imported and used like a HTML element (like components).

You can pass parameters to layouts using HTML attributes. That parameters are collected into `Astro.props` global object inside the Layout file:

```astro
---
const { param1, param2 } = Astro.props;
```

In reality, layout files are components!

## Posts

Not used yet.

## Icons

For Astro, I'll use astro-feather <https://github.com/gabrlyg/astro-feather/tree/master>

Install:

```bash
bun add astro-feather
```

Use: 

```astro
---
// import only what you need
import { FeatherIcon } from 'astro-feather';
---
<FeatherIcon />
```