# GitHub 文档中快速插入项目内部链接的方法

在 GitHub 的 Markdown 文档中，你可以使用相对路径来链接到项目中的其他文档。

## GitHub Markdown 中的链接方式

在 GitHub 的 Markdown 中，你应该使用以下格式来链接到项目内的其他文件：

```markdown
[链接文字](相对路径/文件名.md)
```

## 其他链接技巧

1. **链接到同一仓库中的文件**：
   ```markdown
   [文件名](./path/to/file.md)
   ```

2. **链接到特定文件的特定部分**（通过标题锚点）：
   ```markdown
   [链接到某节](./path/to/file.md#标题名称)
   ```
   注意：锚点名称是标题文本转换为小写，空格替换为连字符

3. **链接到特定的代码行**：
   ```markdown
   [代码行](./path/to/file.py#L10-L20)
   ```

4. **链接到 Issues 或 Pull Requests**：
   ```markdown
   [Issue #123](#123)
   ```

这些方法可以帮助你在 GitHub 文档中快速创建指向项目内其他文件的链接，提高文档的可读性和导航性。