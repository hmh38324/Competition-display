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
cp index_embedded.html github-pages/index.html

# 提交更改
echo "4. 提交更改..."
git add github-pages/index.html
git add 积分排名结果.xlsx
git commit -m "更新分数和排名 - $(date '+%Y-%m-%d %H:%M:%S')"
git push

echo "更新完成！"
