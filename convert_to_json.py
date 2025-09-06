#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将Excel数据转换为JSON格式，供网页展示使用
"""

import pandas as pd
import json
import os

def convert_excel_to_json():
    """
    将Excel数据转换为JSON格式
    """
    # 读取Excel文件
    excel_file = '/Users/apple/Documents/cursor/test2/积分排名结果.xlsx'
    
    if not os.path.exists(excel_file):
        print("Excel文件不存在，请先运行calculate_scores.py生成数据")
        return
    
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
    
    # 确保所有记录都有日均积分字段
    for ranking in data['total_rankings']:
        if '日均积分' not in ranking and '平均积分' in ranking:
            ranking['日均积分'] = ranking['平均积分']
    
    # 保存为JSON文件
    json_file = '/Users/apple/Documents/cursor/test2/data.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"数据已转换为JSON格式，保存到: {json_file}")
    print(f"总分排名记录数: {len(data['total_rankings'])}")
    print(f"总排名记录数: {len(data['daily_rankings'])}")
    print(f"每日积分数据: {list(daily_scores.keys())}")

if __name__ == "__main__":
    convert_excel_to_json()
