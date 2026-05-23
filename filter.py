import json
import os

def check_for_new_items(source_file, existing_cleaned_file, output_new_items_file, output_id_changed_file):
    if not os.path.exists(source_file):
        print(f"错误: 找不到 {source_file}")
        return

    existing_items_map = {} 
    
    if os.path.exists(existing_cleaned_file):
        try:
            with open(existing_cleaned_file, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
                for category in existing_data.values():
                    if isinstance(category, list):
                        for item in category:
                            if "name" in item and "idStr" in item:
                                existing_items_map[item["name"]] = item["idStr"]
            print(f"文件已加载: {existing_cleaned_file} 包含 {len(existing_items_map)} 个物品。")
        except Exception as e:
            print(f"读取文件出错: {e}")
            return
    else:
        print(f"找不到 {existing_cleaned_file}。将视作全新提取。")

    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            source_data = json.load(f)
    except Exception as e:
        print(f"读取文件出错: {e}")
        return

    raw_items = source_data.get("MonoBehaviour", {}).get("items", [])
    if not raw_items:
        raw_items = source_data.get("items", [])
    
    new_entries = {
        "Keys": [], "Codex": [], "Keycards": [], "Tapes": [], "Apparels": [], "Collectables": []
    }
    
    id_changed_entries = {
        "Keys": [], "Codex": [], "Keycards": [], "Tapes": [], "Apparels": [], "Collectables": []
    }
    
    new_item_count = 0
    id_changed_count = 0

    for item in raw_items:
        name = item.get("name", "")
        id_str = item.get("idStr", "")
        
        if not name: continue
        if name.startswith("Stat_"): continue
        if name.startswith("Equipment_"): continue
        if name in ["Codex", "Flashlight", "Backpack", "Compass"]: continue

        processed_item = {
            "name": name,
            "idStr": id_str,
            "stackCapacity": 99,
            "img": f"{name}.png"
        }

        def append_to_category(container, item_name, item_data):
            if item_name.startswith("Key_") and item_name != "Key_ScrewDriver":
                container["Keys"].append(item_data)
            elif item_name.startswith("Codex_"):
                container["Codex"].append(item_data)
            elif item_name.startswith("Keycard_"):
                container["Keycards"].append(item_data)
            elif item_name.startswith("Tape_"):
                container["Tapes"].append(item_data)
            elif item_name.startswith("Apparel_"):
                container["Apparels"].append(item_data)
            else:
                container["Collectables"].append(item_data)

        if name in existing_items_map:
            if existing_items_map[name] != id_str:
                processed_item["old_idStr"] = existing_items_map[name] 
                append_to_category(id_changed_entries, name, processed_item)
                id_changed_count += 1
            continue
        
        append_to_category(new_entries, name, processed_item)
        new_item_count += 1

    if new_item_count > 0:
        with open(output_new_items_file, 'w', encoding='utf-8') as f:
            json.dump(new_entries, f, indent=4, ensure_ascii=False)
        print(f"发现 {new_item_count} 个全新物品，已保存至: {output_new_items_file}")
    else:
        print("没有发现任何全新物品。")

    if id_changed_count > 0:
        with open(output_id_changed_file, 'w', encoding='utf-8') as f:
            json.dump(id_changed_entries, f, indent=4, ensure_ascii=False)
        print(f"发现 {id_changed_count} 个物品 ID 发生变更！已保存至: {output_id_changed_file}")
    else:
        print("没有发现任何 ID 变更的物品。")

if __name__ == "__main__":
    SOURCE_FILE = "InventoryItemManager.json" 
    BASE_FILE = "Inventory_Database.json"      
    OUTPUT_FILE = "Inventory_New_Entries.json" 
    ID_CHANGED_FILE = "Inventory_ID_Changed.json" 

    check_for_new_items(SOURCE_FILE, BASE_FILE, OUTPUT_FILE, ID_CHANGED_FILE)