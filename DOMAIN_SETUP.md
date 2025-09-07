# GitHub Pages 子路径配置说明

## 当前配置
- **自定义域名**: www.biboran.top
- **访问路径**: https://www.biboran.top/Competition-display/

## 配置步骤

### 1. GitHub仓库设置
1. 进入GitHub仓库的Settings页面
2. 找到Pages部分
3. 在Custom domain中输入: `www.biboran.top`
4. 确保"Enforce HTTPS"已启用
5. 部署源设置为: Deploy from a branch → main → / (root)

### 2. 域名DNS设置
在你的域名提供商处设置以下DNS记录：

```
类型: CNAME
名称: www
值: hmh38324.github.io
```

### 3. 仓库文件配置
- `CNAME` 文件: 包含自定义域名
- `.nojekyll` 文件: 禁用Jekyll处理
- `index.html` 文件: 根目录欢迎页面
- `Competition-display/` 目录: 包含子路径的HTML文件

## 访问方式
- **竞赛系统地址**: https://www.biboran.top/Competition-display/ (主要访问地址)
- **根地址**: https://www.biboran.top (显示欢迎页面，提供进入竞赛系统的链接)

## 注意事项
1. DNS更改可能需要几分钟到几小时生效
2. 确保GitHub Pages设置中的Custom domain正确配置
3. 如果遇到问题，可以检查GitHub Actions的部署日志

## 故障排除
如果无法访问新地址：
1. 检查DNS设置是否正确
2. 确认GitHub Pages设置中的Custom domain
3. 等待DNS传播完成（最多24小时）
