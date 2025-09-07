#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新index.html文件中的数据
"""

import json
import re

def update_index_html():
    """
    更新index.html文件中的数据
    """
    # 读取最新的JSON数据
    with open('/Users/apple/Documents/cursor/test2/data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 读取HTML文件
    with open('/Users/apple/Documents/cursor/test2/index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 生成新的数据脚本
    data_script = f'<script>window.competitionData = {json.dumps(data, ensure_ascii=False, indent=2)};</script>'
    
    # 移除所有旧的window.competitionData脚本
    html_content = re.sub(r'<script>window\.competitionData = .*?</script>', '', html_content, flags=re.DOTALL)
    
    # 确保显示逻辑正确（只显示数字，不显示"次"）
    html_content = re.sub(
        r'const traceabilityText = `\$\{negativeCount\}次`;',
        'const traceabilityText = negativeCount.toString();',
        html_content
    )
    
    # 在</head>标签前插入新的数据脚本
    html_content = html_content.replace('</head>', f'{data_script}\n</head>')
    
    # 保存更新后的HTML文件
    with open('/Users/apple/Documents/cursor/test2/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("index.html文件已更新，数据已同步")

if __name__ == "__main__":
    update_index_html()
