# 有悟青年公众号文章排版 Skill（InsightYouth-style）

这是一个 AI Skill——安装后，你的 AI 助手就能把一篇写好的中文财经 / 投资类文章，直接排成可以在微信公众号发布的富文本：白底淡绿、克制留白，表格、引用、金句荧光笔、话题胶囊、风险提示、往期精选等模块齐备，生成一个带「一键复制全文」按钮的 HTML，复制后粘进公众号编辑器即可，样式不丢。

## 在线演示

排版模板的完整效果（含九套配色切换、一键复制按钮）可在线查看：

> **https://workbuddy.link/p/Te93B0yDG3i2QhXqN3tF2E**

打开后点顶栏右侧的配色圆点可整套切换配色，点「一键复制全文」即可直接体验。

## 这个 Skill 能做什么

| 能力 | 你可以说 |
|---|---|
| 套用排版 | 「把这篇套用有悟青年浅绿排版」「帮我排成公众号文章」 |
| 换配色 | 成品页面顶栏九个配色圆点（默认墨绿），一键整套切换后复制 |
| 调整模板 | 「表格名大一号」「标签改圆角胶囊」「金句加荧光笔」 |

**内置模块**：关注引导动图（自动内嵌）、导语、三线表（圆角表头 + 隔行换色）、引用块、金句荧光笔、图片位与图注、风险提示、话题胶囊标签、往期精选、账号名片位。九套配色：墨绿（默认）/ 石墨绿 / 竹青 / 藏蓝 / 湖蓝 / 紫藤 / 橄榄 / 绛红 / 赭石。

## 安装

直接拷贝下面这句话发给你的 AI 助手：

> 安装 https://gitee.com/lennyash/insightyouth-skill

Agent 会自动克隆仓库并安装到对应的 Skill 目录（`~/.workbuddy/skills/InsightYouth-style/`）。安装完成后**新开一个会话**即可生效。

## 使用

把文章发给 AI 助手（直接贴正文，或给 `.md` / `.txt` 文件路径），说「套用有悟青年浅绿排版」。排版过程中**原文一字不改**，只补结构标记；生成 HTML 后点「一键复制全文」→ 粘贴进公众号编辑器。

完整可运行的示例文章见 [`references/sample-article.md`](references/sample-article.md)。

## 文件结构

```
InsightYouth-style/
├── SKILL.md                    # 技能说明（AI 读这一份就知道怎么干活）
├── assets/
│   ├── template.html           # 排版模板（含内嵌动图、配色切换、复制脚本）
│   └── follow-guide.gif        # 关注引导动图原图
├── scripts/
│   └── build.py                # Markdown → 公众号 HTML（仅标准库，python3 即跑）
└── references/
    ├── style-spec.md           # 完整样式规范：色值、字号、模块骨架
    ├── wechat-compat.md        # 公众号兼容性踩坑记录
    └── sample-article.md       # 覆盖全部模块的示例文章
```

## 运行环境

支持 Windows、macOS 和 Linux。`build.py` 只依赖 Python 标准库，任意 python3 均可运行，无需安装任何第三方包。

## 版本

当前版本见 [`skill.json`](skill.json)。
