#!/bin/bash

echo "开始更新分数和页面..."

# 计算分数和排名
echo "1. 计算分数和排名..."
python3 calculate_scores.py

# 生成嵌入数据的HTML文件
echo "2. 生成嵌入数据的HTML文件..."
python3 convert_to_embedded.py

# 更新GitHub Pages
echo "3. 更新GitHub Pages..."
cp index_embedded.html index.html
cp index_embedded.html github-pages/index.html
cp index_embedded.html Competition-display/index.html
echo "   已将index_embedded.html复制到根目录index.html、github-pages/index.html和Competition-display/index.html"

# 提交更改
echo "4. 提交更改..."
# 先同步远端，避免 non-fast-forward
git fetch origin
# 优先尝试基于最新远端进行 rebase，同步历史
git rebase origin/main || {
  echo "rebase 失败，尝试合并到本地分支"
  git merge --no-edit origin/main || true
}

# 仅提交需要发布的文件，忽略被 .gitignore 忽略的 Excel
git add index.html
git add github-pages/index.html
git add Competition-display/index.html

# 若无改动则跳过提交
if git diff --staged --quiet; then
  echo "无文件变化，跳过提交"
else
  git commit -m "更新分数和排名 - $(date '+%Y-%m-%d %H:%M:%S')"
fi

# 推送，若被拒绝则自动 rebase 后重试
git push || {
  echo "push 被拒绝，自动 pull --rebase 后重试"
  git pull --rebase && git push
}

echo "更新完成！"
