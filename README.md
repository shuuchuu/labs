# `labs`

Colab lab notebooks referenced from [shuuchuu/slides](https://github.com/shuuchuu/slides)
training decks, mirrored here from Google Drive/GitHub so they have a stable,
version-controlled home.

## Layout

```
notebooks/<topic>/<lab>/<type>-<lang>.ipynb
```

e.g. `notebooks/nn/cnn/landscape-classification-keras/hands-on-fr.ipynb`.

- `<topic>` is the path of the training section the lab was written for, as it was when
  the lab was created. It is an identifier, not a mirror: it doesn't follow the section if
  that section later moves.
- `<lab>` is a lowercase ASCII, kebab-case English name of what the notebook does, e.g.
  subject + dataset + framework (`author-identification-keras`). DL labs always name their
  framework (`keras`, `tensorflow`, `pytorch`, `lightning`). No ordering numbers, dates,
  client or deck names, and no "tp"/"lab"/"exercise" words (`exercises` is the one
  exception, for a section's generic exercise set).
- `<type>` is `hands-on` (trainees write code: exercises, usually with collapsed
  "Solution" sections) or `demo` (runs start to finish, shown by the trainer).
- `<lang>` is `fr` or `en`: the language the notebook is written in. An untranslated
  notebook exists in one language only. A copy in the other language's name isn't allowed.

## Published paths never change

Colab opens a notebook from its URL:

```
https://colab.research.google.com/github/shuuchuu/labs/blob/main/notebooks/<path>
```

These URLs are printed in PDFs handed to trainees, so a notebook, once published, is never
renamed, moved or deleted. When a lab is rewritten, edit it in place. When a lab changes
so much that it's a different lab, give it a new name and leave the old one published.

`uv run doit publish-labs` (in shuuchuu/slides) enforces this: it refuses to publish if a
path shuuchuu/labs already has is missing, or if a notebook path doesn't follow the
layout. `--break-published-links` overrides the first check. It exists for the one-off
switch to this layout (2026-09-25), done before any PDF linking to the old paths had been
handed out.

Decks link notebooks with the `lab` Jinja filter, never with a hand-written URL (see
`markdown-guide.md` in shuuchuu/slides).
