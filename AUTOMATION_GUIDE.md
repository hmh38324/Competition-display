# 自动化更新指南

## 概述
本项目提供了多种方式来自动计算分数并更新GitHub Pages页面。

## 自动化方式

### 1. GitHub Actions 自动更新
- **自动触发**: 每天上午8点自动执行
- **手动触发**: 在GitHub仓库的Actions页面手动运行
- **文件变更触发**: 当 `data.xlsx`、`negative.xlsx` 等关键文件更新时自动执行

### 2. 本地脚本更新
使用 `update_pages.sh` 脚本快速更新：

```bash
./update_pages.sh
```

### 3. 手动更新步骤
如果需要手动更新，按以下步骤操作：

```bash
# 1. 计算分数和排名
python3 calculate_scores.py

# 2. 生成嵌入数据的HTML文件
python3 convert_to_embedded.py

# 3. 更新GitHub Pages
cp index_embedded.html github-pages/index.html

# 4. 提交更改
git add github-pages/index.html
git add 积分排名结果.xlsx
git commit -m "更新分数和排名 - $(date '+%Y-%m-%d %H:%M:%S')"
git push
```

## 工作流文件说明

### `.github/workflows/update-scores.yml`
- 自动定时更新（每天8点）
- 文件变更时自动触发
- 支持手动触发

### `.github/workflows/manual-update.yml`
- 仅支持手动触发
- 提供更详细的日志输出
- 可以添加自定义更新说明

## 使用建议

1. **日常使用**: 依赖自动定时更新即可
2. **紧急更新**: 使用本地脚本或GitHub Actions手动触发
3. **数据更新**: 更新Excel文件后，系统会自动检测并重新计算

## 注意事项

- 确保 `data.xlsx` 和 `negative.xlsx` 文件格式正确
- GitHub Actions需要仓库有适当的权限设置
- 本地脚本需要Python环境和相关依赖包
