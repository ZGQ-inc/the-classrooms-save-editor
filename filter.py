import json
import os

def clean_inventory_json(input_filename, output_filename):
    # 检查输入文件是否存在
    if not os.path.exists(input_filename):
        print(f"错误: 找不到文件 {input_filename}")
        return

    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 定位到 items 列表
        raw_items = data.get("m_Structure", {}).get("items", [])
        
        # 初始化目标结构
        cleaned_data = {
            "Keys": [],
            "Codex": [],
            "Keycards": [],
            "Collectables": []
        }
        
        for item in raw_items:
            name = item.get("name", "")
            id_str = item.get("idStr", "")
            
            # --- 构建新对象 (应用新规则) ---
            simple_item = {
                "name": name,
                "idStr": id_str,
                "stackCapacity": 99,       # 强制修改为 99
                "img": f"{name}.png"   # 新增图片路径，默认 [name].png
            }
            
            # --- 1. 移除规则 (Remove) ---
            
            # 移除 Stat_ 开头
            if name.startswith("Stat_"):
                continue
                
            # 移除 Equipment_ 开头
            if name.startswith("Equipment_"):
                continue
                
            # 移除 Codex (精确匹配)
            if name == "Codex":
                continue
                
            # 移除 Flashlight (精确匹配)
            if name == "Flashlight":
                continue
                
            # 移除 Backpack (精确匹配)
            if name == "Backpack":
                continue

            # --- 2. 分类规则 (Categorize) ---
            
            # Key_ 开头处理
            if name.startswith("Key_"):
                if name == "Key_ScrewDriver":
                    # 特殊情况：Key_ScrewDriver 归入 Collectables
                    cleaned_data["Collectables"].append(simple_item)
                else:
                    # 其他 Key_ 放入 Keys
                    cleaned_data["Keys"].append(simple_item)
            
            # Codex_ 开头处理
            elif name.startswith("Codex_"):
                cleaned_data["Codex"].append(simple_item)
            
            # Keycard_ 开头处理
            elif name.startswith("Keycard_"):
                cleaned_data["Keycards"].append(simple_item)
            
            # 剩下的全部放入 Collectables
            else:
                cleaned_data["Collectables"].append(simple_item)

        # --- 写入文件 ---
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(cleaned_data, f, indent=4, ensure_ascii=False)
            
        print(f"清洗完成！文件已保存为: {output_filename}")
        print(f"统计: Keys({len(cleaned_data['Keys'])}), Codex({len(cleaned_data['Codex'])}), Keycards({len(cleaned_data['Keycards'])}), Collectables({len(cleaned_data['Collectables'])})")

    except Exception as e:
        print(f"发生错误: {e}")

# 执行脚本
if __name__ == "__main__":
    input_file = "InventoryItemManager.json"
    output_file = "Inventory_Database.json"
    clean_inventory_json(input_file, output_file)