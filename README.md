# Fanze Meng — Personal website

英文个人网站，通过 GitHub Pages 托管。围绕材料科学、工程数学、研究与工程实践介绍 Fanze Meng，也包含本人补充的登山、骑行与驾驶兴趣。

- 网站：[dmpoolm.github.io](https://dmpoolm.github.io/)
- 源码：[DMPoolM/dmpoolm.github.io](https://github.com/DMPoolM/dmpoolm.github.io)

包含首页、四个同等展示的项目案例、当前研究与已实现进度、早期合作论文、教育背景、其他实验与工业经历、个人兴趣和联系方式。公开 CV 为两页，使用与网页一致的 Georgia / Arial 字体和绿色，不含电话号码。工业项目使用文字概要和原创示意图，没有复制内部源代码、数据或截图。

## 本地预览

只需 Python 3.9 或更新版本，无需安装前端依赖：

```sh
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 8000 --directory public --bind 127.0.0.1
```

打开 `http://127.0.0.1:8000/`。预览时只提供 `public/`，不提供上级 CV 文件夹。

## 修改内容

- `content.json`：姓名、链接、项目、学校与论文。
- `scripts/build.py`：首页结构、项目模板、研究与个人介绍。
- `assets/site.css`：页面风格与手机布局。
- `assets/Fanze_Meng_Resume.pdf`：网站公开简历。
- `scripts/make_resume.py`：重新生成公开简历，需 `reportlab`；日常网站构建不需要此依赖。
- `scripts/make_brand_assets.py`：生成 1200 × 630 分享图和多尺寸 ICO 图标，需 `Pillow`。

两个辅助生成脚本使用 macOS 本机的 Georgia / Arial 字体；生成后的 PDF、PNG 和 ICO 已随源码保存，GitHub Actions 的日常部署不需要安装字体或这些库。原有简历文件路径保留，避免旧链接失效；下载文件名显示为 `Fanze_Meng_CV.pdf`。

修改内容后重新执行构建与检查。`public/` 是生成结果，不加入 Git。

## 发布与更新

按照 [GitHub 创建用户网站的官方说明](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)，使用小写仓库名 `dmpoolm.github.io`。

仓库已建立，Pages 发布来源使用 **GitHub Actions**。后续更新：

1. 在当前 `personal-site` 项目中修改页面内容或样式。
2. 本地运行构建与检查，确认预览正常。
3. 将更改提交并推送至 `main`，不要上传上级 CV 文件夹。
4. `Deploy portfolio to GitHub Pages` 工作流会自动构建网页、检查本地链接，再上传 `public/` 并部署。
5. 在 Actions 中确认部署成功后访问 `https://dmpoolm.github.io/`。

仓库需要启用 Actions，并允许 Pages 部署所需的 `pages: write` 和 `id-token: write`。配置参考 [GitHub Pages 自定义工作流官方文档](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)。

## 当前内容依据与后续素材

内容来自个人 CV、研究项目现有状态记录，以及本人补充的个人兴趣。数字保留原有含义：R² 是验证集结果，97.2% 是候选数量减少，约 50 个任务是评测规模。

当前研究的“Implemented so far”依据已有的数据管线、训练/采样、扩散基线和结构评估实现；不表示生成质量已优于基线或已完成分子动力学输运验证。机器人项目用具体交付物说明成果，不推测未提供的编译通过率或节省时间。两段 MSc 明确为先后取得/攻读的两个学位，早期论文标明为本科期间的合作。

页面区块使用文字标题，案例统一为 `Case 01` 至 `Case 04`。HTML 辅助文字不小于 11px，正文更大；分享元数据包含 Open Graph 和 Twitter large-image card，图片使用站点绝对 URL。根目录 `favicon.ico` 由构建时复制提供。

维护时核对英文介绍、邮箱、项目可公开程度、教育日期和论文信息。未发布完整研究报告与工业项目文件。后续可补充经许可的界面截图、真实结果图、公开代码及论文链接；当前示意图均明确注明为概念图。

站点无登录、表单、分析追踪、外部字体或数据库。未添加自定义域名配置；以后绑定域名时再修改 `content.json` 中的 `url` 以及 GitHub Pages 域名设置。
