import json
import os

def merge_databases(base_file, new_entries_file, output_file):
    if not os.path.exists(base_file):
        print(f"错误: 找不到基础数据库文件 {base_file}")
        return
        
    if not os.path.exists(new_entries_file):
        print(f"提示: 找不到新物品文件 {new_entries_file}，无需合并。")
        return

    try:
        with open(base_file, 'r', encoding='utf-8') as f:
            database = json.load(f)
    except Exception as e:
        print(f"读取基础数据库出错: {e}")
        return

    try:
        with open(new_entries_file, 'r', encoding='utf-8') as f:
            new_entries = json.load(f)
    except Exception as e:
        print(f"读取新物品文件出错: {e}")
        return

    total_added = 0
    new_categories_created = []

    for category, items in new_entries.items():
        if not items:
            continue

        if category not in database:
            database[category] = []
            new_categories_created.append(category)

        for item in items:
            database[category].append(item)
            total_added += 1
            print(f" [{category}] -> {item.get('name')}")

    if total_added > 0:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(database, f, indent=4, ensure_ascii=False)
            
            print(f"共把 {total_added} 个新物品合并进了数据库。")
            if new_categories_created:
                print(f"自动在数据库中创建了新的大类: {', '.join(new_categories_created)}")
            print(f"最终数据库已保存至: {output_file}")
            
            # os.remove(new_entries_file)
            
        except Exception as e:
            print(f"保存合并后的数据库时出错: {e}")
    else:
        print("没有发现需要合并的新物品。")

if __name__ == "__main__":
    BASE_DATABASE = "Inventory_Database.json"
    NEW_ENTRIES = "Inventory_New_Entries.json"
    FINAL_OUTPUT = "Inventory_Database.json"

    merge_databases(BASE_DATABASE, NEW_ENTRIES, FINAL_OUTPUT)