# InsightYouth WeChat Article Formatting Skill

An **AI Skill** that turns a finished Chinese article into publish-ready rich-text HTML for **WeChat Official Accounts** (公众号 — the publishing platform inside WeChat). You write the words; it handles layout, typography, color, tables and highlights, then hands you a page with a one-click "copy全文" button. Paste into the WeChat editor and the styles survive.

> **Honest scope note:** WeChat Official Accounts are a China-specific platform, so if you don't publish there, this tool won't be directly useful to you. It is shared here for two other reasons that travel better: the **AI-Skill pattern** (packaging a repeatable content workflow into a single `SKILL.md` that an AI agent can execute), and the **constrained-HTML compatibility work** in `references/wechat-compat.md` — the same class of problem as HTML email, where a restricted editor strips most of your CSS.

**Live demo** (full template, 9 switchable palettes, working copy button):
<https://workbuddy.link/p/Te93B0yDG3i2QhXqN3tF2E>

---

## The problem it solves

WeChat's editor is notoriously hostile to formatting: it strips classes, rejects most CSS, and mangles pasted content. Formatting a long-form article by hand — tables, quotes, highlight boxes, section rhythm — easily eats 30–60 minutes per piece, and the result is inconsistent across posts.

This skill moves that work to the AI agent. You hand over plain text or Markdown; it returns a styled HTML page. Your original wording is never rewritten — only structural markers are added.

## What it does

| Capability | You say |
|---|---|
| Apply the layout | "Format this with InsightYouth style" / "make it WeChat-ready" |
| Switch palette | Click any of the 9 dots in the page header, then copy |
| Tune the template | "Make table headers bigger" / "rounder tag pills" / "add highlighter to pull quotes" |

**Built-in modules:** follow-guide GIF (inlined), lede paragraph, three-line tables (rounded header + zebra rows), blockquotes, highlighter pull quotes, image slots with captions, risk-disclosure boxes, topic pills, "previously on" list, author card slot.

**Nine palettes:** Ink Green (default) / Graphite / Bamboo / Navy / Lake Blue / Wisteria / Olive / Crimson / Ochre.

## Install

This is an **Agent Skill** — a folder with a `SKILL.md` that an AI coding assistant reads to learn the workflow. It follows the Agent Skills frontmatter convention (`name` + `description`), so it works with assistants that support that format.

Tell your AI assistant:

```
Install https://github.com/lennyash/insightyouth-skill
```

The agent clones the repo into its skills directory (e.g. `~/.workbuddy/skills/InsightYouth-style/`). Start a **new session** afterward for it to take effect.

To install manually, clone the repo into your assistant's skills folder.

## Usage

Hand the article to your AI assistant — paste the text inline, or point it at a `.md` / `.txt` file — and say **"format this with InsightYouth style"**.

The agent adds structural markers (headings, lists, tables, quotes, risk notes) **without changing a single word of your copy**, then renders HTML. Click **"一键复制全文"** (copy all) on the generated page and paste into the WeChat editor.

You can also run the renderer directly:

```bash
python3 scripts/build.py references/sample-article.md -o output.html
```

`references/sample-article.md` is a complete sample exercising every module.

## Project structure

```
InsightYouth-style/
├── SKILL.md                    # the skill contract — the AI reads this to do the job
├── assets/
│   ├── template.html           # layout template (inlined GIF, palette switcher, copy script)
│   └── follow-guide.gif        # follow-guide animation source
├── scripts/
│   └── build.py                # Markdown → WeChat HTML (stdlib only, any python3)
└── references/
    ├── style-spec.md           # full style spec: colors, type scale, module skeletons
    ├── wechat-compat.md        # WeChat compatibility notes / gotchas
    └── sample-article.md       # sample article covering all modules
```

## Implementation notes

- **Zero dependencies.** `build.py` uses only the Python standard library — no `pip install`, runs on any Python 3.
- **Inline styles everywhere.** Required by WeChat's editor; this is why the output survives paste. The compatibility research behind it is written up in `references/wechat-compat.md` and generalizes to other restricted-HTML targets (HTML email, for instance).
- **Palette switching is a whole-document replace.** All 9 schemes derive from `THEMES[0]`, so changing the default palette means editing both `assets/template.html` and the constants at the top of `build.py` in lockstep.
- **The article text is never rewritten.** Only Markdown structural markers are added — punctuation, numbers and domain phrasing are preserved verbatim.

## Requirements

Python 3 (standard library only). Works on Windows, macOS and Linux.

## License

MIT — see [LICENSE](LICENSE). Free to use, fork and adapt.

## About

Built by **有悟青年 / InsightYouth**, a finance content creator automating his own publishing pipeline. Part of a broader set of experiments in turning repetitive content work into reusable AI skills and products.

- Site: <https://www.insightyouth.cn>
- Mirror on Gitee: <https://gitee.com/lennyash/insightyouth-skill>
