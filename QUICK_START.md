# 快速开始指南

## 🚀 一键部署到GitHub Pages

### 1. 准备数据
```bash
# 确保有Excel数据文件
# 运行部署脚本
python deploy.py
```

### 2. 上传到GitHub
1. 创建新的GitHub仓库
2. 将 `github-pages` 目录中的所有文件上传到仓库
3. 在仓库设置中启用GitHub Pages功能

### 3. 访问网站
访问：`https://你的用户名.github.io/仓库名`

## 🔧 本地测试

### 方法一：使用嵌入数据的版本（推荐）
```bash
# 生成嵌入数据的HTML
python convert_to_embedded.py

# 启动本地服务器
python -m http.server 8000

# 访问
open http://localhost:8000/index_embedded.html
```

### 方法二：使用原始版本
```bash
# 启动本地服务器
python -m http.server 8000

# 访问
open http://localhost:8000/index.html
```

## 📁 文件说明

- `index.html` - 主页面（需要data.json）
- `index_embedded.html` - 嵌入数据的页面（无需外部文件）
- `data.json` - 数据文件
- `test.html` - 数据加载测试页面

## ❓ 常见问题

### Q: 显示"加载数据失败"
**解决方案**：
1. 使用嵌入数据的版本：`index_embedded.html`
2. 或者确保 `data.json` 文件在同一目录下

### Q: 页面样式异常
**解决方案**：
1. 检查网络连接
2. 确保Font Awesome图标库能正常加载

### Q: 数据不更新
**解决方案**：
1. 重新运行 `python calculate_scores.py`
2. 重新运行 `python convert_to_embedded.py`
3. 重新部署

## 🎯 推荐使用方式

**生产环境**：使用 `python deploy.py` 生成的嵌入数据版本
**开发测试**：使用 `index_embedded.html` 进行本地测试
