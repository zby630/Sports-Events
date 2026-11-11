# -*- coding: utf-8 -*-
"""生成《校园体育赛事管理系统》第一次进度汇报 PPT（未完成、方向明确版）。"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

# ---------- 设计系统 ----------
NAVY = RGBColor(0x0F, 0x27, 0x42)
NAVY2 = RGBColor(0x17, 0x3A, 0x5E)
TEAL = RGBColor(0x14, 0xB8, 0xA6)
TEAL_DARK = RGBColor(0x0E, 0x8F, 0x82)
AMBER = RGBColor(0xF5, 0x9E, 0x0B)
AMBER_DARK = RGBColor(0xB4, 0x6E, 0x00)
GREEN = RGBColor(0x10, 0xB9, 0x81)
GREEN_DARK = RGBColor(0x06, 0x7A, 0x58)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
TEXT = RGBColor(0x1F, 0x29, 0x37)
MUTED = RGBColor(0x64, 0x74, 0x8B)
LIGHT = RGBColor(0xF4, 0xF7, 0xFB)
CARD = RGBColor(0xF8, 0xFA, 0xFC)
BORDER = RGBColor(0xE2, 0xE8, 0xF0)
PALE_TEAL = RGBColor(0xE6, 0xF7, 0xF5)
PALE_AMBER = RGBColor(0xFE, 0xF5, 0xE3)
PALE_GRAY = RGBColor(0xF1, 0xF5, 0xF9)
PALE_NAVY = RGBColor(0xE8, 0xEE, 0xF6)

FONT = "Microsoft YaHei"
SW, SH = 13.333, 7.5


def _ea(run):
    rPr = run._r.get_or_add_rPr()
    el = rPr.find(qn("a:ea"))
    if el is None:
        el = rPr.makeelement(qn("a:ea"), {})
        rPr.append(el)
    el.set("typeface", FONT)


def style_run(run, size=14, bold=False, color=TEXT):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = FONT
    _ea(run)


def textbox(slide, x, y, w, h, text, size=14, bold=False, color=TEXT,
            align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, line_spacing=1.15):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    p.line_spacing = line_spacing
    run = p.add_run()
    run.text = text
    style_run(run, size, bold, color)
    return tb


def shape(slide, kind, x, y, w, h, fill, line=None, line_w=1.0, radius=None):
    sp = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        sp.fill.background()
    else:
        sp.fill.solid()
        sp.fill.fore_color.rgb = fill
    if line is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line
        sp.line.width = Pt(line_w)
    sp.shadow.inherit = False
    if radius is not None:
        try:
            sp.adjustments[0] = radius
        except Exception:
            pass
    return sp


def shape_text(sp, text, size=14, bold=False, color=TEXT, align=PP_ALIGN.CENTER,
               anchor=MSO_ANCHOR.MIDDLE, margins=(0.08, 0.03, 0.08, 0.03)):
    tf = sp.text_frame
    tf.word_wrap = True
    tf.margin_left, tf.margin_right, tf.margin_top, tf.margin_bottom = [Inches(m) for m in margins]
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    style_run(run, size, bold, color)


def header(slide, kicker, title):
    textbox(slide, 0.75, 0.48, 6.0, 0.3, kicker, 11, True, AMBER_DARK)
    textbox(slide, 0.75, 0.78, 11.5, 0.62, title, 28, True, NAVY)
    shape(slide, MSO_SHAPE.RECTANGLE, 0.75, 1.52, 0.55, 0.055, AMBER)
    shape(slide, MSO_SHAPE.RECTANGLE, 0.75, 1.60, 11.83, 0.012, BORDER)


def chip(slide, x, y, w, h, text, fill, color, size=9.5, bold=True):
    sp = shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, fill, None, 1.0, 0.45)
    shape_text(sp, text, size, bold, color)


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def new_slide(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


prs = Presentation()
prs.slide_width = Inches(SW)
prs.slide_height = Inches(SH)
prs.core_properties.title = "校园体育赛事管理系统 · 第一次进度汇报"

# ---------- 1 封面 ----------
s = new_slide(prs)
shape(s, MSO_SHAPE.RECTANGLE, 0, 0, SW, SH, NAVY)
shape(s, MSO_SHAPE.OVAL, 10.2, -1.4, 5.0, 5.0, None, RGBColor(0x1E, 0x4A, 0x6B), 1.5)
shape(s, MSO_SHAPE.OVAL, 11.5, 4.7, 1.0, 1.0, AMBER)
shape(s, MSO_SHAPE.RECTANGLE, 0.9, 1.55, 0.45, 0.06, AMBER)

textbox(s, 0.9, 1.78, 8.0, 0.32, "课程设计 · 第一次进度汇报", 13, True, AMBER)
textbox(s, 0.88, 2.18, 9.4, 0.9, "校园体育赛事管理系统", 44, True, WHITE)
textbox(s, 0.9, 3.2, 8.8, 0.45, "阶段目标：需求确定 · 架构搭好 · 核心流程跑通", 17, False, RGBColor(0xC7, 0xD2, 0xE0))

for i, t in enumerate(["需求分析", "架构设计", "原型开发"]):
    x = 0.9 + i * 1.9
    sp = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, 3.95, 1.7, 0.46, None, RGBColor(0x2C, 0x5A, 0x7C), 1.0, 0.5)
    shape_text(sp, t, 11.5, False, RGBColor(0xC7, 0xD2, 0xE0))

textbox(s, 0.9, 6.1, 7.5, 0.3, "汇报人：________        2026 年 11 月", 12, False, RGBColor(0x94, 0xA3, 0xB8))
textbox(s, 9.3, 6.1, 3.4, 0.3, "当前完成度约 55%", 11, True, AMBER, PP_ALIGN.RIGHT)
notes(s, "老师好，这是我们小组的第一次进度汇报。项目还没有做完，目前完成度大概一半多一点。"
         "今天主要讲清楚四件事：要做什么、打算怎么做、现在做到哪、接下来做什么。")

# ---------- 2 目录 ----------
s = new_slide(prs)
header(s, "汇报提纲", "今天讲四件事")
items = [
    ("01", "项目背景与目标", "为什么做、做到什么程度"),
    ("02", "需求与总体方案", "三类角色、核心流程、架构与数据库"),
    ("03", "当前进度", "已完成、进行中、待开始"),
    ("04", "阶段成果", "已经能跑起来的页面"),
]
for i, (n, t, d) in enumerate(items):
    x = 0.75 + (i % 2) * 5.95
    y = 2.0 + (i // 2) * 2.05
    shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, 5.7, 1.75, CARD, BORDER, 1.0, 0.06)
    textbox(s, x + 0.3, y + 0.25, 0.8, 0.6, n, 26, True, AMBER)
    textbox(s, x + 1.15, y + 0.3, 4.3, 0.4, t, 15.5, True, NAVY)
    textbox(s, x + 1.15, y + 0.85, 4.3, 0.6, d, 10.2, False, MUTED)

textbox(s, 0.75, 6.35, 11.6, 0.3, "汇报重点：把“做什么、怎么做、做到哪、下一步”讲清楚，而不是展示完成品。", 10.2, False, MUTED)
notes(s, "汇报分四部分：背景目标、需求方案、当前进度、风险计划。因为是第一次汇报，重点讲思路和进度，不追求功能完整。")

# ---------- 3 背景与目标 ----------
s = new_slide(prs)
header(s, "01 / 项目背景", "为什么做这套系统")
textbox(s, 0.75, 1.85, 6.0, 0.32, "传统组织方式的三个痛点", 14, True, NAVY)
pain = [
    ("01", "报名靠群接龙、Excel", "重复提交、漏报错报，名单要人工合并"),
    ("02", "赛程靠人工排表", "场地、时间冲突难发现，改一次很麻烦"),
    ("03", "成绩散落在表格里", "排名、奖牌统计靠手工，容易出错"),
]
for i, (n, t, d) in enumerate(pain):
    y = 2.3 + i * 1.28
    shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, 0.75, y, 6.1, 1.1, CARD, BORDER, 1.0, 0.08)
    c = shape(s, MSO_SHAPE.OVAL, 0.97, y + 0.29, 0.5, 0.5, PALE_AMBER)
    shape_text(c, n, 11, True, AMBER_DARK)
    textbox(s, 1.65, y + 0.14, 4.9, 0.3, t, 13, True, NAVY)
    textbox(s, 1.65, y + 0.52, 4.9, 0.45, d, 10.2, False, MUTED)

shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, 7.15, 1.85, 5.4, 4.55, NAVY, None, 1.0, 0.05)
textbox(s, 7.5, 2.05, 4.7, 0.35, "阶段目标", 15, True, WHITE)
goals = [
    ("一个平台", "赛事、项目、报名、赛程、成绩统一管理"),
    ("三类角色", "管理员、教师、学生，按角色授权"),
    ("先通主链路", "优先跑通“建赛事 → 报名 → 审核”"),
]
for i, (t, d) in enumerate(goals):
    y = 2.6 + i * 1.0
    shape(s, MSO_SHAPE.RECTANGLE, 7.5, y + 0.05, 0.05, 0.6, AMBER)
    textbox(s, 7.72, y, 4.4, 0.3, t, 12.5, True, WHITE)
    textbox(s, 7.72, y + 0.33, 4.4, 0.55, d, 10.0, False, RGBColor(0xC7, 0xD2, 0xE0))
textbox(s, 7.5, 5.6, 4.6, 0.35, "本期不追求大而全，先把核心闭环做通。", 10.3, True, AMBER)
notes(s, "背景是报名、赛程、成绩都靠人工，容易出错。我们的目标不是一次做完所有功能，而是先把核心闭环跑通：建赛事、发布、报名、审核。")

# ---------- 4 需求范围 ----------
s = new_slide(prs)
header(s, "02 / 需求范围", "三类角色，一条主流程")
roles = [
    ("管理员", NAVY, "赛事、项目、用户、审核"),
    ("教师", TEAL_DARK, "成绩、赛程、报名审核"),
    ("学生", AMBER, "浏览赛事、报名、我的成绩"),
]
for i, (name, color, desc) in enumerate(roles):
    x = 0.75 + i * 3.95
    shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, 1.85, 3.75, 1.05, CARD, BORDER, 1.0, 0.08)
    shape(s, MSO_SHAPE.RECTANGLE, x, 1.85, 0.08, 1.05, color)
    textbox(s, x + 0.25, 1.98, 3.2, 0.3, name, 13, True, color)
    textbox(s, x + 0.25, 2.35, 3.3, 0.4, desc, 10.0, False, MUTED)

textbox(s, 0.75, 3.2, 4.0, 0.3, "核心流程（本期重点）", 13, True, NAVY)
steps = ["创建赛事", "发布报名", "学生报名", "报名审核", "编排赛程", "录入成绩"]
line = s.shapes.add_connector(1, Inches(1.15), Inches(4.35), Inches(11.9), Inches(4.35))
line.line.color.rgb = RGBColor(0xD5, 0xDE, 0xE8)
line.line.width = Pt(2)
for i, t in enumerate(steps):
    cx = 1.35 + i * 2.05
    done = i < 2
    c = shape(s, MSO_SHAPE.OVAL, cx - 0.23, 4.12, 0.46, 0.46, GREEN if done else (AMBER if i < 4 else RGBColor(0xCB, 0xD5, 0xE1)))
    shape_text(c, str(i + 1), 10, True, WHITE, margins=(0, 0, 0, 0))
    textbox(s, cx - 0.85, 4.7, 1.7, 0.3, t, 10.5, True, NAVY, PP_ALIGN.CENTER)

textbox(s, 0.75, 5.35, 4.0, 0.3, "范围与优先级", 12.5, True, NAVY)
chip(s, 0.75, 5.72, 3.5, 0.42, "P0 赛事 / 项目 / 报名 / 审核", PALE_AMBER, AMBER_DARK, 9.3)
chip(s, 4.35, 5.72, 3.3, 0.42, "P1 赛程 / 成绩 / 导入导出", PALE_TEAL, TEAL_DARK, 9.3)
chip(s, 7.75, 5.72, 2.9, 0.42, "P2 统计 / 资讯 / 用户", PALE_NAVY, NAVY2, 9.3)
textbox(s, 0.75, 6.35, 11.6, 0.3, "绿色 = 已完成，橙色 = 进行中；本期只承诺 P0，P1/P2 按进度推进。", 9.4, False, MUTED)
notes(s, "需求上分三类角色、六个核心步骤。我们把功能分成 P0/P1/P2 三级，第一次汇报只承诺 P0 的赛事、项目、报名和审核，赛程成绩作为下一阶段。")

# ---------- 5 技术架构 ----------
s = new_slide(prs)
header(s, "03 / 总体方案", "前后端分离，容器化部署")
layers = [
    ("展示层", "Vue 3 · TypeScript · Element Plus · ECharts"),
    ("接入层", "Nginx：静态资源 + /api 反向代理"),
    ("业务层", "Spring Boot 3.2 · Spring Security + JWT · MyBatis-Plus"),
    ("数据层", "MySQL 8.0（InnoDB / utf8mb4）· Druid 连接池"),
]
for i, (tag, content) in enumerate(layers):
    y = 1.9 + i * 1.0
    lb = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, 0.75, y, 1.35, 0.74, NAVY if i % 2 == 0 else NAVY2, None, 1.0, 0.12)
    shape_text(lb, tag, 10.5, True, WHITE)
    cb = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, 2.22, y, 6.4, 0.74, CARD, BORDER, 1.0, 0.1)
    shape_text(cb, content, 10.8, False, TEXT, PP_ALIGN.LEFT, margins=(0.18, 0.03, 0.1, 0.03))
    if i < 3:
        shape(s, MSO_SHAPE.DOWN_ARROW, 1.34, y + 0.78, 0.18, 0.16, RGBColor(0xCB, 0xD5, 0xE1))

dep = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, 0.75, 5.95, 7.9, 0.6, PALE_TEAL, None, 1.0, 0.2)
shape_text(dep, "Docker Compose：frontend + backend + mysql 一键启动", 10.8, True, TEAL_DARK,
           PP_ALIGN.LEFT, margins=(0.2, 0.03, 0.1, 0.03))

shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, 9.3, 1.9, 3.28, 4.65, LIGHT, BORDER, 1.0, 0.05)
textbox(s, 9.55, 2.05, 2.85, 0.3, "选型理由", 12.5, True, NAVY)
reasons = [
    ("前后端分离", "页面与接口独立开发、独立部署"),
    ("JWT 无状态", "不存 Session，适合多端和扩展"),
    ("MySQL 8", "事务、索引、utf8mb4 满足需求"),
    ("Docker", "开发、演示环境一致"),
]
for i, (t, d) in enumerate(reasons):
    y = 2.5 + i * 0.98
    textbox(s, 9.55, y, 2.75, 0.28, t, 10.3, True, NAVY)
    textbox(s, 9.55, y + 0.3, 2.75, 0.55, d, 8.8, False, MUTED)
notes(s, "技术方案是前后端分离：Vue 做页面，Spring Boot 做接口，MySQL 存数据，JWT 做无状态认证，最后用 Docker 一键部署。选型以团队熟悉、资料多、能按时完成为主。")

# ---------- 6 数据库设计 ----------
s = new_slide(prs)
header(s, "03 / 方案 · 数据库", "9 张表已定稿，先结构后接口")

NAVICAT_IMG = r"C:\Users\Administrator\Documents\Codex\2026-11-02\ju\outputs\Sports-Events\presentation\assets\navicat.png"
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

# ---------- 8 阶段成果 ① ----------
ASSETS = r"C:\Users\Administrator\Documents\Codex\2026-11-02\ju\outputs\Sports-Events\presentation\assets"

def demo_card(slide, x, y, w, img_path, title):
    shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, 3.75, CARD, BORDER, 1.0, 0.05)
    iw = w - 0.28
    pic = slide.shapes.add_picture(img_path, Inches(x + 0.14), Inches(y + 0.14), width=Inches(iw))
    ih = pic.height / 914400
    textbox(slide, x + 0.2, y + 0.14 + ih + 0.14, w - 0.4, 0.3, title, 12.5, True, NAVY)

s = new_slide(prs)
header(s, "05 / 阶段成果", "登录与教师端：已经能跑起来")
demo_card(s, 0.75, 1.9, 5.75, ASSETS + r"\login.png", "登录页")
demo_card(s, 6.83, 1.9, 5.75, ASSETS + r"\teacher.png", "教师首页")
textbox(s, 0.75, 6.1, 11.6, 0.3, "页面已经能跑起来，业务数据与交互还在补齐。", 9.6, False, MUTED)
notes(s, "这是目前的阶段成果。左边是登录页，三类账号都能登录；右边是教师登录后的首页，"
         "统计卡片和图表框架已经出来，部分数据还在接。")

# ---------- 9 阶段成果 ② ----------
s = new_slide(prs)
header(s, "06 / 阶段成果", "学生端与管理端：同一套界面，不同菜单")
demo_card(s, 0.75, 1.9, 5.75, ASSETS + r"\student.png", "学生首页")
demo_card(s, 6.83, 1.9, 5.75, ASSETS + r"\admin.png", "管理员首页")
textbox(s, 0.75, 6.1, 11.6, 0.3, "同一套前端按角色渲染菜单，权限由前端路由和后端接口共同控制。", 9.6, False, MUTED)
notes(s, "这两张是学生和管理员登录后的界面。学生只有报名、赛程、成绩这些菜单；管理员多了赛事、项目、用户和统计，"
         "同一套前端按角色显示不同菜单。")

# ---------- 10 谢谢 ----------
s = new_slide(prs)
shape(s, MSO_SHAPE.RECTANGLE, 0, 0, SW, SH, NAVY)
shape(s, MSO_SHAPE.OVAL, -1.2, 4.7, 4.0, 4.0, None, RGBColor(0x1E, 0x4A, 0x6B), 1.5)
shape(s, MSO_SHAPE.OVAL, 11.1, -1.0, 3.0, 3.0, None, RGBColor(0x1E, 0x4A, 0x6B), 1.2)
shape(s, MSO_SHAPE.RECTANGLE, 0.95, 2.75, 1.0, 0.06, AMBER)
textbox(s, 0.9, 2.95, 8.0, 0.9, "谢谢", 52, True, WHITE)
textbox(s, 0.95, 3.95, 8.0, 0.4, "请老师和同学批评指正", 18, False, RGBColor(0xC7, 0xD2, 0xE0))
notes(s, "我的汇报到这里，谢谢老师和同学，请批评指正。")

out = r"C:\Users\Administrator\Documents\Codex\2026-11-02\ju\outputs\Sports-Events\presentation\校园体育赛事管理系统-第一次进度汇报-v3.pptx"
prs.save(out)
print("saved:", out)
print("slides:", len(prs.slides))
