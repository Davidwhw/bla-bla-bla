import os
import fitz
from pathlib import Path

def find_pdf_files(root_dir):
    """递归查找目录下所有PDF文件（优化路径处理）"""
    return [
        os.path.abspath(os.path.join(dirpath, filename))
        for dirpath, _, filenames in os.walk(root_dir)
        for filename in filenames
        if filename.lower().endswith('.pdf')
    ]

def is_scanned_pdf(file_path, threshold=20):
    """增强版扫描PDF检测（添加错误处理）"""
    try:
        with fitz.open(file_path) as doc:
            total_text = sum(len(page.get_text("text").strip()) for page in doc)
            return (total_text / len(doc)) < threshold if doc else False
    except Exception as e:
        print(f"文件检测失败: {file_path}\n错误信息: {str(e)}")
        return False

def save_file_list(file_list, output_path):
    """通用化保存函数（支持任意文件列表）[7](@ref)"""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(file_list))
    print(f"已保存 {len(file_list)} 个文件路径至 {os.path.abspath(output_path)}")

if __name__ == "__main__":
    # 配置参数
    SEARCH_DIR = r"C:\Users\Wanghw\Desktop\规章制度-20250427\test_total_200"
    BAD_OUTPUT = r"C:\Users\Wanghw\Desktop\unreadable_pdfs.txt"
    GOOD_OUTPUT = r"C:\Users\Wanghw\Desktop\readable_pdfs.txt"
    
    # 执行流程
    all_pdfs = find_pdf_files(SEARCH_DIR)
    print(f"发现 {len(all_pdfs)} 个PDF，开始检测可读性...")
    
    bad_files, good_files = [], []
    for idx, pdf_path in enumerate(all_pdfs, 1):
        try:
            is_bad = is_scanned_pdf(pdf_path)
            status = "不可读" if is_bad else "可读"
            
            # 动态更新分类列表
            (bad_files if is_bad else good_files).append(pdf_path)
            print(f"[{idx}/{len(all_pdfs)}] {status.ljust(4)} | {os.path.basename(pdf_path)}")
        except Exception as e:
            print(f"处理异常: {pdf_path}\n{str(e)}")
    
    # 保存双结果[6](@ref)
    save_file_list(bad_files, BAD_OUTPUT)
    save_file_list(good_files, GOOD_OUTPUT)
