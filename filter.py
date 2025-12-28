import json
import os

def check_for_new_items(source_file, existing_cleaned_file, output_new_items_file):
    if not os.path.exists(source_file):
        print(f"错误: 找不到 {source_file}")
        return

    existing_names = set()
    if os.path.exists(existing_cleaned_file):
        try:
            with open(existing_cleaned_file, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
                for category in existing_data.values():
                    if isinstance(category, list):
                        for item in category:
                            if "name" in item:
                                existing_names.add(item["name"])
            print(f"文件已加载: {existing_cleaned_file} 包含 {len(existing_names)} 个物品。")
        except Exception as e:
            print(f"读取文件出错: {e}")
            return
    else:
        print(f"找不到 {existing_cleaned_file}。重新清洗。")

    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            source_data = json.load(f)
    except Exception as e:
        print(f"读取文件出错: {e}")
        return

    raw_items = source_data.get("m_Structure", {}).get("items", [])
    
    new_entries = {
        "Keys": [],
        "Codex": [],
        "Keycards": [],
        "Collectables": []
    }
    
    new_item_count = 0

    for item in raw_items:
        name = item.get("name", "")
        id_str = item.get("idStr", "")
        
        if name.startswith("Stat_"): continue
        if name.startswith("Equipment_"): continue
        if name == "Codex": continue
        if name == "Flashlight": continue
        if name == "Backpack": continue

        if name in existing_names:
            continue
        
        processed_item = {
            "name": name,
            "idStr": id_str,
            "stackCapacity": 99,
            "imgPath": f"{name}.png"
        }

        if name.startswith("Key_"):
            if name == "Key_ScrewDriver":
                new_entries["Collectables"].append(processed_item)
            else:
                new_entries["Keys"].append(processed_item)
        elif name.startswith("Codex_"):
            new_entries["Codex"].append(processed_item)
        elif name.startswith("Keycard_"):
            new_entries["Keycards"].append(processed_item)
        else:
            new_entries["Collectables"].append(processed_item)
        
        new_item_count += 1

    if new_item_count > 0:
        with open(output_new_items_file, 'w', encoding='utf-8') as f:
            json.dump(new_entries, f, indent=4, ensure_ascii=False)
        print(f"发现 {new_item_count} 个新物品。")
        print(f"已保存至: {output_new_items_file}")
    else:
        print("没有发现任何新物品。")

if __name__ == "__main__":
    SOURCE_FILE = "InventoryItemManager.json" 
    BASE_FILE = "Inventory_Cleaned.json"      
    OUTPUT_FILE = "Inventory_New_Entries.json" 

    check_for_new_items(SOURCE_FILE, BASE_FILE, OUTPUT_FILE)