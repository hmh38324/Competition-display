#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化部署脚本
生成数据并准备GitHub Pages部署文件
"""

import os
import shutil
import subprocess
import sys

def run_command(command, description):
    """运行命令并显示进度"""
    print(f"正在{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description}完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description}失败: {e.stderr}")
        return False

def main():
    """主函数"""
    print("🚀 开始准备GitHub Pages部署...")
    
    # 检查必要文件
    required_files = ['calculate_scores.py', 'convert_to_json.py', 'index.html']
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ 缺少必要文件: {file}")
            return False
    
    # 1. 运行积分计算
    if not run_command("python calculate_scores.py", "计算积分和排名"):
        return False
    
    # 2. 转换为JSON
    if not run_command("python convert_to_json.py", "转换数据为JSON格式"):
        return False
    
    # 3. 检查生成的文件
    if not os.path.exists('data.json'):
        print("❌ data.json文件未生成")
        return False
    
    # 4. 创建部署目录
    deploy_dir = 'github-pages'
    if os.path.exists(deploy_dir):
        shutil.rmtree(deploy_dir)
    os.makedirs(deploy_dir)
    
    # 5. 生成嵌入数据的HTML文件
    if not run_command("python convert_to_embedded.py", "生成嵌入数据的HTML文件"):
        return False
    
    # 6. 复制必要文件
    files_to_copy = ['index_embedded.html', 'README_GitHub.md']
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, deploy_dir)
            # 将index_embedded.html重命名为index.html
            if file == 'index_embedded.html':
                shutil.move(os.path.join(deploy_dir, 'index_embedded.html'), 
                           os.path.join(deploy_dir, 'index.html'))
                print(f"✅ 复制文件: {file} (重命名为index.html)")
            else:
                print(f"✅ 复制文件: {file}")
    
    print(f"\n🎉 部署文件已准备完成！")
    print(f"📁 部署目录: {deploy_dir}")
    print(f"📋 需要上传的文件:")
    for file in files_to_copy:
        if os.path.exists(os.path.join(deploy_dir, file)):
            print(f"   - {file}")
    
    print(f"\n📝 部署步骤:")
    print(f"1. 将 {deploy_dir} 目录中的所有文件上传到GitHub仓库")
    print(f"2. 在GitHub仓库设置中启用Pages功能")
    print(f"3. 选择从main分支部署")
    print(f"4. 访问 https://你的用户名.github.io/仓库名")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
