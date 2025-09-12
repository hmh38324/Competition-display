#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
积分计算和排名脚本
根据生产数据计算积分并生成排名
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

def calculate_scores(data):
    """
    计算积分
    积分规则：
    A1-A5：早班不低于156.84箱、中班不低于143.16箱，完成以上产量要求，即可累计积分1分。两班当日总产量不低于300箱各积4分。
    A9:早班不低于41箱、中班不低于39箱，完成以上产量要求，即可累计积分1分。两班当日总产量不低于80箱各积4分。
    
    如果报工数据为空，则表示当天台时不足，不计入竞赛天数，得分用/表示
    """
    scores = []
    
    # 从第一行数据判断当天的班次安排
    first_row = data.iloc[0]
    jia_shift = first_row['甲班']  # 甲班的班次（早班或中班）
    yi_shift = first_row['乙班']   # 乙班的班次（早班或中班）
    
    for _, row in data.iterrows():
        machine = row['机号']
        
        # 获取甲班和乙班的计划和报工数据
        jia_plan = row['计划'] if '计划' in row else 0
        jia_actual = row['报工'] if '报工' in row else None
        yi_plan = row['计划.1'] if '计划.1' in row else 0
        yi_actual = row['报工.1'] if '报工.1' in row else None
        
        # 检查报工数据是否为字符串（台时不足、生产牌号不符等）
        jia_is_string = isinstance(jia_actual, str)
        yi_is_string = isinstance(yi_actual, str)
        
        # 检查是否有报工数据为空（台时不足）
        jia_insufficient = pd.isna(jia_actual) or jia_actual == 0 or jia_is_string
        yi_insufficient = pd.isna(yi_actual) or yi_actual == 0 or yi_is_string
        
        # 检查是否为生产牌号不符
        jia_brand_mismatch = jia_is_string and jia_actual == '生产牌号不符'
        yi_brand_mismatch = yi_is_string and yi_actual == '生产牌号不符'
        
        # 检查是否有生产牌号不符的情况
        if jia_brand_mismatch or yi_brand_mismatch:
            # 有生产牌号不符的情况
            scores.append({
                '机号': machine,
                f'甲班({jia_shift})产量': jia_actual if jia_is_string else '/',
                f'甲班({jia_shift})积分': '/',
                f'乙班({yi_shift})产量': yi_actual if yi_is_string else '/',
                f'乙班({yi_shift})积分': '/',
                '总产量': '/',
                '台时不足': False,
                '生产牌号不符': True
            })
            continue
        
        # 如果甲班或乙班报工数据为空，则当天台时不足
        if jia_insufficient and yi_insufficient:
            # 两个班都台时不足，不计入竞赛
            scores.append({
                '机号': machine,
                f'甲班({jia_shift})产量': '/',
                f'甲班({jia_shift})积分': '/',
                f'乙班({yi_shift})产量': '/',
                f'乙班({yi_shift})积分': '/',
                '总产量': '/',
                '台时不足': True
            })
            continue
        elif jia_insufficient:
            # 只有甲班台时不足
            scores.append({
                '机号': machine,
                f'甲班({jia_shift})产量': '/',
                f'甲班({jia_shift})积分': '/',
                f'乙班({yi_shift})产量': yi_actual,
                f'乙班({yi_shift})积分': '/',
                '总产量': '/',
                '台时不足': True
            })
            continue
        elif yi_insufficient:
            # 只有乙班台时不足
            scores.append({
                '机号': machine,
                f'甲班({jia_shift})产量': jia_actual,
                f'甲班({jia_shift})积分': '/',
                f'乙班({yi_shift})产量': '/',
                f'乙班({yi_shift})积分': '/',
                '总产量': '/',
                '台时不足': True
            })
            continue
        
        # 确保报工数据是数值类型
        jia_actual = float(jia_actual) if not pd.isna(jia_actual) else 0
        yi_actual = float(yi_actual) if not pd.isna(yi_actual) else 0
        
        # 计算总产量
        total_production = round(jia_actual + yi_actual, 1)
        
        # 根据机号确定积分规则
        if machine in ['A01', 'A02', 'A03', 'A04', 'A05']:
            # A1-A5规则
            morning_threshold = 156.84  # 早班阈值
            afternoon_threshold = 143.16  # 中班阈值
            total_threshold = 300   # 总产量阈值
            total_bonus = 4         # 总产量达标奖励
        elif machine == 'A09':
            # A9规则
            morning_threshold = 41      # 早班阈值
            afternoon_threshold = 39    # 中班阈值
            total_threshold = 80    # 总产量阈值
            total_bonus = 4         # 总产量达标奖励
        else:
            # 其他机号，使用A1-A5规则
            morning_threshold = 156.84
            afternoon_threshold = 143.16
            total_threshold = 300
            total_bonus = 4
        
        # 计算甲班积分（根据实际班次）
        jia_score = 0
        if jia_shift == '早班':
            if jia_actual >= morning_threshold:
                jia_score += 1
        elif jia_shift == '中班':
            if jia_actual >= afternoon_threshold:
                jia_score += 1
        if total_production >= total_threshold:
            jia_score += total_bonus
        
        # 计算乙班积分（根据实际班次）
        yi_score = 0
        if yi_shift == '早班':
            if yi_actual >= morning_threshold:
                yi_score += 1
        elif yi_shift == '中班':
            if yi_actual >= afternoon_threshold:
                yi_score += 1
        if total_production >= total_threshold:
            yi_score += total_bonus
        
        # 记录结果
        scores.append({
            '机号': machine,
            f'甲班({jia_shift})产量': jia_actual,
            f'甲班({jia_shift})积分': jia_score,
            f'乙班({yi_shift})产量': yi_actual,
            f'乙班({yi_shift})积分': yi_score,
            '总产量': total_production,
            '台时不足': False
        })
    
    return pd.DataFrame(scores)

def calculate_total_scores(all_daily_scores, negative_data=None):
    """
    计算每个机台的总分
    """
    total_scores = {}
    
    for date, scores_df in all_daily_scores.items():
        for _, row in scores_df.iterrows():
            machine = row['机号']
            
            # 只计算有效记录（非台时不足）
            if not row['台时不足']:
                if machine not in total_scores:
                    total_scores[machine] = {
                        '甲班总分': 0,
                        '乙班总分': 0,
                        '总积分': 0,
                        '甲班总产量': 0,
                        '乙班总产量': 0,
                        '总产量': 0,
                        '有效天数': 0,
                        '甲班否样次数': 0,
                        '乙班否样次数': 0
                    }
                
                # 动态获取甲班和乙班的积分和产量列名
                jia_score_col = None
                yi_score_col = None
                jia_production_col = None
                yi_production_col = None
                
                for col in scores_df.columns:
                    if '甲班' in col and '积分' in col:
                        jia_score_col = col
                    elif '乙班' in col and '积分' in col:
                        yi_score_col = col
                    elif '甲班' in col and '产量' in col:
                        jia_production_col = col
                    elif '乙班' in col and '产量' in col:
                        yi_production_col = col
                
                if jia_score_col and yi_score_col and jia_production_col and yi_production_col:
                    # 只对数值类型的积分和产量进行累加
                    jia_score = pd.to_numeric(row[jia_score_col], errors='coerce')
                    yi_score = pd.to_numeric(row[yi_score_col], errors='coerce')
                    jia_production = pd.to_numeric(row[jia_production_col], errors='coerce')
                    yi_production = pd.to_numeric(row[yi_production_col], errors='coerce')
                    
                    if not pd.isna(jia_score) and not pd.isna(yi_score) and not pd.isna(jia_production) and not pd.isna(yi_production):
                        total_scores[machine]['甲班总分'] += jia_score
                        total_scores[machine]['乙班总分'] += yi_score
                        total_scores[machine]['总积分'] += jia_score + yi_score
                        total_scores[machine]['甲班总产量'] += jia_production
                        total_scores[machine]['乙班总产量'] += yi_production
                        total_scores[machine]['总产量'] += jia_production + yi_production
                        total_scores[machine]['有效天数'] += 1
    
    # 添加否样或批量追溯次数
    if negative_data is not None:
        for _, row in negative_data.iterrows():
            machine = row['机号']
            shift = row['班次']
            negative_count = row['否样或批量追溯']
            
            if machine in total_scores:
                if shift == '甲班':
                    total_scores[machine]['甲班否样次数'] = negative_count
                elif shift == '乙班':
                    total_scores[machine]['乙班否样次数'] = negative_count
    
    return total_scores

def calculate_rankings(scores_df, total_scores=None):
    """
    计算排名，区分甲乙班
    包含所有记录，但台时不足的记录积分为'/'，排名为'-'
    """
    rankings = []
    
    # 分离有效记录和台时不足记录
    valid_scores = scores_df[scores_df['台时不足'] == False].copy()
    insufficient_scores = scores_df[scores_df['台时不足'] == True].copy()
    
    # 动态获取甲班和乙班的列名
    jia_production_col = None
    jia_score_col = None
    yi_production_col = None
    yi_score_col = None
    
    for col in scores_df.columns:
        if '甲班' in col and '产量' in col:
            jia_production_col = col
        elif '甲班' in col and '积分' in col:
            jia_score_col = col
        elif '乙班' in col and '产量' in col:
            yi_production_col = col
        elif '乙班' in col and '积分' in col:
            yi_score_col = col
    
    # 甲班排名
    jia_rankings = []
    
    # 有效记录的甲班排名
    if len(valid_scores) > 0 and jia_production_col and jia_score_col:
        valid_jia = valid_scores[['机号', jia_production_col, jia_score_col]].copy()
        valid_jia['班次'] = '甲班'
        valid_jia['排名'] = valid_jia[jia_score_col].rank(method='dense', ascending=False).astype(int)
        valid_jia = valid_jia.rename(columns={
            jia_production_col: '产量',
            jia_score_col: '积分'
        })
        jia_rankings.append(valid_jia)
    
    # 台时不足记录的甲班排名
    if len(insufficient_scores) > 0 and jia_production_col and jia_score_col:
        insufficient_jia = insufficient_scores[['机号', jia_production_col, jia_score_col]].copy()
        insufficient_jia['班次'] = '甲班'
        insufficient_jia['排名'] = '-'  # 台时不足排名为'-'
        insufficient_jia = insufficient_jia.rename(columns={
            jia_production_col: '产量',
            jia_score_col: '积分'
        })
        jia_rankings.append(insufficient_jia)
    
    # 乙班排名
    yi_rankings = []
    
    # 有效记录的乙班排名
    if len(valid_scores) > 0 and yi_production_col and yi_score_col:
        valid_yi = valid_scores[['机号', yi_production_col, yi_score_col]].copy()
        valid_yi['班次'] = '乙班'
        valid_yi['排名'] = valid_yi[yi_score_col].rank(method='dense', ascending=False).astype(int)
        valid_yi = valid_yi.rename(columns={
            yi_production_col: '产量',
            yi_score_col: '积分'
        })
        yi_rankings.append(valid_yi)
    
    # 台时不足记录的乙班排名
    if len(insufficient_scores) > 0 and yi_production_col and yi_score_col:
        insufficient_yi = insufficient_scores[['机号', yi_production_col, yi_score_col]].copy()
        insufficient_yi['班次'] = '乙班'
        insufficient_yi['排名'] = '-'  # 台时不足排名为'-'
        insufficient_yi = insufficient_yi.rename(columns={
            yi_production_col: '产量',
            yi_score_col: '积分'
        })
        yi_rankings.append(insufficient_yi)
    
    # 合并所有排名
    all_rankings = []
    for ranking_list in [jia_rankings, yi_rankings]:
        if ranking_list:
            all_rankings.extend(ranking_list)
    
    if all_rankings:
        all_rankings_df = pd.concat(all_rankings, ignore_index=True)
        # 排序：先按排名（数字在前，'-'在后），再按积分，最后按产量
        all_rankings_df = all_rankings_df.sort_values(['排名', '积分', '产量'], 
                                                     ascending=[True, False, False], 
                                                     na_position='last')
        return all_rankings_df
    else:
        return pd.DataFrame(columns=['机号', '产量', '积分', '班次', '排名', '日期'])

def process_excel_file(file_path):
    """
    处理Excel文件，计算所有sheet的积分和排名
    """
    # 读取Excel文件的所有sheet
    excel_file = pd.ExcelFile(file_path)
    
    results = {}
    all_daily_rankings = []
    all_daily_scores = {}
    
    for sheet_name in excel_file.sheet_names:
        print(f"处理日期: {sheet_name}")
        
        # 读取数据
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # 清理列名，去除空格
        df.columns = df.columns.str.strip()
        
        # 计算积分
        scores = calculate_scores(df)
        results[f"{sheet_name}_积分"] = scores
        all_daily_scores[sheet_name] = scores
        
        # 计算排名
        rankings = calculate_rankings(scores)
        rankings['日期'] = sheet_name
        all_daily_rankings.append(rankings)
        
        # 统计有效记录
        valid_scores = scores[scores['台时不足'] == False]
        insufficient_count = len(scores[scores['台时不足'] == True])
        
        if len(valid_scores) > 0:
            # 动态获取甲班和乙班的积分列名
            jia_score_col = None
            yi_score_col = None
            for col in valid_scores.columns:
                if '甲班' in col and '积分' in col:
                    jia_score_col = col
                elif '乙班' in col and '积分' in col:
                    yi_score_col = col
            
            if jia_score_col and yi_score_col:
                # 过滤掉字符串值，只计算数值类型的积分
                jia_numeric_scores = pd.to_numeric(valid_scores[jia_score_col], errors='coerce')
                yi_numeric_scores = pd.to_numeric(valid_scores[yi_score_col], errors='coerce')
                print(f"  - 甲班最高积分: {jia_numeric_scores.max()}")
                print(f"  - 乙班最高积分: {yi_numeric_scores.max()}")
            print(f"  - 台时不足机台数: {insufficient_count}")
        else:
            print(f"  - 当日所有机台台时不足，不计入竞赛")
            print(f"  - 台时不足机台数: {insufficient_count}")
    
    # 读取negative文件
    negative_data = None
    try:
        negative_data = pd.read_excel('negative.xlsx')
        print(f"成功读取negative文件，包含 {len(negative_data)} 条记录")
    except FileNotFoundError:
        print("警告: 未找到negative.xlsx文件，将不进行扣分计算")
    except Exception as e:
        print(f"警告: 读取negative.xlsx文件失败: {e}")
    
    # 计算总分
    total_scores = calculate_total_scores(all_daily_scores, negative_data)
    
    # 创建总分排名表
    total_rankings = []
    for machine, scores in total_scores.items():
        # 甲班总分排名
        jia_negative_count = scores.get('甲班否样次数', 0)
        jia_adjusted_score = max(0, scores['甲班总分'] - jia_negative_count)  # 扣分后不能为负数
        total_rankings.append({
            '机号': machine,
            '班次': '甲班',
            '总积分': scores['甲班总分'],
            '有效天数': scores['有效天数'],
            '否样次数': jia_negative_count,
            '日均产量': round(scores['甲班总产量'] / scores['有效天数'], 1) if scores['有效天数'] > 0 else 0,
            '平均积分': round(jia_adjusted_score / scores['有效天数'], 2) if scores['有效天数'] > 0 else 0
        })
        # 乙班总分排名
        yi_negative_count = scores.get('乙班否样次数', 0)
        yi_adjusted_score = max(0, scores['乙班总分'] - yi_negative_count)  # 扣分后不能为负数
        total_rankings.append({
            '机号': machine,
            '班次': '乙班',
            '总积分': scores['乙班总分'],
            '有效天数': scores['有效天数'],
            '否样次数': yi_negative_count,
            '日均产量': round(scores['乙班总产量'] / scores['有效天数'], 1) if scores['有效天数'] > 0 else 0,
            '平均积分': round(yi_adjusted_score / scores['有效天数'], 2) if scores['有效天数'] > 0 else 0
        })
    
    # 计算总分排名（甲班乙班一起按日均积分排名，相同时按日均产量排名）
    if total_rankings:
        total_rankings_df = pd.DataFrame(total_rankings)
        
        # 所有机台一起按日均积分和日均产量排序
        total_rankings_df = total_rankings_df.sort_values(['平均积分', '日均产量', '总积分'], ascending=[False, False, False])
        
        # 重新计算排名，确保按排序后的顺序
        total_rankings_df = total_rankings_df.reset_index(drop=True)
        total_rankings_df['排名'] = total_rankings_df.index + 1
        
        # 按班次和排名排序显示
        total_rankings_df = total_rankings_df.sort_values(['班次', '排名', '平均积分', '日均产量'], ascending=[True, True, False, False])
        results['总分排名'] = total_rankings_df
    
    # 合并所有日期的排名
    all_rankings_df = pd.concat(all_daily_rankings, ignore_index=True)
    results['总排名'] = all_rankings_df
    
    return results

def main():
    """
    主函数
    """
    # 使用仓库相对路径，兼容本地与 GitHub Actions
    repo_root = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(repo_root, 'data.xlsx')
    
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        return
    
    print("开始处理数据...")
    
    # 处理Excel文件
    results = process_excel_file(file_path)
    
    # 输出结果到新的Excel文件
    output_file = os.path.join(repo_root, '积分排名结果.xlsx')
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # 写入总分排名
        if '总分排名' in results:
            results['总分排名'].to_excel(writer, sheet_name='总分排名', index=False)
        
        # 写入总排名
        results['总排名'].to_excel(writer, sheet_name='总排名', index=False)
        
        # 写入每日积分和排名
        for sheet_name, data in results.items():
            if sheet_name not in ['总排名', '总分排名']:
                data.to_excel(writer, sheet_name=sheet_name, index=False)
    
    print(f"\n结果已保存到: {output_file}")
    
    # 显示总分排名
    if '总分排名' in results:
        print("\n总分排名:")
        print(results['总分排名'].to_string(index=False))
    
    # 显示总排名前10名
    print("\n总排名前10名:")
    print(results['总排名'].head(10).to_string(index=False))
    
    # 显示每日统计
    print("\n每日统计:")
    if len(results['总排名']) > 0:
        # 只统计有效记录（排除台时不足的记录）
        valid_rankings = results['总排名'][results['总排名']['积分'] != '/'].copy()
        if len(valid_rankings) > 0:
            # 将积分列转换为数值类型
            valid_rankings['积分'] = pd.to_numeric(valid_rankings['积分'], errors='coerce')
            valid_rankings['产量'] = pd.to_numeric(valid_rankings['产量'], errors='coerce')
            
            daily_stats = valid_rankings.groupby('日期').agg({
                '积分': ['max', 'mean'],
                '产量': 'sum'
            }).round(2)
            print(daily_stats)
        else:
            print("所有日期都因台时不足不计入竞赛")
    else:
        print("所有日期都因台时不足不计入竞赛")
    
    # 显示台时不足统计
    print("\n台时不足统计:")
    for sheet_name in results.keys():
        if sheet_name.endswith('_积分'):
            date = sheet_name.replace('_积分', '')
            scores = results[sheet_name]
            insufficient_count = len(scores[scores['台时不足'] == True])
            valid_count = len(scores[scores['台时不足'] == False])
            print(f"{date}: 有效记录 {valid_count} 条, 台时不足 {insufficient_count} 条")

if __name__ == "__main__":
    main()
