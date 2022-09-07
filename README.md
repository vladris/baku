# Baku

![Baku](baku.png)

Baku is a simple, Markdown-based blogging engine/static website generator. Baku is the spiritual successor to [Tinkerer](https://github.com/vladris/tinkerer).

## Getting started

Install Baku from PyPI:

```
pip install baku
```

Set up your blog:

```
md blog
cd blog
baku --init
```

Update the newly generated `blog.cfg` file to add your name as the author.

## Posting

Create a new post using the command line `-p` or `--post` argument:

```
baku --post "This is my first post"
```

This will generate a new Markdown file under a path representing today's date.
For example if today were September 1st, 2022, you would see the following new
file: `2022/09/01/this-is-my-first-post.md`.

Date can be overriden with the `--date` argument:

```
baku --post "This is my first post" --date 2022/09/01
```

Will explicitly set the date to September 1st, 2022.

## Build

Build your blog using the `--build` command:

```
baku --build
```

This will generate the static blog website under the `html` folder. You can
publish this, for example using [GitHub Pages](https://pages.github.com/)

## Drafts

You can create a draft using the `-d` or `--draft` argument:

```
baku --draft "This is my draft"
```

This will create `drafts/this-is-my-draft.md`. Drafts are ignored during build
(more on build below).

You can promote a draft to a post by passing an existing draft to the `--post`
command:

```
baku --post drafts/this-is-my-draft.md
```

This will move the file from `drafts` to today's date. Similarly, you can
turn a post into a draft by passing an existing post to the `--draft` command:

```
baku --draft 2022/09/01/this-is-my-first-post.md
```

This will move the post from `2022/09/01` to the `drafts` folder.

## Directory layout

When you initialize a new blog, Baku will create a couple of directories:
`templates` and `static`.

The `static` directory contains a default icon for the website and a couple of
CSS files. The content of this directory is copied to the build directory.

In fact, all files that are not `.md` files and that are not under root,
`templates` or `drafts` are copied to the build directory.

The build directory is `html` and it gets cleaned up with each build.

## Templates

The `templates` directory contains the HTML templates used for building posts
and `index.html`. Baku uses a custom, simple templating engine to avoid
dependencies. Variables between `{{` and `}}` are evaluated as follows:

* `{{ if <expr> }}` is a conditional expression which needs a matching
  `{{ endif }}`. During template rendering, Baku will evaluate `<expr>`. If
  the result is truthy, the text and expressions until `{{ endif }}` will
  be evaluated, otherwise they will be skipped.

* `{{ for <expr> }}` is a loop expression which needs a matching
  `{{ endfor }}`. During template rendering, Baku will iterate over the
  result of evaluating `<expr>` and will repeatedly evaluate the text and
  expressions until `{{ endfor }}` for each item in the result. A `$item`
  representing the result item will be available in the context.

* All other expressions are evaluated as references to values in the context
  (e.g. `{{ a.b.c }}`). A `&` after an expression HTML-escapes the value
  (e.g. `{{ a.b.c & }}` will HTML-escape `a.b.c`). A `%` followed by a format
  string will apply date formatting to the value using `strftime()` (e.g.
  `{{ a.b.c & %B %d %Y }}`).

The context used during post rendering includes all values in `blog.cfg`. When
rendering posts, the context includes a `post` variable with various post data.
When rendering the index, the context includes `years`, each year containing a
`year` value and a list of posts (`posts`).
