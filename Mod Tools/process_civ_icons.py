#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 Mod Tools 下的七国 AI 勋章 JPG 处理为 104x104 文明图标。

默认只输出 wpfg 层 (当前启用):
  resources/_common/wpfg/resources/civ_techtree/ezs_techtree_{拼音}.png (+_hover/_pressed)
  经 civilizations.json 的 tech_tree_image_path 引用; 用 ezs_ 前缀避免与原版文件名冲突
  (如三国魏占用 menu_techtree_wei.png)。

加 --with-widgetui 参数时额外输出 widgetui 两层:
  widgetui/textures/ingame/icons/civ_techtree_buttons/menu_techtree_{ezs名}.png (+_hover/_pressed)
    游戏内科技树按钮。文件名使用 civilizations.json 中新的 internal_name 小写 (如 ezsqi),
    不覆盖原版文明文件; 对应的 MaterialDef 由 Civ Icons Materials Editor.py 注入 materials.json。
  widgetui/textures/menu/civs/{ezs名}.png
    大厅文明选择菜单图标 (只有普通版)。

hover 提亮 10% / pressed 压暗 10%, 与原版变体方向一致。
泛洪填充去黑底: 封闭在勋章内部的深色区域 (如秦的黑色底) 不会被误删。
"""
import sys

sys.dont_write_bytecode = True

import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance

TEMP = Path(__file__).resolve().parent
ROOT = TEMP.parent

# 中文名 -> (拼音, 被替换的原版文明文件名, EZS internal_name 小写)
CIVS = {
    "齐": ("qi", "jurchens", "ezsqi"),
    "秦": ("qin", "chinese", "ezsqin"),
    "韩": ("han", "koreans", "ezshan"),
    "魏": ("wei", "teutons", "ezswei"),
    "赵": ("zhao", "mongols", "ezszhao"),
    "楚": ("chu", "goths", "ezschu"),
    "燕": ("yan", "japanese", "ezsyan"),
    "吴": ("wu", "vikings", "ezswu"),
    "越": ("yue", "malay", "ezsyue"),
}

MAGIC = (255, 0, 255)  # 泛洪填充用的背景标记色 (勋章图中不存在品红)
BG_THRESH = 50  # 与种点的最大色差, 覆盖 JPEG 压缩噪点

ICON_SIZE = 104

OUT_TECHTREE = ROOT / "resources" / "_common" / "wpfg" / "resources" / "civ_techtree"
OUT_INGAME_BTNS = ROOT / "widgetui" / "textures" / "ingame" / "icons" / "civ_techtree_buttons"
OUT_MENU_CIVS = ROOT / "widgetui" / "textures" / "menu" / "civs"


def foreground_mask(src: Image.Image):
    """四周泛洪把纯黑背景填成品红, 返回 (前景蒙版L, 前景bbox)"""
    work = src.copy()
    w, h = work.size
    seeds = [
        (0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1),
        (w // 2, 0), (w // 2, h - 1), (0, h // 2), (w - 1, h // 2),
    ]
    for s in seeds:
        if work.getpixel(s) != MAGIC:
            ImageDraw.floodfill(work, s, MAGIC, thresh=BG_THRESH)
    arr = np.array(work)
    fg = ~np.all(arr == MAGIC, axis=-1)
    mask = Image.fromarray((fg * 255).astype(np.uint8), "L")
    return mask, mask.getbbox()


def make_icon(src: Image.Image, mask: Image.Image, bbox) -> Image.Image:
    """104x104 彩色图标: 勋章整体等比缩放居中, 四周留 3px 透明边"""
    x0, y0, x1, y1 = bbox
    pad = 6
    box = (
        max(0, x0 - pad), max(0, y0 - pad),
        min(src.width, x1 + pad), min(src.height, y1 + pad),
    )
    art = src.crop(box).convert("RGBA")
    art.putalpha(mask.crop(box))

    aw, ah = art.size
    usable = ICON_SIZE - 2 * 3
    scale = min(usable / aw, usable / ah)
    nw, nh = max(1, round(aw * scale)), max(1, round(ah * scale))
    art = art.resize((nw, nh), Image.LANCZOS)

    canvas = Image.new("RGBA", (ICON_SIZE, ICON_SIZE), (0, 0, 0, 0))
    canvas.alpha_composite(art, ((ICON_SIZE - nw) // 2, (ICON_SIZE - nh) // 2))
    return canvas


def brightness_variant(icon: Image.Image, factor: float) -> Image.Image:
    """只调 RGB 亮度, 保持 alpha 不变"""
    r, g, b, a = icon.split()
    rgb = Image.merge("RGB", (r, g, b))
    rgb = ImageEnhance.Brightness(rgb).enhance(factor)
    return Image.merge("RGBA", (*rgb.split(), a))


def save_variants(icon: Image.Image, path_no_ext: Path):
    icon.save(path_no_ext.with_suffix(".png"))
    brightness_variant(icon, 1.10).save(path_no_ext.with_name(path_no_ext.name + "_hover.png"))
    brightness_variant(icon, 0.90).save(path_no_ext.with_name(path_no_ext.name + "_pressed.png"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--with-widgetui",
        action="store_true",
        help="额外输出游戏内科技树按钮与大厅菜单图标 (widgetui 层, 当前未启用)",
    )
    args = parser.parse_args()

    OUT_TECHTREE.mkdir(parents=True, exist_ok=True)
    if args.with_widgetui:
        for folder in (OUT_INGAME_BTNS, OUT_MENU_CIVS):
            folder.mkdir(parents=True, exist_ok=True)

    for cn_name, (pinyin, vanilla, ezs_name) in CIVS.items():
        src = Image.open(TEMP / f"{cn_name}.jpg").convert("RGB")
        mask, bbox = foreground_mask(src)
        icon = make_icon(src, mask, bbox)

        # wpfg 层 (civilizations.json tech_tree_image_path 引用)
        save_variants(icon, OUT_TECHTREE / f"ezs_techtree_{pinyin}")
        outputs = f"ezs_techtree_{pinyin}"

        if args.with_widgetui:
            # 游戏内科技树按钮 (用新 internal_name 小写, 不覆盖原版)
            save_variants(icon, OUT_INGAME_BTNS / f"menu_techtree_{ezs_name}")
            # 大厅文明选择菜单 (仅普通版)
            icon.save(OUT_MENU_CIVS / f"{ezs_name}.png")
            outputs += f" + menu_techtree_{ezs_name} + {ezs_name}.png"

        print(f"{cn_name} -> {outputs}")
    print("全部处理完成")


if __name__ == "__main__":
    main()
