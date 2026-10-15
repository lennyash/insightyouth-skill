#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把一篇 Markdown 文章套进「公众号财经排版模板」，输出带一键复制功能的 HTML。

用法:
    python build.py article.md
    python build.py article.md -o "D:/某目录/成品.html"
    python build.py article.md --no-follow-gif     # 不插入关注引导动图

只依赖 Python 标准库。模板读取 <skill>/assets/template.html（含内嵌 GIF 与复制脚本），
只替换 <!--DOC:START--> 与 <!--DOC:END--> 之间的正文，工具栏/样式/JS 原样保留。

正文固定以「关注引导动图」开篇，它上面不放任何内容；Markdown 的 `# 一级标题` 只用来命名
页面 <title>，不进正文（文章大标题由公众号标题栏承担）。需要正文里另起大标题时用 `!标题 xxx`。
"""

import argparse
import html as _html
import io
import os
import re
import sys

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_TPL = os.path.join(SKILL_DIR, "assets", "template.html")

# ---------- 设计常量（须与 assets/template.html 的 THEMES[0] 逐值一致）----------
# 当前默认配色「墨绿」。改这里必须同步改模板 THEMES[0]，否则成品里的内联色与模板 SCHEME
# 对不上，页面上的「配色」按钮会失效（切换逻辑是从 THEMES[0] 出发做整体替换的）。
ACCENT = "#17705a"            # 主色（墨绿）
DEEP = "#0f5443"              # 主色加深（区块标题字、按钮按下态）
TINT = "#dff2e9"              # 点缀浅色（引用左线、话题胶囊底、区块标题气泡底）
HEAD_BG = "#ecf3ef"           # 表头底 / 表格行线
ROW_BG = "#f6faf8"            # 表格隔行底
SOFT_BG = "#f5faf7"           # 往期精选块底
RISK_BG = "#e9f4ee"           # 风险提示块底（比 SOFT_BG 深一档）
TITLE = "#12372e"             # 一二级标题色——随配色切换
LINE = "#d9e3df"              # 小标题下方细线——随配色切换
FADE = "rgba(217,227,223,0)"  # 细线右端渐隐
MARK = "#a9ddc6"              # 金句荧光笔高亮——随配色切换
INK = "#101418"               # 近黑（表格首列 / 金句）——刻意不参与配色切换
BODY = "#333333"              # 正文
MUTED = "#555555"             # 次级文字
NOTE = "#999999"              # 表格名「表 1｜…」
SLOT = "#b3b9c2"              # 占位标记字（图片位 / 名片位）
CAPTION = "#aaaaaa"           # 图注 / 表注

JUSTIFY = "text-align:justify;text-justify:inter-ideograph;"

# ---------- 行内标记 ----------


def inline(text):
    """转义 + 支持 **粗** / *斜* / ==高亮== / `代码`"""
    s = _html.escape(text, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r'<strong style="font-weight:700;">\1</strong>', s)
    s = re.sub(r"==(.+?)==", r'<span style="background-color:%s;padding:0 3px;">\1</span>' % TINT, s)
    s = re.sub(r"`(.+?)`", r'<code style="background:#f2f5f3;padding:1px 4px;border-radius:3px;font-size:15px;">\1</code>', s)
    s = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", s)
    return s


def para(text):
    return ('      <section style="margin:0 0 24px;">\n'
            '        <p style="margin:0;font-size:16px;line-height:1.85;color:%s;%s">%s</p>\n'
            '      </section>' % (BODY, JUSTIFY, inline(text)))


# ---------- 块级 ----------

def h1(text):
    """正文大标题。仅由 !标题 显式调用——Markdown 的 # 标题默认不进正文。"""
    return ('      <p style="margin:0 0 12px;font-size:26px;line-height:1.42;font-weight:700;color:%s;">%s</p>'
            % (TITLE, inline(text)))


def h2(text):
    """小标题 + 下方 1px 渐隐细线（左实右淡），两者一体输出。"""
    return ('      <h2 style="margin:28px 0 12px;font-size:20px;font-weight:700;color:%s;line-height:1.4;">%s</h2>\n\n'
            '      <section style="height:1px;background:linear-gradient(90deg,%s,%s);margin:0 0 20px;"></section>'
            % (TITLE, inline(text), LINE, FADE))


def h3(text):
    return ('      <h3 style="margin:24px 0 10px;font-size:17px;font-weight:700;color:%s;line-height:1.5;">%s</h3>'
            % (TITLE, inline(text)))


def lead(text):
    return ('      <section style="border-left:2px solid %s;padding-left:14px;margin:0 0 30px;">\n'
            '        <section><p style="margin:0;font-size:15.5px;line-height:1.85;color:#666666;%s">%s</p></section>\n'
            '      </section>' % (ACCENT, JUSTIFY, inline(text)))


def bullet_list(items):
    rows = []
    for it in items:
        rows.append(
            '        <section style="margin:6px 0;display:flex;align-items:flex-start;gap:6px;font-size:16px;">\n'
            '          <span style="color:%s;font-size:15px;line-height:1.8;flex-shrink:0;transform:scale(0.6);">●</span>\n'
            '          <span style="word-break:break-word;min-width:0;">%s</span>\n'
            '        </section>' % (ACCENT, inline(it)))
    return ('      <section style="margin:8px 0 22px;padding-left:24px;">\n' + "\n".join(rows) + '\n      </section>')


def ordered_list(items):
    """数字列表：主色加粗序号，min-width 定宽对齐。

    items 元素可以是字符串（按位置编号）或 (num, text) 对（用原文序号）——
    原文里有图片/空行把列表切断时，Typecho 会渲染成多个 <ol start="n">，
    此时必须沿用作者写的数字，不能各自从 1 重来。
    """
    rows = []
    for i, it in enumerate(items, 1):
        num, text = (it if isinstance(it, tuple) else (i, it))
        rows.append(
            '        <section style="margin:6px 0;display:flex;align-items:flex-start;gap:8px;font-size:16px;">\n'
            '          <span style="color:%s;font-weight:700;font-size:15.5px;line-height:1.85;flex-shrink:0;min-width:20px;">%s.</span>\n'
            '          <span style="word-break:break-word;min-width:0;">%s</span>\n'
            '        </section>' % (ACCENT, num, inline(text)))
    return ('      <section style="margin:8px 0 22px;padding-left:24px;">\n' + "\n".join(rows) + '\n      </section>')


def quote(text, source=""):
    src = ('\n        <p style="margin:0;font-size:13px;line-height:1.6;color:%s;letter-spacing:.5px;">—— %s</p>'
           % (ACCENT, inline(source))) if source else ""
    return ('      <section style="margin:28px 0;border-left:3px solid %s;padding:2px 0 2px 16px;">\n'
            '        <p style="margin:0 0 6px;font-size:30px;line-height:0.9;font-weight:700;color:%s;font-family:\'SimHei\',\'Microsoft YaHei\',sans-serif;">&ldquo;</p>\n'
            '        <p style="margin:0 0 10px;font-size:15.5px;line-height:1.9;color:%s;%s">%s</p>\n'
            '        <p style="margin:0 0 6px;font-size:30px;line-height:0.9;font-weight:700;color:%s;text-align:right;font-family:\'SimHei\',\'Microsoft YaHei\',sans-serif;">&rdquo;</p>%s\n'
            '      </section>' % (TINT, ACCENT, MUTED, JUSTIFY, inline(text), ACCENT, src))


def pull_quote(text, source=""):
    """金句：居中、加粗，每行一道「荧光笔」渐变高亮（linear-gradient 画的下半截色块）。

    必须按行拆开各包一个 span——行内元素跨 <br> 时渐变基准会错乱，第二行的笔迹会飘。
    行高放到 2，让两行笔迹之间有呼吸。
    """
    src = ('\n        <p style="margin:0;font-size:13px;line-height:1.6;color:%s;letter-spacing:1px;">—— %s</p>'
           % (ACCENT, inline(source))) if source else ""
    lines = [ln for ln in re.split(r"\n|<br\s*/?>", inline(text).strip()) if ln.strip()]
    marked = "<br>".join(
        f'<span style="font-weight:700;background:linear-gradient(transparent 62%,{MARK} 62%);padding:1px 4px;">{ln}</span>'
        for ln in lines)
    return ('      <section style="text-align:center;margin:32px 0;">\n'
            '        <p style="margin:0 0 14px;font-size:17.5px;line-height:2;color:%s;">%s</p>%s\n'
            '      </section>' % (INK, marked, src))


def risk(text):
    return ('      <section style="margin:14px 0;padding:12px 16px;background:%s;border-left:4px solid %s;border-radius:0 8px 8px 0;color:#444444;font-size:14px;">\n'
            '        <p style="margin:4px 0;line-height:1.8;%s"><strong style="font-weight:700;color:%s;">⚠ 风险提示</strong>：%s</p>\n'
            '      </section>' % (RISK_BG, ACCENT, JUSTIFY, ACCENT, inline(text)))


def caption(text):
    """表格名（表 1｜…）：比表注大一号，视觉上属于表格的一部分。"""
    return ('      <p style="margin:26px 0 8px;font-size:15px;line-height:1.6;color:%s;">%s</p>' % (NOTE, inline(text)))


def small_note(text):
    """表注 / 口径说明：紧跟表格之后，比表格名更小更淡。图注用同一档字号。"""
    return ('      <p style="margin:0 0 6px;font-size:12.5px;line-height:1.6;color:%s;">%s</p>' % (CAPTION, inline(text)))


def source_line(text):
    return ('      <p style="margin:0 0 24px;font-size:13px;line-height:14px;color:%s;letter-spacing:1px;">%s</p>'
            % (ACCENT, inline(text)))


def image_slot(text=""):
    """图片占位：居中的灰字标记 + 紧随其后的图注行（与表注同级，间距 2px 贴着图片走）。

    `!图 营收走势` → 图注「营收走势」；不写参数时显示占位「图注 XX」。
    换成真实图片后上传到公众号、把这两行字删掉即可，图注那行可留着当图片说明。
    """
    t = text.strip()
    cap = t if t else "图注 XX"
    return ('      <section style="margin:30px 0;text-align:center;">\n'
            '        <p style="margin:0;font-size:13px;line-height:1.8;color:%s;">【图片位】</p>\n'
            '        <p style="margin:2px 0 0;font-size:12.5px;line-height:1.6;color:%s;">%s</p>\n'
            '      </section>' % (SLOT, CAPTION, inline(cap)))


def card_slot(text=""):
    """文末账号名片位：与「【图片位】」同一套占位写法，复制到公众号后删字换名片。"""
    t = text.strip()
    label = "【%s】" % t if t else "【账号名片位】"
    return ('      <section style="margin:18px 0 0;text-align:center;">\n'
            '        <p style="margin:0;font-size:13px;line-height:1.8;color:%s;">%s</p>\n'
            '      </section>' % (SLOT, inline(label)))


def divider():
    return ('      <section style="border:none;height:1px;background:linear-gradient(90deg,rgba(255,255,255,0),#dddddd,rgba(255,255,255,0));margin:24px 0;"></section>')


def tags(items):
    """话题标签：淡绿底圆角胶囊（inline-block + 999px 圆角）。"""
    if isinstance(items, str):
        items = re.split(r"[\s,，、]+", items.strip())
    parts = []
    for t in items:
        t = t.strip()
        if not t:
            continue
        parts.append(t if t.startswith("#") else "#" + t)
    if not parts:
        return ""
    pills = "".join(
        '<span style="display:inline-block;padding:3px 12px;margin:0 8px 8px 0;'
        'background:%s;border-radius:999px;color:%s;font-size:13px;line-height:1.6;'
        'letter-spacing:.5px;">%s</span>'
        % (TINT, ACCENT, _html.escape(p, quote=False))
        for p in parts)
    return '      <p style="margin:18px 0 0;">%s</p>' % pills


def past_picks(items):
    if isinstance(items, str):
        items = [x for x in re.split(r"[|｜]", items) if x.strip()]
    rows = []
    for it in items:
        rows.append(
            '        <section style="margin:6px 0;font-size:14px;line-height:1.7;color:%s;">%s</section>'
            % (MUTED, inline(it.strip())))
    return ('      <section style="margin:14px 0;padding:14px 16px;background:%s;border-radius:8px;">\n'
            '        <p style="margin:0 0 10px;"><span style="display:inline-block;padding:3px 12px;'
            'background:%s;border-radius:8px 8px 8px 2px;color:%s;font-size:15.5px;line-height:1.6;'
            'font-weight:700;letter-spacing:.5px;">✿ 往期精选</span></p>\n%s\n'
            '      </section>' % (SOFT_BG, TINT, DEEP, "\n".join(rows)))


def table(rows):
    """rows: 第一行是表头，其余是数据行。

    必须用 section + flex 实现，不要用 <table>——公众号编辑器粘贴时会重写 table 结构，
    圆角和隔行底色会变形。列宽按列数均分，单元格一律 box-sizing:border-box。
    """
    if not rows:
        return ""
    head = rows[0]
    body = rows[1:]
    ncol = max(len(r) for r in rows)
    head = head + [""] * (ncol - len(head))
    w = "%.2f%%" % (100.0 / ncol)

    head_cells = []
    for c in head:
        head_cells.append(
            '          <section style="box-sizing:border-box;width:%s;padding:12px 10px;color:%s;font-size:14px;font-weight:600;letter-spacing:.5px;">%s</section>'
            % (w, ACCENT, inline(c)))

    trs = []
    for ri, r in enumerate(body):
        r = r + [""] * (ncol - len(r))
        bg = "background:%s;" % ROW_BG if ri % 2 == 1 else ""
        cells = []
        for ci, c in enumerate(r):
            color = INK if ci == 0 else MUTED
            cells.append(
                '          <section style="box-sizing:border-box;width:%s;padding:13px 10px;border-bottom:1px solid %s;color:%s;">%s</section>'
                % (w, HEAD_BG, color, inline(c)))
        trs.append('        <section style="display:flex;%s">\n%s\n        </section>'
                   % (bg, "\n".join(cells)))

    return ('      <section style="margin:0 0 10px;font-size:14px;line-height:1.7;">\n'
            '        <section style="display:flex;background:%s;border-radius:8px 8px 0 0;">\n%s\n        </section>\n'
            '%s\n      </section>'
            % (HEAD_BG, "\n".join(head_cells), "\n".join(trs)))


# ---------- 解析 ----------

DIRECTIVES = {
    "导语": lambda a: lead(a),
    "引用": lambda a: quote(*_split_pair(a)),
    "金句": lambda a: pull_quote(*_split_pair(a)),
    "风险": lambda a: risk(a),
    "小字": lambda a: small_note(a),
    "表名": lambda a: caption(a),
    "来源": lambda a: source_line(a),
    "标签": lambda a: tags(a),
    "往期": lambda a: past_picks(a),
    "图": lambda a: image_slot(a),
    "名片": lambda a: card_slot(a),
    "名片位": lambda a: card_slot(a),
    "分隔": lambda a: divider(),
    "标题": lambda a: h1(a),
}


def _split_pair(a):
    """把 '内容 | 出处' 拆成两段；没有竖线则只有内容。"""
    parts = re.split(r"\s*[|｜]\s*", a.strip(), maxsplit=1)
    if len(parts) == 2:
        return parts[0], parts[1]
    return parts[0], ""


def _is_table_row(line):
    return line.strip().startswith("|") and line.strip().endswith("|")


def _cells(line):
    s = line.strip().strip("|")
    return [c.strip() for c in re.split(r"(?<!\\)\|", s)]


def _is_sep_row(line):
    return bool(re.fullmatch(r"[\s|:\-]+", line.strip())) and "-" in line


def parse(md, titles=None):
    """把 Markdown 转成模板风格的 HTML 块列表。

    `# 一级标题` 不进正文（正文顶部留给关注引导动图，文章大标题由公众号标题栏承担），
    仅收集到 titles 里用于写入页面 <title>。需要正文里另起大标题时用 `!标题 xxx`。
    """
    lines = md.replace("\r\n", "\n").split("\n")
    out = []
    i = 0
    n = len(lines)
    while i < n:
        raw = lines[i]
        line = raw.strip()

        # 空行
        if not line:
            i += 1
            continue

        # 指令行
        m = re.match(r"^!\s*([^\s!]+)\s*(.*)$", line)
        if m and m.group(1) in DIRECTIVES:
            name, arg = m.group(1), m.group(2)
            out.append(DIRECTIVES[name](arg))
            i += 1
            continue

        # 标题
        if re.match(r"^#\s+", line):
            if titles is not None:
                titles.append(re.sub(r"^#\s+", "", line))
            i += 1
            continue
        if re.match(r"^##\s+", line):
            out.append(h2(re.sub(r"^##\s+", "", line)))
            i += 1
            continue
        if re.match(r"^###\s+", line):
            out.append(h3(re.sub(r"^###\s+", "", line)))
            i += 1
            continue

        # 话题标签行：#算力 #数据中心（整行只由 #标签 组成，允许空格分隔）
        if re.fullmatch(r"(#[^\s#]+[\s　]*)+", line):
            out.append(tags(line))
            i += 1
            continue

        # 分隔线
        if re.fullmatch(r"(-{3,}|\*{3,}|_{3,})", line):
            out.append(divider())
            i += 1
            continue

        # 引用块
        if line.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(re.sub(r"^>\s?", "", lines[i].strip()))
                i += 1
            src = ""
            if buf and re.match(r"^[—–-]{1,2}\s*", buf[-1]):
                src = re.sub(r"^[—–-]{1,2}\s*", "", buf.pop())
            out.append(quote("\n".join(buf), src))
            continue

        # 表格
        if _is_table_row(line):
            rows = []
            while i < n and _is_table_row(lines[i]):
                if not _is_sep_row(lines[i]):
                    rows.append(_cells(lines[i]))
                i += 1
            out.append(table_with_caption(rows, lines, i))
            continue

        # 无序列表
        if re.match(r"^[-*+]\s+", line):
            items = []
            while i < n and re.match(r"^[-*+]\s+", lines[i].strip()):
                items.append(re.sub(r"^[-*+]\s+", "", lines[i].strip()))
                i += 1
            _tighten_lead(out)
            out.append(bullet_list(items))
            continue

        # 有序列表（保留原文序号，兼容被空行/图片切成多段的情形）
        if re.match(r"^\d+[.)]\s+", line):
            items = []
            while i < n and re.match(r"^\d+[.)]\s+", lines[i].strip()):
                m_ol = re.match(r"^(\d+)[.)]\s+([\s\S]*)$", lines[i].strip())
                items.append((m_ol.group(1), m_ol.group(2)))
                i += 1
            _tighten_lead(out)
            out.append(ordered_list(items))
            continue

        # 图片
        m = re.match(r"^!\[([^\]]*)\]\([^)]*\)$", line)
        if m:
            out.append(image_slot(m.group(1)))
            i += 1
            continue

        # 风险提示 / 免责声明（自动识别）
        if re.match(r"^(风险提示|免责声明|声明)[：:]", line):
            out.append(risk(re.sub(r"^(风险提示|免责声明|声明)[：:]\s*", "", line)))
            i += 1
            continue

        # 普通段落（连续行并成一段）
        buf = [line]
        i += 1
        while i < n:
            nxt = lines[i].strip()
            if (not nxt or re.match(r"^(!\w|[#>]|\d+[.)]\s|[-*+]\s|###?\s)", nxt)
                    or _is_table_row(nxt) or re.fullmatch(r"(-{3,}|\*{3,}|_{3,})", nxt)):
                break
            buf.append(nxt)
            i += 1
        out.append(para(" ".join(buf)))

    return "\n\n".join(x for x in out if x)


def table_with_caption(rows, lines, idx):
    """表格 + 可选的表注/来源（表格后紧跟的 !小字 / !来源）。"""
    return table(rows)


# ---------- 组装 ----------


def extract_follow_gif(tpl):
    """从模板里抓出「关注引导动图」那一段，保持 base64 与模板同步。

    模板可能带有平台（资料库在线 page）注入的标记属性，所以这里按 style 关键片段
    宽松匹配 section 开标签，并把多余属性统一去掉，避免图块整体失配丢失。
    """
    m = re.search(r'<section[^>]*style="text-align:left;margin:0 0 8px;"[^>]*>[\s\S]*?</section>', tpl)
    if not m:
        return ""
    block = re.sub(r"<section[^>]*>",
                   '<section style="text-align:left;margin:0 0 8px;">',
                   m.group(0), count=1)
    lines = [ln.strip() for ln in block.split("\n") if ln.strip()]
    out = []
    for idx, ln in enumerate(lines):
        out.append(("        " if 0 < idx < len(lines) - 1 else "      ") + ln)
    return "\n".join(out)


def _tighten_lead(out):
    """列表紧跟在引出句（以冒号结尾的段落）后时，把两侧间距收紧。"""
    if out and out[-1].startswith('      <section style="margin:0 0 24px;">'):
        out[-1] = out[-1].replace('margin:0 0 24px;', 'margin:0 0 8px;', 1)


def render(md, tpl, follow_gif=True):
    titles = []
    content = parse(md, titles)
    if titles:
        # 一级标题只用来命名页面，不进入正文
        tpl = re.sub(r"<title>[\s\S]*?</title>",
                     "<title>%s</title>" % _html.escape(titles[0], quote=False), tpl, count=1)
    gif_block = extract_follow_gif(tpl) if follow_gif else ""
    if gif_block:
        # 关注引导动图固定为正文第一块，它上面不放任何内容
        content = gif_block + ("\n\n" + content if content.strip() else "")

    start_tag = "<!--DOC:START-->"
    end_tag = "<!--DOC:END-->"
    if start_tag not in tpl or end_tag not in tpl:
        raise SystemExit("模板缺少 <!--DOC:START--> / <!--DOC:END--> 锚点")

    head_end = tpl.index(">", tpl.index('<section id="doc"')) + 1
    prefix = tpl[:head_end]
    suffix = tpl[tpl.index("\n    </section>\n    " + end_tag):]

    return prefix + "\n" + content + suffix


def main():
    ap = argparse.ArgumentParser(description="把 Markdown 文章套进公众号财经模板")
    ap.add_argument("article", help="Markdown 文章路径")
    ap.add_argument("-o", "--out", help="输出 HTML 路径（默认与输入同名 .html）")
    ap.add_argument("--template", default=DEFAULT_TPL, help="模板文件路径")
    ap.add_argument("--no-follow-gif", action="store_true", help="不插入关注引导动图")
    args = ap.parse_args()

    src = args.article
    if not os.path.isfile(src):
        raise SystemExit("找不到文章文件：%s" % src)
    md = open(src, "r", encoding="utf-8").read()
    tpl = open(args.template, "r", encoding="utf-8").read()

    out_html = render(md, tpl, follow_gif=not args.no_follow_gif)

    dst = args.out or os.path.splitext(src)[0] + ".html"
    open(dst, "w", encoding="utf-8", newline="").write(out_html)
    print("OK -> %s (%d bytes)" % (dst, os.path.getsize(dst)))


if __name__ == "__main__":
    main()
