# -*- coding: utf-8 -*-
"""简化第一次进度汇报：去掉细进度/分工/甘特图，加入 9 张表截图。"""

from pathlib import Path

p = Path(r"C:\Users\Administrator\Documents\Codex\2026-11-02\ju\outputs\Sports-Events\presentation\build_progress_deck.py")
text = p.read_text(encoding="utf-8")

i6 = text.index("# ---------- 6 数据库设计 ----------")
i7 = text.index("# ---------- 7 当前进度 ----------")
i8 = text.index("# ---------- 8 阶段成果 ----------")
i9 = text.index("# ---------- 9 难点与风险 ----------")
i11 = text.index("# ---------- 11 请指导 ----------")

db_block = '''# ---------- 6 数据库设计 ----------
s = new_slide(prs)
header(s, "03 / 方案 · 数据库", "9 张表已定稿，先结构后接口")

NAVICAT_IMG = r"C:\\Users\\Administrator\\Documents\\Codex\\2026-11-02\\ju\\outputs\\Sports-Events\\presentation\\assets\\navicat.png"
s.shapes.add_picture(NAVICAT_IMG, Inches(0.75), Inches(1.85), width=Inches(11.83))

infos = [
    ("表结构", "9 张表 · InnoDB · utf8mb4"),
    ("关键设计", "逻辑删除、唯一索引防重复报名"),
    ("当前状态", "初版完成，随接口小幅调整"),
]
for i, (t, d) in enumerate(infos):
    x = 0.75 + i * 3.97
    shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, 5.35, 3.8, 0.9, CARD, BORDER, 1.0, 0.12)
    textbox(s, x + 0.2, 5.45, 3.4, 0.28, t, 10.2, True, NAVY)
    textbox(s, x + 0.2, 5.75, 3.45, 0.4, d, 8.6, False, MUTED)

textbox(s, 0.75, 6.45, 11.8, 0.3, "截图：Navicat 中 sports_events 库的 9 张表（演示数据）。", 9.5, False, MUTED)
notes(s, "数据库部分是九张表，已经定稿。截图是在 Navicat 里打开 sports_events 库看到的结果，"
         "包括用户、赛事、项目、报名、赛程、成绩、公告和字典表。先定结构再写接口，后面只做小幅调整。")

# ---------- 7 已完成 / 下一步 ----------
s = new_slide(prs)
header(s, "04 / 进展", "做了什么，接下来做什么")

shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, 0.75, 1.9, 5.75, 4.25, CARD, BORDER, 1.0, 0.05)
hd = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, 0.75, 1.9, 5.75, 0.58, GREEN, None, 1.0, 0.06)
shape_text(hd, "已经完成", 13, True, WHITE)
done = [
    "需求梳理，确定三类角色与 P0 范围",
    "数据库 9 张表设计",
    "前后端框架、登录与 JWT 权限",
    "赛事 / 项目 / 报名接口与基础页面",
]
for i, d in enumerate(done):
    y = 2.75 + i * 0.78
    shape(s, MSO_SHAPE.OVAL, 1.02, y + 0.1, 0.1, 0.1, GREEN)
    textbox(s, 1.25, y, 5.0, 0.5, d, 10.6, False, TEXT)

shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, 6.83, 1.9, 5.75, 4.25, CARD, BORDER, 1.0, 0.05)
hd2 = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, 6.83, 1.9, 5.75, 0.58, AMBER, None, 1.0, 0.06)
shape_text(hd2, "接下来要做", 13, True, WHITE)
todo = [
    "报名审核闭环与页面联调",
    "赛程编排、成绩录入",
    "统计图表与资讯模块",
    "测试、部署与答辩材料",
]
for i, d in enumerate(todo):
    y = 2.75 + i * 0.78
    shape(s, MSO_SHAPE.OVAL, 7.1, y + 0.1, 0.1, 0.1, AMBER)
    textbox(s, 7.33, y, 5.0, 0.5, d, 10.6, False, TEXT)

textbox(s, 0.75, 6.35, 11.6, 0.3, "原则：先把 P0 的报名闭环做扎实，再补赛程和成绩。", 9.8, True, NAVY2)
notes(s, "目前完成的是需求、数据库、框架、登录和赛事项目报名的主链路；接下来重点做报名审核联调、赛程成绩、统计和测试。先把报名闭环做扎实。")

'''

progress_block = ''

stage_header_old = 'header(s, "04 / 阶段成果", "已经能跑起来的部分")'
stage_header_new = 'header(s, "05 / 阶段成果", "已经能跑起来的部分")'

new_text = text[:i6] + db_block + text[i8:i9].replace(stage_header_old, stage_header_new) + text[i11:]

# 提纲第 4 项改为阶段成果
new_text = new_text.replace('("04", "风险与计划", "难点、应对、分工与里程碑")',
                            '("04", "阶段成果", "已经能跑起来的页面")')
# 封面备注措辞
new_text = new_text.replace("今天主要讲清楚四件事：要做什么、打算怎么做、现在做到哪、下一步怎么安排。",
                            "今天主要讲清楚四件事：要做什么、打算怎么做、现在做到哪、接下来做什么。")

p.write_text(new_text, encoding="utf-8")
print("patched; chars:", len(new_text))
