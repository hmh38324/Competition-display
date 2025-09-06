# 生产竞赛排名系统

一个美观的网页应用，用于展示生产竞赛的排名和积分统计。

## 功能特点

- 🏆 **总分排名**：按日均积分排名，更公平的排名方式
- 📅 **每日排名**：查看特定日期的排名情况
- 📊 **详细数据**：展示每日的详细积分和产量数据
- 📱 **响应式设计**：支持手机和桌面设备
- 🎨 **现代化UI**：美观的渐变色彩和动画效果

## 部署到GitHub Pages

### 1. 准备数据

首先运行Python脚本生成数据：

```bash
# 安装依赖
pip install -r requirements.txt

# 运行积分计算脚本
python calculate_scores.py

# 转换为JSON格式
python convert_to_json.py
```

### 2. 上传到GitHub

1. 创建新的GitHub仓库
2. 将以下文件上传到仓库：
   - `index.html`
   - `data.json`
   - `README_GitHub.md`

### 3. 启用GitHub Pages

1. 进入仓库的Settings页面
2. 找到"Pages"部分
3. 选择"Deploy from a branch"
4. 选择"main"分支和"/ (root)"文件夹
5. 点击"Save"

### 4. 访问网站

部署完成后，可以通过以下URL访问：
`https://你的用户名.github.io/仓库名`

## 文件说明

- `index.html` - 主页面文件
- `data.json` - 数据文件（由convert_to_json.py生成）
- `calculate_scores.py` - 积分计算脚本
- `convert_to_json.py` - 数据转换脚本
- `requirements.txt` - Python依赖

## 更新数据

要更新网页上的数据，请按以下步骤操作：

1. 更新Excel数据文件
2. 运行 `python calculate_scores.py`
3. 运行 `python convert_to_json.py`
4. 将新的 `data.json` 文件上传到GitHub仓库

## 技术栈

- HTML5
- CSS3 (Flexbox, Grid)
- JavaScript (ES6+)
- Font Awesome 图标
- 响应式设计

## 浏览器支持

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## 许可证

MIT License
