#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从JSON数据生成HTML周报
"""

import json
import re
from datetime import datetime

def escape_html(text):
    """转义HTML特殊字符（但保留已有的HTML标签）"""
    # 如果文本已经包含HTML标签，只转义纯文本部分
    # 这里简化处理，假设用户已经正确使用了HTML标签
    return text

def generate_table_rows(data_list, columns):
    """生成表格行HTML"""
    rows_html = ""
    for item in data_list:
        cells = []
        for col in columns:
            value = item.get(col, "")
            cells.append(f"<td>{escape_html(str(value))}</td>")
        rows_html += f"      <tr>\n        {'\n        '.join(cells)}\n      </tr>\n"
    return rows_html

def update_html_from_json(html_template_path, json_data_path, output_path):
    """从JSON数据更新HTML模板"""
    
    # 读取JSON数据
    with open(json_data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 读取HTML模板
    with open(html_template_path, "r", encoding="utf-8") as f:
        html = f.read()
    
    # 更新报告日期
    report_date = data.get("report_period", {}).get("report_date", datetime.now().strftime("%Y-%m-%d"))
    html = re.sub(
        r'<div class="meta">Market Research Team @ \d{4}-\d{2}-\d{2}',
        f'<div class="meta">Market Research Team @ {report_date}',
        html
    )
    
    # 更新第一部分：工程项目
    if data.get("section1_projects"):
        projects = data["section1_projects"]
        if projects and len(projects) > 0 and projects[0].get("date") != "日期（如：12月1日）":
            rows_html = generate_table_rows(projects, ["date", "region", "details", "impact"])
            tbody_pattern = r'(<section id="sec1">.*?<tbody>).*?(</tbody>)'
            html = re.sub(tbody_pattern, r'\1\n' + rows_html + r'    \2', html, flags=re.DOTALL)
            
            # 更新小结
            if data.get("section1_summary"):
                callout_pattern = r'(<div class="callout"><strong>小结：</strong>).*?(</div>)'
                html = re.sub(callout_pattern, r'\1 ' + data["section1_summary"] + r'\2', html)
    
    # 更新第二部分：行业动态
    if data.get("section2_industry"):
        industry_news = data["section2_industry"]
        if industry_news and len(industry_news) > 0 and industry_news[0].get("date") != "日期":
            rows_html = generate_table_rows(industry_news, ["date", "topic", "content", "significance"])
            tbody_pattern = r'(<section id="sec2">.*?<tbody>).*?(</tbody>)'
            html = re.sub(tbody_pattern, r'\1\n' + rows_html + r'    \2', html, flags=re.DOTALL)
    
    # 更新第三部分：制造企业
    if data.get("section3_manufacturers"):
        manufacturers = data["section3_manufacturers"]
        if manufacturers and len(manufacturers) > 0 and manufacturers[0].get("date") != "日期":
            rows_html = generate_table_rows(manufacturers, ["date", "company", "event", "analysis"])
            tbody_pattern = r'(<section id="sec3">.*?<tbody>).*?(</tbody>)'
            html = re.sub(tbody_pattern, r'\1\n' + rows_html + r'    \2', html, flags=re.DOTALL)
    
    # 更新第四部分：租赁企业
    if data.get("section4_rental"):
        rental_news = data["section4_rental"]
        if rental_news and len(rental_news) > 0 and rental_news[0].get("date") != "日期":
            rows_html = generate_table_rows(rental_news, ["date", "company", "event", "notes"])
            tbody_pattern = r'(<section id="sec4">.*?<tbody>).*?(</tbody>)'
            html = re.sub(tbody_pattern, r'\1\n' + rows_html + r'    \2', html, flags=re.DOTALL)
    
    # 更新第五部分：综合观察
    if data.get("section5_synthesis"):
        synthesis = data["section5_synthesis"]
        if synthesis and len(synthesis) > 0 and not synthesis[0].startswith("综合观察要点"):
            items_html = ""
            for point in synthesis:
                if "：" in point:
                    title, content = point.split("：", 1)
                    items_html += f'    <li><strong>{title}：</strong>{content}</li>\n'
                else:
                    items_html += f'    <li>{point}</li>\n'
            
            ol_pattern = r'(<section id="sec5">.*?<ol>).*?(</ol>)'
            html = re.sub(ol_pattern, r'\1\n' + items_html + r'\2', html, flags=re.DOTALL)
    
    # 更新第六部分：下周前瞻
    if data.get("section6_watchlist"):
        watchlist = data["section6_watchlist"]
        if watchlist and len(watchlist) > 0 and watchlist[0].get("focus") != "关注事项（加粗格式：<strong>事项</strong>）":
            rows_html = generate_table_rows(watchlist, ["focus", "timing", "impact"])
            tbody_pattern = r'(<section id="sec6">.*?<tbody>).*?(</tbody>)'
            html = re.sub(tbody_pattern, r'\1\n' + rows_html + r'    \2', html, flags=re.DOTALL)
    
    # 移除说明框（如果数据已填写）
    if data.get("section1_projects") and len(data["section1_projects"]) > 0:
        note_box_pattern = r'<div class="note-box">.*?</div>'
        html = re.sub(note_box_pattern, "", html, flags=re.DOTALL)
    
    # 保存更新后的HTML
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"周报已生成：{output_path}")

if __name__ == "__main__":
    import sys
    
    template_path = "建筑业周报_2025-12-02.html"
    json_path = "新闻数据模板.json"
    output_path = "建筑业周报_2025-12-02_完整版.html"
    
    if len(sys.argv) > 1:
        json_path = sys.argv[1]
    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    
    try:
        update_html_from_json(template_path, json_path, output_path)
        print("✓ 周报生成成功！")
    except FileNotFoundError as e:
        print(f"✗ 错误：文件未找到 - {e}")
    except json.JSONDecodeError as e:
        print(f"✗ 错误：JSON格式错误 - {e}")
    except Exception as e:
        print(f"✗ 错误：{e}")
