import yaml
import json
import os

def unity_tag_constructor(loader, tag_suffix, node):
    if isinstance(node, yaml.ScalarNode):
        return loader.construct_scalar(node)
    elif isinstance(node, yaml.SequenceNode):
        return loader.construct_sequence(node)
    elif isinstance(node, yaml.MappingNode):
        return loader.construct_mapping(node)
    return None

yaml.SafeLoader.add_multi_constructor("tag:unity3d.com,2011:", unity_tag_constructor)

def yaml_to_json(yaml_file, json_file):
    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
        print(f"已将 {yaml_file} 转换为 {json_file}")
        
    except yaml.YAMLError as e:
        print(f"YAML 解析错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    input_yaml = "InventoryItemManager.asset"
    output_json = "InventoryItemManager.json"
    
    if os.path.exists(input_yaml):
        yaml_to_json(input_yaml, output_json)
    else:
        print(f"错误：找不到文件 {input_yaml}")