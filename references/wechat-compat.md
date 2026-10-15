# 微信公众号排版兼容性要点

这些是踩过的坑，改模板或排查"粘过去样式坏了"时先看这里。

## 1. 样式必须全部内联

公众号编辑器会**剥离 `<style>` 标签和 class**。所以正文里每个元素都要写 `style="..."`，不能用 class 选样式。

模板页面顶部的 `<style>` 只服务于本地预览和工具栏 UI，不参与复制。

## 2. 容器用 `<section>`，不用 `<div>`

`<div>` 在公众号里容易被处理掉块级语义（边距、边框丢失），`<section>` 更可靠。

## 3. 图片：外链不吃，base64 吃

- 公众号编辑器**不支持外链图片**（会自动丢弃）
- 但**支持 base64 内嵌**——复制时浏览器会把 `data:image/...` 连同 HTML 一起写进剪贴板，公众号后台接收后**自动转存到素材库**

所以关注引导 GIF 以 base64 内嵌在模板里，一键复制时会跟着走。若个别情况下没跟过去，手动上传同目录的 `.gif` 兜底。

**注意**：外部图片（正文里的配图、数据图）仍需在公众号里手动上传，模板里用虚线占位框提示。

## 4. CSS 动画不支持

公众号不支持 `@keyframes` / `animation`。模板里的呼吸闪烁动效只在本地预览可见；复制时 `buildHTML()` 会**遍历剥掉所有 class**，只留纯静态内联样式，粘过去是干净的静态引导条。

想要真的会动，唯一办法是 **GIF**（或视频/动图）。

## 5. 表格的坑（本模板已全部绕开）

1. **公众号编辑器粘贴时会重写 `<table>` 结构**——`border-collapse:separate` 被改回、单元格样式被剥，圆角和隔行色必坏。所以本模板的表格**用 section + flex 实现，彻底不用 table 标签**：圆角表头条自带 `border-radius:8px 8px 0 0`，编辑器不会碰它。
2. section 版表格的每个单元格务必带 `box-sizing:border-box`——公众号环境没有全局 border-box，不加的话 padding 会把列宽撑爆。
3. 隔行底色直接写在行容器（行 section）上，不要依赖 tr。
4. 表头底色用中性色（如 `#ecf3ef`），不要跟随主题主色，否则切换主题时容易和文字色撞。

若表格粘贴后排版错乱，最稳的兜底是**截图成图片插入**。

## 6. 中文字体与对齐

- 字体栈：`-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',Arial,sans-serif`
- 中文段落两端对齐：`text-align:justify;text-justify:inter-ideograph;`（后者对中文生效）
- 中英文之间、数字与单位之间手动留半角空格，观感更好

## 7. 复制通道（模板页里的实现）

1. 优先 `navigator.clipboard.write([new ClipboardItem({'text/html': …, 'text/plain': …})])` —— 保留样式
2. 失败（`file://` 或非安全上下文）降级为离屏节点 + `Range` + `document.execCommand('copy')`
3. 内嵌预览面板有时会拦剪贴板权限，此时用 Chrome 直接打开文件复制最稳

## 8. 其它

- `<h2>` / `<strong>` / `<table>` 等语义标签公众号是保留的，可放心用；但不要依赖它们的默认样式，字号颜色都显式写。
- 空段落会被公众号编辑器吞掉，需要间距就用 `margin`，不要用空 `<p>` 占位。
- 行内代码用 `<span>` 加底色模拟，比 `<code>` 更稳。
