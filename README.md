# Fanze Meng — Personal website

英文研究与项目作品集。目标托管：GitHub Pages；目标仓库：`DMPoolM/dmpoolm.github.io`；目标网址：`https://dmpoolm.github.io/`。这些是预定配置，仓库与线上地址需要完成发布后才可使用。

第一版包含首页、四个项目案例、进行中的研究、论文、教育背景、联系方式，以及不含电话号码的公开简历。工业项目使用文字概要和原创示意图，没有复制内部源代码、数据或截图。

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

修改内容后重新执行构建与检查。`public/` 是生成结果，不加入 Git。

## 发布到 GitHub Pages

按照 [GitHub 创建用户网站的官方说明](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)，使用小写仓库名 `dmpoolm.github.io`。

1. 在 GitHub 账号 `DMPoolM` 下新建 `dmpoolm.github.io` 仓库。若已有同名仓库，先检查现有内容，不覆盖。
2. 将**当前 personal-site 文件夹**作为独立仓库推送至 `main`，不要上传整个 CV 文件夹。
3. 在仓库的 **Settings → Pages → Build and deployment → Source** 选择 **GitHub Actions**。
4. 运行已提供的 `Deploy portfolio to GitHub Pages` 工作流。它构建网页、检查本地链接，再上传 `public/` 并部署。
5. 在 Actions 中确认部署成功后访问 `https://dmpoolm.github.io/`。

仓库需要启用 Actions，并允许 Pages 部署所需的 `pages: write` 和 `id-token: write`。配置参考 [GitHub Pages 自定义工作流官方文档](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)。

## 当前内容依据与后续素材

内容来自现有 CV、更新后的 MI-6 resume 与上次会话；数字保留原有含义：R² 是验证集结果，97.2% 是候选数量减少，约 50 个任务是评测规模。当前研究路线明确标为进行中或计划。

上线前可核对：英文介绍、邮箱、项目可公开程度、教育日期和论文信息。暂不发布完整研究报告与工业项目文件。后续可补充经许可的界面截图、真实结果图、公开代码及论文链接；当前示意图均明确注明为概念图。

站点无登录、表单、分析追踪、外部字体或数据库。未添加自定义域名配置；以后绑定域名时再修改 `content.json` 中的 `url` 以及 GitHub Pages 域名设置。
