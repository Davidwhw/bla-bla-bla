import os
import time
from huggingface_hub import snapshot_download
from huggingface_hub.utils import HfHubHTTPError

# 配置镜像站加速（可选）
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

# 重试逻辑配置
MAX_RETRIES = 20  # 最大重试次数（可设置为 None 表示无限重试）
RETRY_DELAY = 60  # 429 错误重试间隔（秒）

def download_dataset(repo_id, local_dir):
    attempts = 0

    while True:
        try:
            snapshot_download(
                repo_id=repo_id,
                repo_type="dataset",
                local_dir=local_dir,
                local_dir_use_symlinks=False,
                resume_download=True,  # 启用断点续传[2,7](@ref)
                max_workers=4,        # 控制并发下载线程数
                etag_timeout=30       # 增加元数据请求超时时间
            )
            print("下载完成！")
            break

        except HfHubHTTPError as e:
            if e.response.status_code == 429:  # 处理速率限制
                print(f"触发速率限制，将在 {RETRY_DELAY} 秒后重试...")
                time.sleep(RETRY_DELAY)
                attempts += 1
                if MAX_RETRIES and attempts >= MAX_RETRIES:
                    raise RuntimeError(f"已达到最大重试次数 {MAX_RETRIES}")
                continue
            else:
                raise  # 其他错误直接抛出

        except Exception as e:
            print(f"未知错误: {str(e)}")
            raise

if __name__ == "__main__":
    repo_id = "Timbrt/MuLMS-Img"
    local_dir = "./MuLMS-Img"
    download_dataset(repo_id, local_dir)