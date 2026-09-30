import sys
sys.dont_write_bytecode = True

import json
from pathlib import Path

CHANGES_FILE = Path('changes.json')
with open(CHANGES_FILE, 'r', encoding='utf-8') as f:
    changes_json = json.load(f)

# 支持通过 "includes" 引用外部 JSON 文件, 各模块的改动列表会按引用顺序追加到主文件之后
_INCLUDE_MODULES = ("effect_adjustments", "unit_copies", "unit_changes", "tech_changes", "resource_changes", "tech_tree_changes")
for include_path in changes_json.get("includes", []):
    include_file = Path(include_path)
    if not include_file.is_absolute():
        include_file = CHANGES_FILE.parent / include_file
    with open(include_file, 'r', encoding='utf-8') as f:
        included_json = json.load(f)
    for module in _INCLUDE_MODULES:
        if module in included_json:
            changes_json.setdefault(module, []).extend(included_json[module])


def _entry_ids(item):
    """展开单个条目的 id 为整数列表"""
    raw = item['id']
    if isinstance(raw, list):
        return [int(i) for i in raw]
    return [int(raw)]


copy_from_old = changes_json.get("copy_from_old_datafile", {})

# copy_dict: 拷贝自旧数据文件的所有 id 列表 (保持原顺序, 用于 copyFromOldVersion)
# lock_dict: 带有 "lock": true 标记的条目对应的 id 集合, 这些 id 不受后续 customChanges 中任何 apply*Changes 修改的影响
copy_dict = {}
lock_dict = {}
for _key in ["unit_list", "tech_list", "effect_list", "resource_list"]:
    _entries = copy_from_old.get(_key, [])
    copy_dict[_key] = [i for item in _entries for i in _entry_ids(item)]
    lock_dict[_key] = {i for item in _entries if item.get("lock", False) for i in _entry_ids(item)}


effect_change_list = changes_json["effect_adjustments"]
unit_copy_change_list = changes_json.get("unit_copies", [])
unit_change_list = changes_json["unit_changes"]
tech_change_list = changes_json["tech_changes"]
resource_change_list = changes_json["resource_changes"]
tech_tree_change_list = changes_json.get("tech_tree_changes", [])

changes_json = None
