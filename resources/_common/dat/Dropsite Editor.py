#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Drop Site 变更处理器
支持 type: add（向 drop_site_list 添加新的 DropSite）
"""

import json
import copy
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from paths import OFFICIAL_DROPSITES_FILE, DR_CHANGES_FILE, OUTPUT_DROPSITES_FILE

os.chdir(Path(__file__).parent)


class DropSiteChangeProcessor:
    """处理 dropsites.json 的变更"""
    
    def __init__(self, base_file: str):
        self.base_data = self._load_json(base_file)
        self.changes: List[Dict[str, Any]] = []
        
    def _load_json(self, path: str) -> Dict[str, Any]:
        """加载 JSON 文件"""
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_json(self, path: str, data: Dict[str, Any]):
        """保存 JSON 文件，保持格式"""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.write('\n')
    
    def load_changes(self, changes_file: str):
        """加载变更指令"""
        with open(changes_file, 'r', encoding='utf-8') as f:
            self.changes = json.load(f)
    
    def _validate_dropsite(self, dropsite: Dict[str, Any]) -> bool:
        """验证 DropSite 结构是否合法"""
        required_fields = ['name', 'building_id']
        for field in required_fields:
            if field not in dropsite:
                raise ValueError(f"DropSite 缺少必填字段: {field}")
        
        if 'target_list' in dropsite:
            for target in dropsite['target_list']:
                if 'name' not in target or 'object_group' not in target:
                    raise ValueError(f"Target 缺少必填字段: {target}")
        
        return True
    
    def _merge_dropsite(self, existing: Dict[str, Any], new_data: Dict[str, Any]) -> Dict[str, Any]:
        """合并两个 DropSite 定义"""
        merged = copy.deepcopy(existing)
        
        if 'target_list' in new_data:
            existing_targets = {
                (t.get('name'), t.get('object_group')): t 
                for t in merged.get('target_list', [])
            }
            for new_target in new_data['target_list']:
                key = (new_target.get('name'), new_target.get('object_group'))
                if key not in existing_targets:
                    merged.setdefault('target_list', []).append(new_target)
                    existing_targets[key] = new_target
        
        if 'update_ai_resource_types' in new_data:
            existing_resources = {
                r.get('resource_type'): r 
                for r in merged.get('update_ai_resource_types', [])
            }
            for new_res in new_data['update_ai_resource_types']:
                rt = new_res.get('resource_type')
                if rt not in existing_resources:
                    merged.setdefault('update_ai_resource_types', []).append(new_res)
                    existing_resources[rt] = new_res
        
        for key, value in new_data.items():
            if key not in ['target_list', 'update_ai_resource_types']:
                merged[key] = value
        
        return merged
    
    def _find_existing_dropsite(self, building_id: int, name: Optional[str] = None) -> Optional[int]:
        """查找是否已存在相同 building_id 的 dropsite"""
        for i, ds in enumerate(self.base_data['drop_site_list']):
            if ds.get('building_id') == building_id:
                if name is None or ds.get('name') == name:
                    return i
        return None
    
    def _strip_note(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """移除 note 字段及其嵌套中的 note 字段"""
        result = {}
        for key, value in data.items():
            if key == 'note':
                continue
            if isinstance(value, dict):
                result[key] = self._strip_note(value)
            elif isinstance(value, list):
                result[key] = [
                    self._strip_note(item) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                result[key] = value
        return result
    
    def apply_add(self, change: Dict[str, Any]):
        """
        执行 add 操作
        
        参数: 一个 change 对象，包含 dropsite 的所有字段
              可选: merge_if_exists, position
              note 字段会被忽略
        """
        # 提取控制字段
        merge_if_exists = change.pop('merge_if_exists', False)
        position = change.pop('position', 'end')
        
        # 移除 note 字段
        dropsite = self._strip_note(change)
        
        self._validate_dropsite(dropsite)
        
        building_id = dropsite['building_id']
        name = dropsite.get('name')
        
        existing_idx = self._find_existing_dropsite(building_id, name)
        
        if existing_idx is not None and merge_if_exists:
            print(f"  合并现有 DropSite: {name} (ID: {building_id})")
            existing = self.base_data['drop_site_list'][existing_idx]
            merged = self._merge_dropsite(existing, dropsite)
            self.base_data['drop_site_list'][existing_idx] = merged
            
        elif existing_idx is not None and not merge_if_exists:
            print(f"  添加新变体 DropSite: {name} (ID: {building_id})")
            if position == 'end' or (isinstance(position, int) and position >= len(self.base_data['drop_site_list'])):
                self.base_data['drop_site_list'].append(dropsite)
            else:
                self.base_data['drop_site_list'].insert(position, dropsite)
                
        else:
            print(f"  添加新 DropSite: {name} (ID: {building_id})")
            if position == 'end' or (isinstance(position, int) and position >= len(self.base_data['drop_site_list'])):
                self.base_data['drop_site_list'].append(dropsite)
            else:
                self.base_data['drop_site_list'].insert(position, dropsite)
    
    def apply_change(self, change: Dict[str, Any]):
        """应用单个变更"""
        change_type = change.get('type', 'add').lower()
        
        if change_type == 'add':
            self.apply_add(change)
        else:
            raise NotImplementedError(f"不支持的操作类型: {change_type}")
    
    def process(self, output_file: str):
        """处理所有变更并保存"""
        print(f"处理 {len(self.changes)} 个变更...")
        
        for i, change in enumerate(self.changes, 1):
            print(f"[{i}/{len(self.changes)}] 类型: {change.get('type', 'add')}")
            self.apply_change(change)
        
        self._save_json(output_file, self.base_data)
        print(f"已保存到: {output_file}")
        return self.base_data


def main():
    processor = DropSiteChangeProcessor(str(OFFICIAL_DROPSITES_FILE))
    processor.load_changes(str(DR_CHANGES_FILE))
    processor.process(str(OUTPUT_DROPSITES_FILE))
    
    print(f"\n完成！新条目数: {len(processor.base_data['drop_site_list'])}")


if __name__ == "__main__":
    main()