# GitHub Pages 部署指南

## 🚀 快速部署

### 方法一：使用自动化脚本（推荐）

1. **运行部署脚本**：
   ```bash
   python deploy.py
   ```

2. **上传文件**：
   - 将 `github-pages` 目录中的所有文件上传到GitHub仓库

3. **启用Pages**：
   - 进入仓库 Settings → Pages
   - 选择 "Deploy from a branch"
   - 选择 "main" 分支和 "/ (root)" 文件夹

### 方法二：手动部署

1. **准备数据**：
   ```bash
   # 安装依赖
   pip install -r requirements.txt
   
   # 计算积分和排名
   python calculate_scores.py
   
   # 转换为JSON格式
   python convert_to_json.py
   ```

2. **上传文件**：
   需要上传以下文件到GitHub仓库：
   - `index.html` - 主页面
   - `data.json` - 数据文件
   - `README_GitHub.md` - 说明文档

## 📁 文件结构

```
your-repo/
├── index.html          # 主页面
├── data.json          # 数据文件
├── README_GitHub.md   # 说明文档
└── .gitignore         # Git忽略文件
```

## 🔄 更新数据

当需要更新排名数据时：

1. **更新Excel数据文件**
2. **重新生成数据**：
   ```bash
   python calculate_scores.py
   python convert_to_json.py
   ```
3. **上传新的data.json文件到GitHub**

## 🌐 访问网站

部署完成后，访问：
`https://你的用户名.github.io/仓库名`

## 🎨 页面功能

### 总分排名
- 显示各机台的总积分排名
- 区分甲乙班分别排名
- 显示有效天数和平均积分

### 每日排名
- 选择特定日期查看排名
- 显示当日产量和积分
- 台时不足的记录会特别标注

### 详细数据
- 查看每日的详细积分数据
- 显示台时状态
- 包含所有机台的完整信息

## 📱 响应式设计

页面支持各种设备：
- 桌面电脑
- 平板电脑
- 手机

## 🎯 特色功能

- **现代化UI**：渐变色彩和动画效果
- **实时数据**：自动加载最新排名
- **智能排序**：按积分和排名智能排序
- **状态标识**：清晰区分正常和台时不足
- **统计信息**：显示冠军和参赛统计

## 🔧 自定义

### 修改样式
编辑 `index.html` 中的 `<style>` 部分

### 修改数据格式
编辑 `convert_to_json.py` 脚本

### 添加新功能
在 `index.html` 的 `<script>` 部分添加JavaScript代码

## ❓ 常见问题

### Q: 页面显示"加载数据失败"
A: 检查 `data.json` 文件是否存在且格式正确

### Q: 排名显示不正确
A: 检查Excel数据文件格式是否正确

### Q: 页面样式异常
A: 检查网络连接，确保Font Awesome图标库能正常加载

## 📞 技术支持

如有问题，请检查：
1. 数据文件格式是否正确
2. 网络连接是否正常
3. 浏览器控制台是否有错误信息
