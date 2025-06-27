def save_to_jsonl(data_list, file_path, mode='w', ensure_ascii=True, encoding='utf-8'):
    if not isinstance(data_list, list):
        raise TypeError("输入数据必须是字典列表")
    
    if mode not in ['w', 'a']:
        raise ValueError("模式参数必须是'w'或'a'")
    
    written_count = 0
    try:
        with open(file_path, mode, encoding=encoding) as f:
            for item in data_list:
                # 验证元素是否为字典类型
                if not isinstance(item, dict):
                    raise TypeError(f"列表元素必须是字典类型，发现 {type(item)}")
                
                # 序列化并写入单行JSON
                json_line = json.dumps(item, ensure_ascii=ensure_ascii)
                f.write(json_line + '\n')
                written_count += 1
        print(f"成功写入 {written_count} 条记录到 {file_path}")
        return written_count
        
    except Exception as e:
        print(f"写入文件失败: {e}")
        return 0

def read_jsonl(file_path, return_type="list", encoding="utf-8", error_handling="skip"):
    def process_line(line):
        stripped = line.strip()
        if not stripped:  # 跳过空行
            return None
        try:
            return json.loads(stripped)
        except json.JSONDecodeError as e:
            if error_handling == "raise":
                raise ValueError(f"JSON解析失败 (行: {line})") from e
            elif error_handling == "replace":
                return None
            return None  # 默认跳过

    if return_type == "generator":
        def stream_generator():
            with open(file_path, "r", encoding=encoding) as f:
                for line in f:
                    result = process_line(line)
                    if result is not None:
                        yield result
        return stream_generator()
    
    elif return_type == "list":
        data = []
        with open(file_path, "r", encoding=encoding) as f:
            for line in f:
                result = process_line(line)
                if result is not None:
                    data.append(result)
        return data
    
    else:
        raise ValueError("无效返回类型: 仅支持 'list' 或 'generator'")
