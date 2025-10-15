# 嘚啵嘚的博客

欢迎来到我的个人博客！这里记录着我的生活感悟、技术学习和各种思考。


本博客使用 [Jekyll](https://jekyllrb.com/) 构建，托管在 [GitHub Pages](https://pages.github.com/) 上。

## 一键发布到 GitHub Pages（提高效率）

- 前置：在仓库根目录用 VS Code 打开本项目，已安装 Git，并且远端 `origin` 指向 GitHub 仓库。
- 快速发布（推荐两种方式）：
  - VS Code 任务：打开命令面板 `⇧⌘P` → 输入 `Run Task` → 选择“发布博客到 GitHub Pages”，按提示输入提交说明即可。
  - 命令行脚本：`bash ./publish.sh "sync: 更新博客"`
    - 不传参数时默认消息为 `sync: 更新博客`；脚本会自动：
      - 检测工作区变更并提交（自动附加时间戳）
      - `git pull --rebase` 同步远端，保持线性历史
      - `git push origin master` 推送，触发 GitHub Pages 部署
      - 输出站点地址（优先读取 `CNAME`，否则默认 `blogwego.com`）

提示：可为 VS Code 任务绑定快捷键（`⌘K ⌘S` 打开键盘快捷键 → 绑定 `Tasks: Run Task` 并选择该任务），做到一键发布。

## 本地预览

- 运行：`bundle exec jekyll serve --livereload`
- 访问：`http://127.0.0.1:4000/`
- 修改后会自动刷新，便于快速验证。

## 常见问题

- 部署时间：GitHub Pages 通常 1–3 分钟完成部署；未刷新时可清除浏览器缓存或使用隐私模式。
- 推送失败：多为网络或认证问题，检查：
  - 是否有代理拦截 Git 请求；
  - GitHub 认证是否过期；
  - 仓库的 `origin` URL 是否正确。
