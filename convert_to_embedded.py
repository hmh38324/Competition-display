#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将JSON数据嵌入到HTML文件中，避免CORS问题
"""

import pandas as pd
import json
import os

def convert_to_embedded_html():
    """
    将JSON数据嵌入到HTML文件中
    """
    # 使用仓库相对路径，兼容 GitHub Actions 运行环境
    repo_root = os.path.dirname(os.path.abspath(__file__))
    # 读取Excel文件（由 calculate_scores.py 生成）
    excel_file = os.path.join(repo_root, '积分排名结果.xlsx')
    
    if not os.path.exists(excel_file):
        print("Excel文件不存在，使用示例数据")
        # 使用示例数据
        data = {
            "total_rankings": [
                {"机号": "A01", "班次": "甲班", "总积分": 20, "有效天数": 4, "日均积分": 5.0, "排名": 1},
                {"机号": "A03", "班次": "甲班", "总积分": 16, "有效天数": 4, "日均积分": 4.0, "排名": 2},
                {"机号": "A04", "班次": "甲班", "总积分": 11, "有效天数": 3, "日均积分": 3.67, "排名": 3},
                {"机号": "A05", "班次": "甲班", "总积分": 10, "有效天数": 3, "日均积分": 3.33, "排名": 4},
                {"机号": "A09", "班次": "甲班", "总积分": 7, "有效天数": 3, "日均积分": 2.33, "排名": 5},
                {"机号": "A02", "班次": "甲班", "总积分": 0, "有效天数": 4, "日均积分": 0.0, "排名": 6},
                {"机号": "A01", "班次": "乙班", "总积分": 17, "有效天数": 4, "日均积分": 4.25, "排名": 1},
                {"机号": "A03", "班次": "乙班", "总积分": 14, "有效天数": 4, "日均积分": 3.5, "排名": 2},
                {"机号": "A05", "班次": "乙班", "总积分": 10, "有效天数": 3, "日均积分": 3.33, "排名": 3},
                {"机号": "A04", "班次": "乙班", "总积分": 10, "有效天数": 3, "日均积分": 3.33, "排名": 3},
                {"机号": "A09", "班次": "乙班", "总积分": 4, "有效天数": 3, "日均积分": 1.33, "排名": 4},
                {"机号": "A02", "班次": "乙班", "总积分": 2, "有效天数": 4, "日均积分": 0.5, "排名": 5}
            ],
            "daily_rankings": [
                {"机号": "A01", "产量": 163.2, "积分": 5, "班次": "乙班", "排名": 1, "日期": "9.1"},
                {"机号": "A01", "产量": 153.4, "积分": 5, "班次": "甲班", "排名": 1, "日期": "9.1"},
                {"机号": "A03", "产量": 152.4, "积分": 1, "班次": "甲班", "排名": 2, "日期": "9.1"},
                {"机号": "A05", "产量": 113.6, "积分": 0, "班次": "乙班", "排名": 2, "日期": "9.1"},
                {"机号": "A02", "产量": 112.4, "积分": 0, "班次": "乙班", "排名": 2, "日期": "9.1"},
                {"机号": "A03", "产量": 110.6, "积分": 0, "班次": "乙班", "排名": 2, "日期": "9.1"},
                {"机号": "A05", "产量": 134.8, "积分": 0, "班次": "甲班", "排名": 3, "日期": "9.1"},
                {"机号": "A02", "产量": 127.4, "积分": 0, "班次": "甲班", "排名": 3, "日期": "9.1"},
                {"机号": "A04", "产量": "/", "积分": "/", "班次": "甲班", "排名": "-", "日期": "9.1"},
                {"机号": "A09", "产量": "/", "积分": "/", "班次": "甲班", "排名": "-", "日期": "9.1"},
                {"机号": "A04", "产量": "/", "积分": "/", "班次": "乙班", "排名": "-", "日期": "9.1"},
                {"机号": "A09", "产量": "/", "积分": "/", "班次": "乙班", "排名": "-", "日期": "9.1"}
            ],
            "daily_scores": {
                "9.1": [
                    {"机号": "A01", "甲班_中班_产量": 153.4, "甲班_中班_积分": 5, "乙班_早班_产量": 163.2, "乙班_早班_积分": 5, "总产量": 316.6, "台时不足": False},
                    {"机号": "A02", "甲班_中班_产量": 127.4, "甲班_中班_积分": 0, "乙班_早班_产量": 112.4, "乙班_早班_积分": 0, "总产量": 239.8, "台时不足": False},
                    {"机号": "A03", "甲班_中班_产量": 152.4, "甲班_中班_积分": 1, "乙班_早班_产量": 110.6, "乙班_早班_积分": 0, "总产量": 263.0, "台时不足": False},
                    {"机号": "A04", "甲班_中班_产量": "/", "甲班_中班_积分": "/", "乙班_早班_产量": "/", "乙班_早班_积分": "/", "总产量": "/", "台时不足": True},
                    {"机号": "A05", "甲班_中班_产量": 134.8, "甲班_中班_积分": 0, "乙班_早班_产量": 113.6, "乙班_早班_积分": 0, "总产量": 248.4, "台时不足": False},
                    {"机号": "A09", "甲班_中班_产量": "/", "甲班_中班_积分": "/", "乙班_早班_产量": "/", "乙班_早班_积分": "/", "总产量": "/", "台时不足": True}
                ]
            },
            "last_updated": "2024-01-15 10:30:00"
        }
    else:
        # 读取总分排名
        total_rankings = pd.read_excel(excel_file, sheet_name='总分排名')
        
        # 读取总排名
        daily_rankings = pd.read_excel(excel_file, sheet_name='总排名')
        
        # 读取每日积分数据
        daily_scores = {}
        excel_file_obj = pd.ExcelFile(excel_file)
        
        for sheet_name in excel_file_obj.sheet_names:
            if sheet_name.endswith('_积分'):
                date = sheet_name.replace('_积分', '')
                daily_scores[date] = pd.read_excel(excel_file, sheet_name=sheet_name).to_dict('records')
        
        # 转换为JSON格式
        data = {
            'total_rankings': total_rankings.to_dict('records'),
            'daily_rankings': daily_rankings.to_dict('records'),
            'daily_scores': daily_scores,
            'last_updated': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 将"平均积分"字段名改为"日均积分"
        for ranking in data['total_rankings']:
            if '平均积分' in ranking:
                ranking['日均积分'] = ranking.pop('平均积分')
        
        # 读取negative.xlsx文件中的否样数据
        negative_data = None
        try:
            negative_df = pd.read_excel('negative.xlsx')
            negative_data = negative_df.to_dict('records')
            print(f"成功读取negative.xlsx文件，包含 {len(negative_data)} 条记录")
        except FileNotFoundError:
            print("警告: 未找到negative.xlsx文件")
        except Exception as e:
            print(f"警告: 读取negative.xlsx文件失败: {e}")
        
        # 将否样数据合并到总分排名中
        if negative_data:
            # 创建否样数据的查找字典
            negative_lookup = {}
            for item in negative_data:
                key = f"{item['机号']}_{item['班次']}"
                negative_lookup[key] = item['否样或批量追溯']
            
            # 更新总分排名中的否样次数
            for ranking in data['total_rankings']:
                key = f"{ranking['机号']}_{ranking['班次']}"
                ranking['否样次数'] = negative_lookup.get(key, 0)
    
    # 读取HTML模板（仓库根目录）
    template_path = os.path.join(repo_root, 'index.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 将数据嵌入到HTML中
    data_script = f'<script>window.competitionData = {json.dumps(data, ensure_ascii=False, indent=2)};</script>'
    
    # 替换原来的数据加载代码
    html_content = html_content.replace(
        '        // 页面加载完成后加载数据\n        document.addEventListener(\'DOMContentLoaded\', loadData);',
        '        // 页面加载完成后初始化\n        document.addEventListener(\'DOMContentLoaded\', function() {\n            if (window.competitionData) {\n                competitionData = window.competitionData;\n                initializePage();\n            } else {\n                showError(\'数据加载失败\');\n            }\n        });'
    )
    
    # 移除loadData函数，因为数据已经嵌入
    loadData_start = '        async function loadData() {'
    loadData_end = '        }'
    
    start_pos = html_content.find(loadData_start)
    if start_pos != -1:
        # 找到loadData函数结束的位置
        brace_count = 0
        pos = start_pos
        while pos < len(html_content):
            if html_content[pos] == '{':
                brace_count += 1
            elif html_content[pos] == '}':
                brace_count -= 1
                if brace_count == 0:
                    # 找到匹配的结束括号
                    end_pos = pos + 1
                    # 替换整个函数
                    html_content = html_content[:start_pos] + '        // loadData函数已移除，数据已嵌入到HTML中' + html_content[end_pos:]
                    break
            pos += 1
    
    # 确保参赛机台数显示为12
    html_content = html_content.replace(
        'totalMachines: new Set(totalRankings.map(r => r.机号)).size,',
        'totalMachines: 12, // 固定显示12台机台'
    )
    
    # 在</head>标签前插入数据脚本，先移除可能存在的旧脚本
    # 移除可能存在的旧数据脚本
    import re
    html_content = re.sub(r'<script>window\.competitionData = .*?</script>', '', html_content, flags=re.DOTALL)
    
    # 在</head>标签前插入新的数据脚本
    html_content = html_content.replace('</head>', f'{data_script}\n</head>')
    
    # 保存嵌入数据的HTML文件（仓库根目录）
    output_file = os.path.join(repo_root, 'index_embedded.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"嵌入数据的HTML文件已生成: {output_file}")
    print(f"总分排名记录数: {len(data['total_rankings'])}")
    print(f"总排名记录数: {len(data['daily_rankings'])}")
    print(f"每日积分数据: {list(data['daily_scores'].keys())}")

if __name__ == "__main__":
    convert_to_embedded_html()
