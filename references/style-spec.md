# 样式规范（公众号财经模板 · 墨绿默认）

所有样式必须内联。容器一律用 `<section>`（公众号不认 `<div>` 的块级语义时更稳）。

## 色彩系统

默认配色「墨绿」。下列常量定义在 `scripts/build.py`，**必须与 `assets/template.html` 里 `THEMES[0]` 逐值一致**——否则成品内联色与页面上的「配色」按钮对不上，切换会失效。

| 变量 | 值 | 用途 | 随配色切换 |
|---|---|---|---|
| 主色 ACCENT | `#17705a` | 出处小字、表头文字、列表序号、导语左线、胶囊字、风险提示标题 | 是 |
| 主色加深 DEEP | `#0f5443` | 区块标题气泡字、按钮 hover（仅页面外壳用） | 是 |
| 点缀 TINT | `#dff2e9` | 引用块左线、话题胶囊底、区块标题气泡底、行内高亮底 | 是 |
| 表头/行线 HEAD_BG | `#ecf3ef` | 表头底、表格行线 | 是 |
| 隔行底 ROW_BG | `#f6faf8` | 表格第 2、4、6… 行 | 是 |
| 提示块底 SOFT_BG | `#f5faf7` | 往期精选 | 是 |
| 风险提示底 RISK_BG | `#e9f4ee` | 风险提示块（比往期精选深一档） | 是 |
| 标题色 TITLE | `#12372e` | 一、二、三级标题（`h1` / `h2` / `h3`） | 是 |
| 细线 LINE | `#d9e3df` | 小标题下方细线的实色端 | 是 |
| 渐隐 FADE | `rgba(217,227,223,0)` | 小标题细线的右端 | 是 |
| 荧光笔 MARK | `#a9ddc6` | 金句的高亮笔迹（比 TINT 深一档才看得出） | 是 |
| 近黑 INK | `#101418` | 金句、表格首列文字 | **否** |
| 正文 BODY | `#333333` | 正文段落 | 否 |
| 次级 MUTED | `#555555` | 表格数据、引用引文、往期精选条目 | 否 |
| 表格名 NOTE | `#999999` | 「表 1｜…」表格名 | 否 |
| 占位标记 SLOT | `#b3b9c2` | 图片位 / 名片位的灰字 | 否 |
| 图注 / 表注 CAPTION | `#aaaaaa` | 「图为…」「注：…」同一档 | 否 |
| 导语灰 | `#666666` | 导语文字 | 否 |

### 页面上的九套配色

模板顶栏右侧九个圆点即配色方案，**默认墨绿**。切换是整套替换：上表标注「是」的角色色全部跟随，页面外壳（顶栏描边、品牌字、选中圆点的描边、「一键复制」按钮、提示条、画布底色）也通过 CSS 变量 `:root` 同步；正文 `#333` / `#555` / `#101418` 刻意保持不变，避免正文发色伤可读性。

| 冷暖 | 方案 | 主色 | 标题色 | 浅底（胶囊） | 荧光笔 |
|---|---|---|---|---|---|
| 冷 | **墨绿（默认）** | `#17705a` | `#12372e` | `#dff2e9` | `#a9ddc6` |
| 冷 | 石墨绿 | `#47584e` | `#2b3630` | `#e5ece8` | `#c9d6cf` |
| 冷 | 竹青 | `#3a8f72` | `#1d4a3d` | `#d7efe4` | `#b0ddca` |
| 冷 | 藏蓝 | `#2a5b8f` | `#1c3b5e` | `#dde9f5` | `#b3d3f0` |
| 冷 | 湖蓝 | `#2e7f8c` | `#1e4a52` | `#d9eef1` | `#b2e0e8` |
| 冷 | 紫藤 | `#6a4c93` | `#372a52` | `#e9e2f3` | `#d3c6ec` |
| 暖 | 橄榄 | `#6b7f3a` | `#3f4a24` | `#eaf0d8` | `#dfe6b4` |
| 暖 | 绛红 | `#a34a52` | `#5c2028` | `#f7e3e5` | `#f2c3c8` |
| 暖 | 赭石 | `#9c6a2f` | `#553714` | `#f6ead6` | `#f0d9a8` |

每套 12 个色：accent / deep / tint / head / row / risk / soft / title / line / fade / paper / mark，定义在 `template.html` 的 `THEMES` 数组里。切换函数 `recolor()` 同时兼容 `#rrggbb` 与 `rgb()` 写法（云端平台常把 hex 改写为 rgb，且空格不统一）。

## 排版基线

- 正文：16px / 行高 1.85 / 段距 24px / `text-align:justify;text-justify:inter-ideograph;`
- 大标题：26px / 700 / 行高 1.42（**正文默认不出现**，公众号标题栏已承担；需要时用 `!标题` 显式插入）
- 小标题 h2：20px / 700 / 行高 1.4 / **标题色 `TITLE`（不是纯黑，会随配色变）**，下方自带一条 1px 渐隐细线（`linear-gradient(90deg,#d9e3df,rgba(217,227,223,0))`，与标题间距 12px、与正文间距 20px）
- 三级标题 h3：17px / 700
- 正文宽度按 677px 设计
- **正文第一块固定是关注引导动图**，它上面不放任何内容
- **列表引出句收紧**：以冒号结尾的段落后面直接跟列表时，段落底距与列表顶距自动收为 8px

## 模块骨架（可直接复制）

**导语**
```html
<section style="border-left:2px solid #17705a;padding-left:14px;margin:0 0 30px;">
  <section><p style="margin:0;font-size:15.5px;line-height:1.85;color:#666666;text-align:justify;text-justify:inter-ideograph;">…</p></section>
</section>
```

**正文段落**
```html
<section style="margin:0 0 24px;">
  <p style="margin:0;font-size:16px;line-height:1.85;color:#333333;text-align:justify;text-justify:inter-ideograph;">…</p>
</section>
```

**小标题 + 细线**（一体输出）
```html
<h2 style="margin:28px 0 12px;font-size:20px;font-weight:700;color:#12372e;line-height:1.4;">一、标题文字</h2>

<section style="height:1px;background:linear-gradient(90deg,#d9e3df,rgba(217,227,223,0));margin:0 0 20px;"></section>
```

**圆点列表**
```html
<section style="margin:8px 0 22px;padding-left:24px;">
  <section style="margin:6px 0;display:flex;align-items:flex-start;gap:6px;font-size:16px;">
    <span style="color:#17705a;font-size:15px;line-height:1.8;flex-shrink:0;transform:scale(0.6);">●</span>
    <span style="word-break:break-word;min-width:0;">…</span>
  </section>
</section>
```

**数字列表**（序号主色加粗、min-width 定宽对齐）
```html
<section style="margin:8px 0 22px;padding-left:24px;">
  <section style="margin:6px 0;display:flex;align-items:flex-start;gap:8px;font-size:16px;">
    <span style="color:#17705a;font-weight:700;font-size:15.5px;line-height:1.85;flex-shrink:0;min-width:20px;">1.</span>
    <span style="word-break:break-word;min-width:0;">…</span>
  </section>
</section>
```

**引用块**（引述他人观点 / 研报原文；大引号用黑体加粗）
```html
<section style="margin:28px 0;border-left:3px solid #dff2e9;padding:2px 0 2px 16px;">
  <p style="margin:0 0 6px;font-size:30px;line-height:0.9;font-weight:700;color:#17705a;font-family:'SimHei','Microsoft YaHei',sans-serif;">&ldquo;</p>
  <p style="margin:0 0 10px;font-size:15.5px;line-height:1.9;color:#555555;text-align:justify;text-justify:inter-ideograph;">引文</p>
  <p style="margin:0;font-size:13px;line-height:1.6;color:#17705a;letter-spacing:.5px;">—— 机构名《报告名》，年月</p>
</section>
```

**金句块**（自己的观点，居中，带「荧光笔」高亮）

每行必须各包一个 `span`——行内元素跨 `<br>` 时渐变基准会错乱，第二行的笔迹会飘。行高放到 2，让两行笔迹之间有呼吸。

```html
<section style="text-align:center;margin:32px 0;">
  <p style="margin:0 0 14px;font-size:17.5px;line-height:2;color:#101418;"><span style="font-weight:700;background:linear-gradient(transparent 62%,#a9ddc6 62%);padding:1px 4px;">第一行</span><br><span style="font-weight:700;background:linear-gradient(transparent 62%,#a9ddc6 62%);padding:1px 4px;">第二行</span></p>
  <p style="margin:0;font-size:13px;line-height:1.6;color:#17705a;letter-spacing:1px;">—— 署名</p>
</section>
```

**表格**（重要：**必须用 section + flex，不要用 table 标签**——公众号编辑器粘贴时会重写 table 结构，圆角和隔行色会变形；每个单元格务必带 `box-sizing:border-box`，列宽按列数均分）
```html
<section style="margin:0 0 10px;font-size:14px;line-height:1.7;">
  <section style="display:flex;background:#ecf3ef;border-radius:8px 8px 0 0;">
    <section style="box-sizing:border-box;width:33.33%;padding:12px 10px;color:#17705a;font-size:14px;font-weight:600;letter-spacing:.5px;">列1</section>
    <section style="box-sizing:border-box;width:33.33%;padding:12px 10px;color:#17705a;font-size:14px;font-weight:600;letter-spacing:.5px;">列2</section>
  </section>
  <section style="display:flex;">
    <section style="box-sizing:border-box;width:33.33%;padding:13px 10px;border-bottom:1px solid #ecf3ef;color:#101418;">…</section>
    <section style="box-sizing:border-box;width:33.33%;padding:13px 10px;border-bottom:1px solid #ecf3ef;color:#555555;">…</section>
  </section>
  <section style="display:flex;background:#f6faf8;">
    <section style="box-sizing:border-box;width:33.33%;padding:13px 10px;border-bottom:1px solid #ecf3ef;color:#101418;">…</section>
    <section style="box-sizing:border-box;width:33.33%;padding:13px 10px;border-bottom:1px solid #ecf3ef;color:#555555;">…</section>
  </section>
</section>
```
要点：表头不比正文大（同为 14px，仅靠底色 + 主色 + 半粗区分）；正文单元格一律不加粗；末行也要有 border-bottom 收口；隔行底色写在行容器上。

**表格名**（表格上方一行「表 1｜…」，15px / `#999999`，比表注大一号；表格多时按 表 1、表 2 依次编号）
```html
<p style="margin:26px 0 8px;font-size:15px;line-height:1.6;color:#999999;">表 1｜本轮与上一轮周期对比</p>
```

**表注 / 数据来源**
```html
<p style="margin:0 0 6px;font-size:12.5px;line-height:1.6;color:#aaaaaa;">注：…</p>
<p style="margin:0 0 24px;font-size:13px;line-height:14px;color:#17705a;letter-spacing:1px;">数据来源：…</p>
```

**图片占位**（无外框，居中灰字标记 + 紧随其后的图注；上传时删掉标记那行、原位插图，图注可留当图片说明）

图注与表注同一档（12.5px / `#aaaaaa`），`margin-top` 只给 2px，让它贴着图片走。

```html
<section style="margin:30px 0;text-align:center;">
  <p style="margin:0;font-size:13px;line-height:1.8;color:#b3b9c2;">【图片位】</p>
  <p style="margin:2px 0 0;font-size:12.5px;line-height:1.6;color:#aaaaaa;">图为 XX</p>
</section>
```

**渐变分隔线**
```html
<section style="border:none;height:1px;background:linear-gradient(90deg,rgba(255,255,255,0),#dddddd,rgba(255,255,255,0));margin:24px 0;"></section>
```

**风险提示**（比往期精选醒目一档：底色深、左线 4px、标题用主色；标题前带一个 ⚠ 符号，符号与四个字同属一个 `strong`）

```html
<section style="margin:14px 0;padding:12px 16px;background:#e9f4ee;border-left:4px solid #17705a;border-radius:0 8px 8px 0;color:#444444;font-size:14px;">
  <p style="margin:4px 0;line-height:1.8;text-align:justify;text-justify:inter-ideograph;"><strong style="font-weight:700;color:#17705a;">⚠ 风险提示</strong>：…</p>
</section>
```
默认文案：「基于公开信息梳理，仅用于个人研究，不构成任何投资建议。」

**话题标签**（圆角胶囊：一个标签一个 `inline-block` span，淡绿底 + 主色字 + `999px` 圆角；标签之间不留空白字符，间距靠 `margin-right`）
```html
<p style="margin:18px 0 0;"><span style="display:inline-block;padding:3px 12px;margin:0 8px 8px 0;background:#dff2e9;border-radius:999px;color:#17705a;font-size:13px;line-height:1.6;letter-spacing:.5px;">#标签一</span><span style="display:inline-block;padding:3px 12px;margin:0 8px 8px 0;background:#dff2e9;border-radius:999px;color:#17705a;font-size:13px;line-height:1.6;letter-spacing:.5px;">#标签二</span></p>
```

**往期精选**（条目是纯文字行，无圆点；标题做成一个气泡：15.5px 胶囊，tint 底 + deep 字，左下收到 2px 当小尾巴，与容器的 8px 圆角同源）

```html
<section style="margin:14px 0;padding:14px 16px;background:#f5faf7;border-radius:8px;">
  <p style="margin:0 0 10px;"><span style="display:inline-block;padding:3px 12px;background:#dff2e9;border-radius:8px 8px 8px 2px;color:#0f5443;font-size:15.5px;line-height:1.6;font-weight:700;letter-spacing:.5px;">✿ 往期精选</span></p>
  <section style="margin:6px 0;font-size:14px;line-height:1.7;color:#555555;">标题一</section>
  <section style="margin:6px 0;font-size:14px;line-height:1.7;color:#555555;">标题二</section>
</section>
```

**账号名片位**（全文最末一块，与【图片位】同一套占位写法；复制到公众号后删掉这行字、就地插入账号名片）
```html
<section style="margin:18px 0 0;text-align:center;">
  <p style="margin:0;font-size:13px;line-height:1.8;color:#b3b9c2;">【账号名片位】</p>
</section>
```

**行内高亮**（可选）：`<span style="background-color:#dff2e9;padding:0 3px;">文字</span>`

## 正文模块顺序

关注引导动图 → 图片位（头图，含图注）→ 导语 → 正文（小标题 / 段落 / 列表 / 表格 / 引用） → 金句 → 图片位（含图注）→ 分隔线 → 风险提示 → 话题标签 → 分隔线 → 往期精选 → 账号名片位（全文结束，其后不再放落款）

**正文第一块固定是关注引导动图，上面不放任何内容**；文章大标题由公众号标题栏承担，正文里不重复。原 Markdown 的 `# 标题` 只用于页面 `<title>`，不会进入正文。

## 关注引导动图

- 位图，配色写死在图里：主色字 `#17705a` + 淡色药丸 `#dff2e9` + 中调三角 `#6d7f74`
- **画布即药丸（336×56 @2x），四周无白边**；模板里以 `width:168px` 固定宽显示（**不要用 width:100%，会撑满整行显得过大**）
- 容器 `margin:0 0 8px`——上下间隙已收至最小（上 0 / 下 8px）
- 左对齐（外层 `text-align:left`）
- 文案固定为「点击上方关注我们」，常规字重 16px（显示尺寸，与正文一致），三角在文字左侧

## 改配色 / 改默认配色时的联动清单

1. `scripts/build.py` 顶部的常量（ACCENT / DEEP / TINT / HEAD_BG / ROW_BG / SOFT_BG / RISK_BG / TITLE / LINE / FADE / MARK）
2. `assets/template.html` 的 `THEMES` 数组——**`THEMES[0]` 是默认配色，必须与第 1 项逐值相同**，否则页面上的配色按钮对成品不生效；改默认色时把目标方案那一行挪到第一位
3. `assets/template.html` 里 `THEMES[0]` 之外写死的内联色（正文示例、hint 文案、`CSS :root` 的五个变量）：换默认色时，要连同所有 `<script>` 块之外出现的旧值一起替换（`<script>` 里的 THEMES 数组不动，避免自己替换自己）
4. 本文档「色彩系统」表与所有模块骨架里的示例色值
5. **关注引导动图 GIF**（位图，配色写死在像素里，不随配色切换；它画的是墨绿 `#17705a`，与当前默认配色一致。若把默认配色改到墨绿以外的方案，需重新生成 GIF 并替换 `assets/follow-guide.gif` 与模板里的 base64）
6. 表头/隔行等底色换成新色后是否仍协调

顺序建议：先改 `build.py` 常量与 `template.html` 的 `THEMES[0]` → 用同一份脚本跑一遍成品核对（确认正文里没有旧方案残留）→ 再改文档。
