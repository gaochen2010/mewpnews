#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
建筑业周报更新脚本
用于将搜集到的新闻数据更新到HTML周报中
"""

import re
from datetime import datetime
from typing import List, Dict

def update_section_table(html_content: str, section_id: str, rows: List[Dict]) -> str:
    """
    更新指定section的表格内容
    
    Args:
        html_content: HTML内容
        section_id: section的ID（如'sec1'）
        rows: 行数据列表，每行是一个字典，包含表格列的数据
    """
    # 找到对应的section
    section_pattern = rf'<section id="{section_id}">.*?</section>'
    section_match = re.search(section_pattern, html_content, re.DOTALL)
    
    if not section_match:
        print(f"警告：未找到section {section_id}")
        return html_content
    
    section_content = section_match.group(0)
    
    # 找到tbody标签
    tbody_pattern = r'<tbody>.*?</tbody>'
    tbody_match = re.search(tbody_pattern, section_content, re.DOTALL)
    
    if not tbody_match:
        print(f"警告：在section {section_id}中未找到tbody")
        return html_content
    
    # 生成新的表格行
    new_rows_html = ""
    for row in rows:
        cells = "".join([f"<td>{cell}</td>" for cell in row.values()])
        new_rows_html += f"<tr>{cells}</tr>\n      "
    
    # 替换tbody内容
    new_tbody = f"<tbody>\n      {new_rows_html}</tbody>"
    new_section_content = re.sub(tbody_pattern, new_tbody, section_content, flags=re.DOTALL)
    
    # 替换整个section
    return html_content.replace(section_content, new_section_content)

def update_synthesis(html_content: str, points: List[str]) -> str:
    """
    更新综合观察部分
    
    Args:
        html_content: HTML内容
        points: 观察要点列表
    """
    section_pattern = r'<section id="sec5">.*?</section>'
    section_match = re.search(section_pattern, html_content, re.DOTALL)
    
    if not section_match:
        return html_content
    
    section_content = section_match.group(0)
    
    # 生成新的列表项
    new_items = ""
    for i, point in enumerate(points, 1):
        # 如果point已经包含strong标签，直接使用；否则添加
        if "<strong>" in point:
            new_items += f"    <li>{point}</li>\n"
        else:
            # 尝试提取标题和内容
            if "：" in point:
                title, content = point.split("：", 1)
                new_items += f"    <li><strong>{title}：</strong>{content}</li>\n"
            else:
                new_items += f"    <li><strong>要点{i}：</strong>{point}</li>\n"
    
    # 替换ol内容
    ol_pattern = r'<ol>.*?</ol>'
    new_ol = f"<ol>\n{new_items}</ol>"
    new_section_content = re.sub(ol_pattern, new_ol, section_content, flags=re.DOTALL)
    
    return html_content.replace(section_content, new_section_content)

def update_watchlist(html_content: str, items: List[Dict]) -> str:
    """
    更新下周前瞻表格
    
    Args:
        html_content: HTML内容
        items: 前瞻事项列表，每个item包含'focus', 'timing', 'impact'键
    """
    section_pattern = r'<section id="sec6">.*?</section>'
    section_match = re.search(section_pattern, html_content, re.DOTALL)
    
    if not section_match:
        return html_content
    
    section_content = section_match.group(0)
    
    # 生成新的表格行
    new_rows_html = ""
    for item in items:
        focus = item.get('focus', '')
        timing = item.get('timing', '')
        impact = item.get('impact', '')
        new_rows_html += f'      <tr>\n        <td><strong>{focus}</strong></td>\n        <td>{timing}</td>\n        <td>{impact}</td>\n      </tr>\n'
    
    # 替换tbody内容
    tbody_pattern = r'<tbody>.*?</tbody>'
    new_tbody = f"<tbody>\n{new_rows_html}    </tbody>"
    new_section_content = re.sub(tbody_pattern, new_tbody, section_content, flags=re.DOTALL)
    
    return html_content.replace(section_content, new_section_content)

def update_summary(html_content: str, section_id: str, summary_text: str) -> str:
    """
    更新section的callout摘要
    
    Args:
        html_content: HTML内容
        section_id: section的ID
        summary_text: 摘要文本
    """
    section_pattern = rf'<section id="{section_id}">.*?</section>'
    section_match = re.search(section_pattern, html_content, re.DOTALL)
    
    if not section_match:
        return html_content
    
    section_content = section_match.group(0)
    
    # 查找并替换callout
    callout_pattern = r'<div class="callout">.*?</div>'
    new_callout = f'<div class="callout"><strong>小结：</strong> {summary_text}</div>'
    
    if re.search(callout_pattern, section_content, re.DOTALL):
        new_section_content = re.sub(callout_pattern, new_callout, section_content, flags=re.DOTALL)
    else:
        # 如果没有callout，在table后面添加
        table_pattern = r'(</table>)'
        new_section_content = re.sub(table_pattern, r'\1\n  ' + new_callout, section_content)
    
    return html_content.replace(section_content, new_section_content)

# 使用示例
if __name__ == "__main__":
    # 读取HTML文件
    with open("建筑业周报_2025-12-02.html", "r", encoding="utf-8") as f:
        html = f.read()
    
    # 示例：更新第一部分（工程项目）
    projects = [
        {
            "date": "12月1日",
            "region": "<strong>美国 — 某大型数据中心项目</strong>",
            "details": "项目详情...",
            "impact": "影响分析..."
        }
    ]
    
    # 注意：需要根据实际的表格列数调整
    # 这里只是示例，实际使用时需要匹配表格的列结构
    
    print("脚本已准备就绪。")
    print("使用方法：")
    print("1. 搜集新闻数据")
    print("2. 按照函数格式整理数据")
    print("3. 调用相应的更新函数")
    print("4. 保存更新后的HTML文件")
