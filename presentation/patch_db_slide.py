# -*- coding: utf-8 -*-
"""把 build_deck.py 中的“数据库操作”页替换成 Navicat 截图版。"""

from pathlib import Path

p = Path(r"C:\Users\Administrator\Documents\Codex\2026-11-02\ju\outputs\Sports-Events\presentation\build_deck.py")
text = p.read_text(encoding="utf-8")

start = text.index("# 6 数据库操作")
end = text.index("# 7 流程")

new_block = '''# 6 数据库操作
s = new_slide(prs)
header(s, "06 / 数据库操作", "在 Navicat 中打开并编辑这 9 张表")

NAVICAT_IMG = r"C:\\Users\\Administrator\\Documents\\Codex\\2026-11-02\\ju\\outputs\\Sports-Events\\presentation\\assets\\navicat.png"
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

'''

p.write_text(text[:start] + new_block + text[end:], encoding="utf-8")
print("patched")
