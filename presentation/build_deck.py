# -*- coding: utf-8 -*-
"""构建《校园体育赛事管理系统》5 分钟汇报 PPT。"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from pptx.enum.shapes import MSO_CONNECTOR

# ---------- 设计系统 ----------
NAVY = RGBColor(0x0F, 0x27, 0x42)
NAVY2 = RGBColor(0x17, 0x3A, 0x5E)
TEAL = RGBColor(0x14, 0xB8, 0xA6)
TEAL_DARK = RGBColor(0x0E, 0x8F, 0x82)
ORANGE = RGBColor(0xF5, 0x9E, 0x0B)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
TEXT = RGBColor(0x1F, 0x29, 0x37)
MUTED = RGBColor(0x64, 0x74, 0x8B)
LIGHT = RGBColor(0xF4, 0xF7, 0xFB)
CARD = RGBColor(0xF8, 0xFA, 0xFC)
BORDER = RGBColor(0xE2, 0xE8, 0xF0)
PALE_TEAL = RGBColor(0xE6, 0xF7, 0xF5)
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


def style_run(run, size=14, bold=False, color=TEXT, italic=False):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    run.font.name = FONT
    _ea(run)


def textbox(slide, x, y, w, h, text, size=14, bold=False, color=TEXT,
            align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, line_spacing=1.15,
            margins=(0, 0, 0, 0)):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left, tf.margin_right, tf.margin_top, tf.margin_bottom = [Inches(m) for m in margins]
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
               anchor=MSO_ANCHOR.MIDDLE, margins=(0.08, 0.04, 0.08, 0.04), line_spacing=1.0):
    tf = sp.text_frame
    tf.word_wrap = True
    tf.margin_left, tf.margin_right, tf.margin_top, tf.margin_bottom = [Inches(m) for m in margins]
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    p.line_spacing = line_spacing
    run = p.add_run()
    run.text = text
    style_run(run, size, bold, color)


def header(slide, kicker, title):
    textbox(slide, 0.75, 0.48, 6.0, 0.3, kicker, 11, True, TEAL)
    textbox(slide, 0.75, 0.78, 11.4, 0.62, title, 29, True, NAVY)
    shape(slide, MSO_SHAPE.RECTANGLE, 0.75, 1.52, 0.55, 0.055, TEAL)
    shape(slide, MSO_SHAPE.RECTANGLE, 0.75, 1.60, 11.83, 0.012, BORDER)


def footer(slide, num):
    shape(slide, MSO_SHAPE.RECTANGLE, 0.75, 7.02, 11.83, 0.01, BORDER)
    textbox(slide, 0.75, 7.10, 8.0, 0.25, "校园体育赛事管理系统 · 项目汇报", 9, False, MUTED)
    textbox(slide, 11.6, 7.10, 1.0, 0.25, f"{num:02d}", 9, True, MUTED, PP_ALIGN.RIGHT)


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def new_slide(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


# ---------- 演示文稿 ----------
prs = Presentation()
prs.slide_width = Inches(SW)
prs.slide_height = Inches(SH)
prs.core_properties.title = "校园体育赛事管理系统 · 项目汇报"
prs.core_properties.author = "Sports Events"

# 1 封面
s = new_slide(prs)
shape(s, MSO_SHAPE.RECTANGLE, 0, 0, SW, SH, NAVY)
# 装饰
shape(s, MSO_SHAPE.OVAL, 9.9, -1.55, 5.4, 5.4, None, RGBColor(0x1E, 0x4A, 0x6B), 1.5)
shape(s, MSO_SHAPE.OVAL, 11.35, 4.55, 1.15, 1.15, TEAL)
shape(s, MSO_SHAPE.OVAL, 10.7, 5.9, 0.32, 0.32, ORANGE)
shape(s, MSO_SHAPE.RECTANGLE, 0.9, 1.62, 0.42, 0.06, TEAL)

textbox(s, 0.9, 1.85, 7.5, 0.35, "课程设计 · 项目汇报", 13, True, TEAL)
textbox(s, 0.88, 2.28, 9.2, 0.95, "校园体育赛事管理系统", 46, True, WHITE)
textbox(s, 0.9, 3.32, 8.4, 0.5, "基于 Spring Boot 3 + Vue 3 的赛事全流程管理平台", 18, False, RGBColor(0xC7, 0xD2, 0xE0))

# 标签
tags = ["赛事报名", "赛程编排", "成绩统计"]
for i, t in enumerate(tags):
    x = 0.9 + i * 1.75
    sp = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, 4.12, 1.55, 0.46, None, RGBColor(0x2C, 0x5A, 0x7C), 1.0, 0.5)
    shape_text(sp, t, 11.5, False, RGBColor(0xC7, 0xD2, 0xE0))

textbox(s, 0.9, 6.25, 7.5, 0.3, "汇报人：________        2026 年 11 月", 12, False, RGBColor(0x94, 0xA3, 0xB8))
textbox(s, 0.9, 6.65, 8.5, 0.3, "在线演示：http://localhost:3000", 10, False, RGBColor(0x64, 0x74, 0x8B))
notes(s, "各位老师、同学好，我汇报的项目是校园体育赛事管理系统。它面向管理员、教师、学生三类角色，"
         "把赛事发布、报名审核、赛程编排、成绩统计串成一条线上闭环。今天用五分钟介绍功能、真实界面、"
         "技术实现和几个排错案例。")

# 2 功能全景
s = new_slide(prs)
header(s, "01 / 功能全景", "三类角色，一套系统")
roles = [
    ("管理员", NAVY, ["赛事与项目管理", "报名审核", "用户与权限", "数据统计"]),
    ("教师", TEAL_DARK, ["成绩录入与修改", "Excel 导入导出", "赛程查看", "报名审核"]),
    ("学生", ORANGE, ["浏览赛事", "在线报名", "我的报名", "我的成绩与奖牌"]),
]
for i, (name, color, items) in enumerate(roles):
    x = 0.75 + i * 3.95
    shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, 1.88, 3.75, 2.95, CARD, BORDER, 1.0, 0.06)
    hd = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, 1.88, 3.75, 0.62, color, None, 1.0, 0.06)
    shape_text(hd, name, 14, True, WHITE)
    for j, it in enumerate(items):
        yy = 2.68 + j * 0.48
        shape(s, MSO_SHAPE.OVAL, x + 0.28, yy + 0.12, 0.1, 0.1, color)
        textbox(s, x + 0.5, yy, 3.0, 0.35, it, 11.5, False, TEXT)

textbox(s, 0.75, 5.08, 3.0, 0.3, "核心模块", 13, True, NAVY)
modules = ["赛事管理", "项目管理", "报名审核", "赛程编排", "成绩管理", "资讯公告", "统计分析", "用户管理"]
for i, m in enumerate(modules):
    x = 0.75 + i * 1.48
    sp = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, 5.45, 1.36, 0.48, PALE_NAVY, None, 1.0, 0.35)
    shape_text(sp, m, 10, False, NAVY2)

textbox(s, 0.75, 6.18, 11.0, 0.3, "9 张数据表   ·   68 个后端接口   ·   16 个前端页面", 11, False, MUTED)
notes(s, "功能上按角色划分：管理员管赛事、项目、用户和审核；教师负责成绩录入和导入导出；"
         "学生浏览赛事、报名、看成绩。底层是八个核心模块，共 9 张表、68 个接口、16 个页面。")

# 3 界面演示（登录 + 教师）
ASSETS = r"C:\Users\Administrator\Documents\Codex\2026-11-02\ju\outputs\Sports-Events\presentation\assets"

def demo_card(slide, x, y, w, img_path, title, desc):
    shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, 3.92, CARD, BORDER, 1.0, 0.05)
    iw = w - 0.28
    pic = slide.shapes.add_picture(img_path, Inches(x + 0.14), Inches(y + 0.14), width=Inches(iw))
    ih = pic.height / 914400
    textbox(slide, x + 0.2, y + 0.14 + ih + 0.12, w - 0.4, 0.3, title, 13, True, NAVY)
    textbox(slide, x + 0.2, y + 0.14 + ih + 0.46, w - 0.4, 0.4, desc, 9.6, False, MUTED)

s = new_slide(prs)
header(s, "02 / 界面演示", "登录与教师端：同一套系统，不同视角")
demo_card(s, 0.75, 1.92, 5.75, ASSETS + r"\login.png", "登录界面", "统一入口，演示账号一键填充，JWT 登录")
demo_card(s, 6.83, 1.92, 5.75, ASSETS + r"\teacher.png", "教师账号主界面", "成绩录入 / 导入导出、赛程查看、报名审核")
textbox(s, 0.75, 6.28, 11.5, 0.3, "截图来自本机运行环境 localhost:3000，数据为演示数据。", 9.2, False, MUTED)
notes(s, "这是系统的真实界面。左边是登录页，三类账号都可以登录；右边是教师登录后的首页，"
         "有统计卡片和图表，左侧菜单是成绩、赛程、报名审核等教师权限功能。")

# 4 界面演示（学生 + 管理员）
s = new_slide(prs)
header(s, "03 / 界面演示", "学生端与管理端：报名与全局管理")
demo_card(s, 0.75, 1.92, 5.75, ASSETS + r"\student.png", "学生账号主界面", "浏览赛事、在线报名、我的报名与我的成绩")
demo_card(s, 6.83, 1.92, 5.75, ASSETS + r"\admin.png", "管理员账号主界面", "赛事 / 项目 / 用户 / 审核 / 统计全局管理")
textbox(s, 0.75, 6.28, 11.5, 0.3, "同一套界面按角色动态渲染菜单，权限由前端路由与后端接口双重控制。", 9.2, False, MUTED)
notes(s, "左边是学生视角，菜单只有我的报名、赛程、我的成绩；右边是管理员视角，多了赛事、项目、"
         "用户管理和统计分析。同一套前端，菜单随角色变化。")

# 5 架构
s = new_slide(prs)
header(s, "04 / 技术架构", "前后端分离，容器化部署")
layers = [
    ("展示层", "Vue 3 · TypeScript · Element Plus · ECharts · Pinia"),
    ("接入层", "Nginx：静态资源托管 + /api 反向代理"),
    ("业务层", "Spring Boot 3.2 · Spring Security + JWT · MyBatis-Plus"),
    ("数据层", "MySQL 8.0（InnoDB / utf8mb4）· Druid 连接池"),
]
for i, (tag, content) in enumerate(layers):
    y = 1.92 + i * 1.06
    lb = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, 0.75, y, 1.35, 0.78, NAVY if i % 2 == 0 else NAVY2, None, 1.0, 0.12)
    shape_text(lb, tag, 11, True, WHITE)
    cb = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, 2.22, y, 6.55, 0.78, CARD, BORDER, 1.0, 0.1)
    shape_text(cb, content, 11.5, False, TEXT, PP_ALIGN.LEFT, margins=(0.18, 0.04, 0.1, 0.04))
    if i < 3:
        ar = shape(s, MSO_SHAPE.DOWN_ARROW, 1.34, y + 0.82, 0.18, 0.2, RGBColor(0xCB, 0xD5, 0xE1))
        ar.shadow.inherit = False

dep = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, 0.75, 6.18, 8.0, 0.62, PALE_TEAL, None, 1.0, 0.2)
shape_text(dep, "Docker Compose：frontend + backend + mysql 一键启动，环境一致", 11.5, True, TEAL_DARK,
           PP_ALIGN.LEFT, margins=(0.2, 0.04, 0.1, 0.04))

shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, 9.35, 1.92, 3.25, 4.88, LIGHT, BORDER, 1.0, 0.05)
textbox(s, 9.6, 2.1, 2.8, 0.3, "为什么这样选", 13, True, NAVY)
reasons = [
    ("前后端分离", "前端独立构建，Nginx 托管，接口复用"),
    ("无状态鉴权", "JWT 携带角色，便于多端与扩展"),
    ("ORM 提效", "MyBatis-Plus 减少样板 SQL"),
    ("一键部署", "镜像 + Compose，开发生产一致"),
]
for i, (t, d) in enumerate(reasons):
    y = 2.55 + i * 1.02
    textbox(s, 9.6, y, 2.75, 0.28, t, 10.8, True, NAVY)
    textbox(s, 9.6, y + 0.3, 2.75, 0.6, d, 9.3, False, MUTED)
notes(s, "技术架构分四层：Vue 3 展示，Nginx 接入，Spring Boot 业务，MySQL 存储。"
         "选择前后端分离、JWT 无状态鉴权、MyBatis-Plus 和 Docker Compose，兼顾开发效率和部署一致性。")

# 5 数据库
s = new_slide(prs)
header(s, "05 / 数据库设计", "9 张表支撑赛事全流程")

boxes = [
    (0.72, 2.15, "用户 sys_user", "id · username · role"),
    (2.98, 2.15, "报名 registration", "user_id · item_id · status"),
    (5.24, 2.15, "项目 sport_item", "event_id · name · 性别限制"),
    (7.50, 2.15, "赛事 event", "名称 · 起止日期 · status"),
]
for x, y, t, sub in boxes:
    b = shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, 2.05, 1.02, WHITE, BORDER, 1.2, 0.08)
    textbox(s, x + 0.12, y + 0.12, 1.85, 0.32, t, 11.5, True, NAVY)
    textbox(s, x + 0.12, y + 0.5, 1.85, 0.4, sub, 8.3, False, MUTED)

for x in (2.78, 5.04, 7.30):
    ar = shape(s, MSO_SHAPE.RIGHT_ARROW, x, 2.52, 0.18, 0.24, TEAL)
    ar.shadow.inherit = False

lower = [
    (0.72, 4.15, "公告 news", "event_id · is_top · status"),
    (2.98, 4.15, "成绩 result", "score · ranking · points"),
    (5.24, 4.15, "字典 sys_dict", "dict_code · item_value"),
    (7.50, 4.15, "赛程 schedule", "match_date · location"),
]
for x, y, t, sub in lower:
    shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, 2.05, 0.95, WHITE, BORDER, 1.2, 0.08)
    textbox(s, x + 0.12, y + 0.1, 1.85, 0.3, t, 11.2, True, NAVY)
    textbox(s, x + 0.12, y + 0.45, 1.85, 0.35, sub, 8.0, False, MUTED)

# 关联线
for x in (4.0, 8.52):
    shape(s, MSO_SHAPE.RECTANGLE, x, 3.2, 0.02, 0.92, RGBColor(0xCB, 0xD5, 0xE1))
textbox(s, 4.08, 3.45, 0.7, 0.25, "N:1", 8, True, MUTED)
textbox(s, 8.6, 3.45, 0.7, 0.25, "N:1", 8, True, MUTED)

shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, 0.75, 5.42, 8.65, 0.95, CARD, BORDER, 1.0, 0.1)
textbox(s, 0.95, 5.53, 8.3, 0.3, "关系：赛事 1:N 项目 / 赛程 / 公告；用户 1:N 报名；报名 N:1 项目；成绩 N:1 赛事 / 项目 / 用户", 9.2, False, TEXT)
textbox(s, 0.95, 5.88, 8.3, 0.3, "字典拆为 sys_dict_type / sys_dict_data 两张配置表；全部关联由应用层校验，未建外键。", 9.2, False, MUTED)

# 右侧设计要点
shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, 9.75, 1.92, 2.83, 4.55, LIGHT, BORDER, 1.0, 0.06)
textbox(s, 9.93, 2.08, 2.5, 0.3, "设计要点", 12.5, True, NAVY)
points = [
    "9 张表，按业务模块拆分",
    "逻辑删除 is_deleted，可追溯",
    "唯一索引防重复报名",
    "utf8mb4 全链路中文支持",
    "event_id / status 建索引",
]
for i, p in enumerate(points):
    y = 2.52 + i * 0.72
    shape(s, MSO_SHAPE.OVAL, 9.95, y + 0.08, 0.08, 0.08, TEAL)
    textbox(s, 10.12, y, 2.3, 0.6, p, 9.6, False, TEXT)
notes(s, "数据库一共 9 张表，按系统、赛事、报名、赛程、成绩、公告分模块。几个关键设计："
         "逻辑删除保留数据、联合唯一索引防止重复报名、utf8mb4 保证中文、按查询频率建索引。"
         "没有建外键，关联完整性由应用层校验。")

# 6 数据库操作
s = new_slide(prs)
header(s, "06 / 数据库操作", "在 Navicat 中打开并编辑这 9 张表")

NAVICAT_IMG = r"C:\Users\Administrator\Documents\Codex\2026-11-02\ju\outputs\Sports-Events\presentation\assets\navicat.png"
pic = s.shapes.add_picture(NAVICAT_IMG, Inches(0.75), Inches(1.85), width=Inches(11.83))

infos = [
    ("连接", "127.0.0.1 : 3307    root / root"),
    ("查看与编辑", "双击表看数据；双击单元格修改后 Ctrl+S"),
    ("结构与 SQL", "右键「设计表」改结构；新建查询执行 SQL"),
]
for i, (t, d) in enumerate(infos):
    x = 0.75 + i * 3.97
    shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, 5.34, 3.8, 0.9, CARD, BORDER, 1.0, 0.12)
    textbox(s, x + 0.2, 5.44, 3.4, 0.28, t, 10.2, True, NAVY)
    textbox(s, x + 0.2, 5.74, 3.45, 0.4, d, 8.6, False, MUTED)

textbox(s, 0.75, 6.48, 11.8, 0.3, "截图来自本机 Navicat：sports_events 库，9 张表全部为 InnoDB、utf8mb4。", 9.5, False, MUTED)
notes(s, "这张就是我在 Navicat 里打开 sports_events 库的截图，九张表都在，右侧能看到行数和注释。"
         "双击表可以改数据，右键设计表可以改结构，也可以新建查询直接跑 SQL。")

# 7 流程
s = new_slide(prs)
header(s, "07 / 核心流程", "从创建赛事到成绩归档，六步闭环")
steps = [
    ("创建赛事", "默认草稿，可反复编辑"),
    ("发布报名", "状态切换为报名中"),
    ("学生报名", "校验资格、人数与时间"),
    ("报名审核", "通过或拒绝并留痕"),
    ("编排赛程", "日期、场地、组别"),
    ("录入成绩", "排名、积分、导出"),
]
line = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(1.2), Inches(3.02), Inches(12.1), Inches(3.02))
line.line.color.rgb = RGBColor(0xD5, 0xDE, 0xE8)
line.line.width = Pt(2)

for i, (t, d) in enumerate(steps):
    cx = 1.45 + i * 2.02
    c = shape(s, MSO_SHAPE.OVAL, cx - 0.31, 2.71, 0.62, 0.62, NAVY if i % 2 == 0 else TEAL_DARK)
    shape_text(c, str(i + 1), 13, True, WHITE, margins=(0, 0, 0, 0))
    textbox(s, cx - 0.95, 2.05, 1.9, 0.3, t, 12, True, NAVY, PP_ALIGN.CENTER)
    textbox(s, cx - 0.95, 3.5, 1.9, 0.65, d, 9.2, False, MUTED, PP_ALIGN.CENTER)

shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, 0.75, 4.55, 11.83, 1.28, CARD, BORDER, 1.0, 0.08)
textbox(s, 1.0, 4.68, 11.3, 0.3, "赛事状态：1 草稿  →  2 报名中  →  3 进行中  →  4 已结束", 10.8, True, NAVY2)
textbox(s, 1.0, 5.0, 11.3, 0.3, "报名状态：1 待审核  →  2 已通过 / 3 已拒绝 / 4 已取消", 10.8, True, NAVY2)
textbox(s, 1.0, 5.32, 11.3, 0.3, "发布仅限草稿；删除仅限草稿；已结束赛事不可取消 —— 状态机保证流程不越界", 9.8, False, MUTED)

textbox(s, 0.75, 6.1, 11.5, 0.3, "报名动作 = 写入报名记录 + 更新项目报名人数，放在同一个事务里，避免人数与名单不一致。", 10.5, False, MUTED)
notes(s, "核心流程是六步：创建赛事、发布报名、学生报名、审核、排赛程、录成绩。"
         "每一步都有状态约束，比如只有草稿能发布和删除。报名和人数更新在同一个事务里，保证一致性。")

# 7 亮点
s = new_slide(prs)
header(s, "08 / 技术亮点", "四个让项目“能演示”的细节")
cards = [
    ("01", "Excel 导入导出", "EasyExcel 生成模板与成绩表；导入逐行校验，返回成功数与失败明细", "现场演示：成绩页 → 导出 / 导入"),
    ("02", "我的成绩与奖牌", "参赛次数、金银铜牌实时统计，学生端一屏可见", "现场演示：我的成绩 → 奖牌卡片"),
    ("03", "可视化统计", "报名 Top10、赛事状态、类型分布、月度趋势，ECharts 渲染", "现场演示：统计页 → 状态分布"),
    ("04", "权限与安全", "JWT + Spring Security，路由与接口双重校验，密码 BCrypt 加密", "现场演示：切换账号 → 菜单变化"),
]
for i, (n, t, d, demo) in enumerate(cards):
    x = 0.75 + (i % 2) * 5.95
    y = 1.92 + (i // 2) * 2.1
    shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, 5.75, 1.86, CARD, BORDER, 1.0, 0.07)
    textbox(s, x + 0.28, y + 0.18, 0.6, 0.4, n, 17, True, TEAL)
    textbox(s, x + 0.9, y + 0.2, 4.6, 0.35, t, 14, True, NAVY)
    textbox(s, x + 0.9, y + 0.72, 4.6, 0.7, d, 10.2, False, MUTED)
    textbox(s, x + 0.9, y + 1.42, 4.6, 0.25, demo, 8.8, True, TEAL_DARK)

textbox(s, 0.75, 6.3, 11.4, 0.3, "这些细节让系统不只是“能跑”，而是可以完整演示、经得起提问。", 11, False, MUTED)
notes(s, "几个可以现场演示的细节：成绩 Excel 导入导出、学生端奖牌统计、ECharts 图表，"
         "以及 JWT 加角色权限的双重校验。")

# 8 排错
s = new_slide(prs)
header(s, "09 / 工程实践", "三个真实问题，三次定位与修复")
rows = [
    ("中文全部乱码", "客户端按 latin1 解析 UTF-8，写入后双重编码", "SET NAMES utf8mb4 + 重建数据 + 校验字节", "修复后重新导入，中文与十六进制均核对"),
    ("赛程页 500", "空 matchDate 仍被执行 LocalDate.parse", "改为非空才解析，兼容空格", "空参数与日期筛选均回归通过"),
    ("后端启动失败", "3306 被本机 MySQL 占用；健康检查过早", "映射 3307 + TCP 探活 + 重启策略", "三容器健康启动，异常退出可自恢复"),
]
textbox(s, 0.98, 1.78, 2.4, 0.25, "现象", 9.5, True, MUTED)
textbox(s, 4.05, 1.78, 3.9, 0.25, "定位", 9.5, True, MUTED)
textbox(s, 8.25, 1.78, 3.9, 0.25, "修复", 9.5, True, MUTED)

for i, (a, b, c, d) in enumerate(rows):
    y = 2.12 + i * 1.4
    shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, 0.75, y, 11.83, 1.18, CARD, BORDER, 1.0, 0.07)
    shape(s, MSO_SHAPE.RECTANGLE, 0.75, y, 0.06, 1.18, TEAL if i != 1 else ORANGE)
    textbox(s, 1.0, y + 0.2, 2.5, 0.4, a, 12, True, NAVY)
    textbox(s, 4.05, y + 0.2, 3.9, 0.8, b, 9.8, False, MUTED)
    textbox(s, 8.25, y + 0.18, 4.0, 0.55, c, 9.8, False, TEXT)
    textbox(s, 8.25, y + 0.66, 4.0, 0.3, d, 8.6, False, TEAL_DARK)

textbox(s, 0.75, 6.45, 11.5, 0.3, "排错方法：看日志 → 查数据 → 稳定复现 → 验证修复，而不是靠猜。", 10.5, True, NAVY2)
notes(s, "分享三个真实问题：中文乱码是字符集双重编码；赛程 500 是空字符串仍被日期解析；"
         "启动失败是端口占用和健康检查过早。每个问题都是先看日志和数据，再验证修复。")

# 9 成果
s = new_slide(prs)
header(s, "10 / 成果与展望", "当前成果与下一步")
kpis = [("9", "张数据表"), ("68", "个接口"), ("16", "个页面"), ("10", "条报名数据")]
for i, (n, label) in enumerate(kpis):
    x = 0.75 + i * 3.0
    textbox(s, x, 1.95, 2.4, 0.7, n, 34, True, TEAL_DARK if i % 2 else NAVY)
    textbox(s, x, 2.68, 2.5, 0.3, label, 10.5, False, MUTED)

shape(s, MSO_SHAPE.RECTANGLE, 0.75, 3.25, 5.7, 0.02, BORDER)
shape(s, MSO_SHAPE.RECTANGLE, 6.88, 3.25, 5.7, 0.02, BORDER)

textbox(s, 0.75, 3.45, 5.5, 0.3, "已完成", 13, True, NAVY)
done = ["8 大功能模块与三类角色权限", "成绩 Excel 导入导出与奖牌统计", "ECharts 统计图表与个人中心", "Docker Compose 一键部署"]
for i, d in enumerate(done):
    y = 3.85 + i * 0.5
    shape(s, MSO_SHAPE.OVAL, 0.8, y + 0.12, 0.09, 0.09, TEAL)
    textbox(s, 1.0, y, 5.2, 0.35, d, 10.2, False, TEXT)

textbox(s, 6.88, 3.45, 5.5, 0.3, "下一步", 13, True, NAVY)
nexts = ["移动端 / 小程序，扫码报名", "站内消息与报名审核提醒", "成绩公示、证书与导出模板", "云服务器部署、备份与监控"]
for i, d in enumerate(nexts):
    y = 3.85 + i * 0.5
    shape(s, MSO_SHAPE.OVAL, 6.93, y + 0.12, 0.09, 0.09, ORANGE)
    textbox(s, 7.13, y, 5.2, 0.35, d, 10.2, False, TEXT)

shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, 0.75, 5.95, 11.83, 0.72, PALE_NAVY, None, 1.0, 0.2)
textbox(s, 1.05, 6.12, 11.2, 0.35, "从“能跑”到“好用”，系统已经具备完整演示和继续迭代的基础。", 12, True, NAVY2)
notes(s, "目前系统有 9 张表、68 个接口、16 个页面，功能闭环已经完整，也做了导入导出和奖牌统计。"
         "下一步可以向移动端、消息提醒、成绩公示和云端部署扩展。")

# 10 结尾
s = new_slide(prs)
shape(s, MSO_SHAPE.RECTANGLE, 0, 0, SW, SH, NAVY)
shape(s, MSO_SHAPE.OVAL, -1.3, 4.6, 4.2, 4.2, None, RGBColor(0x1E, 0x4A, 0x6B), 1.5)
shape(s, MSO_SHAPE.OVAL, 11.0, -1.0, 3.2, 3.2, None, RGBColor(0x1E, 0x4A, 0x6B), 1.2)
textbox(s, 0.9, 2.55, 8.0, 0.9, "谢谢", 52, True, WHITE)
textbox(s, 0.95, 3.62, 8.0, 0.45, "欢迎老师和同学提问", 18, False, RGBColor(0xC7, 0xD2, 0xE0))
shape(s, MSO_SHAPE.RECTANGLE, 0.95, 4.35, 1.1, 0.06, TEAL)
textbox(s, 0.95, 4.65, 8.5, 0.3, "演示地址  http://localhost:3000", 11, False, RGBColor(0x94, 0xA3, 0xB8))
textbox(s, 0.95, 5.0, 9.0, 0.3, "项目源码  github.com/MidFlowers-1337/Sports-Events", 11, False, RGBColor(0x94, 0xA3, 0xB8))
notes(s, "我的汇报到这里，谢谢大家，欢迎提问。")

out = r"C:\Users\Administrator\Documents\Codex\2026-11-02\ju\outputs\Sports-Events\presentation\校园体育赛事管理系统-汇报-v3.pptx"
prs.save(out)
print("saved:", out)
print("slides:", len(prs.slides))
