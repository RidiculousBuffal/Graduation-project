# app/services/ipfs_service.py
import concurrent.futures
import mimetypes
import os
import tempfile
import time
import urllib.parse
import uuid
from datetime import datetime

from werkzeug.utils import secure_filename

from app.ipfs.Client import IPFSClient


class IPFSService:
    """处理IPFS相关业务逻辑的服务"""

    def __init__(self, config):
        """初始化IPFS服务"""
        self.client = IPFSClient(
            host=config.IPFS_API_HOST,
            port=config.IPFS_API_PORT,
            gateway_host=config.IPFS_GATEWAY_HOST,
            gate_way_port=config.IPFS_GATEWAY_PORT
        )

        # 是否将文件存储到MFS目录树
        self.use_mfs = config.IPFS_USE_MFS
        # MFS中的基础目录
        self.mfs_base_dir = config.IPFS_MFS_BASE_DIR
        # 并行上传的线程数
        self.max_workers = config.IPFS_MAX_UPLOAD_WORKERS
        # 时间戳格式 (可选: 'timestamp', 'datetime', 'date')
        self.timestamp_format = config.IPFS_TIMESTAMP_FORMAT

        # # 确保基础目录存在
        # if self.use_mfs:
        #     try:
        #         self.client.create_directory(self.mfs_base_dir)
        #     except Exception:
        #         pass  # 如果目录已存在，忽略错误

    def add_timestamp_to_filename(self, filename):
        """
        在文件名中加入时间戳，避免重名

        Args:
            filename: 原始文件名

        Returns:
            添加了时间戳的文件名
        """
        if not filename:
            return f"{uuid.uuid4().hex}"

        # 分离文件名和扩展名
        if '.' in filename:
            name_part, ext_part = filename.rsplit('.', 1)
            ext_part = f".{ext_part}"
        else:
            name_part = filename
            ext_part = ""

        # 根据配置生成时间戳
        if self.timestamp_format == 'datetime':
            # 格式: filename_YYYYMMDD_HHMMSS.ext
            timestamp = datetime.now().strftime("_%Y%m%d_%H%M%S")
        elif self.timestamp_format == 'date':
            # 格式: filename_YYYYMMDD.ext
            timestamp = datetime.now().strftime("_%Y%m%d")
        else:
            # 默认使用Unix时间戳: filename_1681234567.ext
            timestamp = f"_{int(time.time())}"

        # 组合新文件名
        timestamped_filename = f"{name_part}{timestamp}{ext_part}"
        return timestamped_filename

    def upload_file(self, file_obj, filename=None, directory=None, add_timestamp=True):
        """
        上传单个文件到IPFS

        Args:
            file_obj: 文件对象
            filename: 可选的文件名
            directory: MFS中的目标目录，默认使用按日期组织的目录
            add_timestamp: 是否添加时间戳避免重名

        Returns:
            包含文件信息的字典
        """
        # 处理文件名
        if filename is None:
            if hasattr(file_obj, 'filename'):
                filename = secure_filename(file_obj.filename)
            else:
                # 生成随机文件名
                ext = mimetypes.guess_extension(file_obj.content_type) if hasattr(file_obj, 'content_type') else ''
                filename = f"{uuid.uuid4().hex}{ext}"

        # 存储原始文件名(用于显示)
        original_filename = filename

        # 添加时间戳避免重名
        if add_timestamp:
            filename = self.add_timestamp_to_filename(filename)

        # 创建临时文件
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_filepath = temp_file.name

        try:
            # 将上传的文件内容写入临时文件
            if hasattr(file_obj, 'save'):
                file_obj.save(temp_filepath)
            else:
                # 如果不是Flask的FileStorage对象，尝试读取内容
                file_obj.seek(0)  # 确保从头开始读取
                with open(temp_filepath, 'wb') as f:
                    f.write(file_obj.read())

            # 上传到IPFS
            upload_result = self.client.webui_upload(temp_filepath, mfs_destination=None)

            # 获取CID
            ipfs_cid = upload_result['ipfs_cid']

            # 如果使用MFS，构建目录路径
            mfs_path = None
            if self.use_mfs:
                if directory is None:
                    # 按日期创建目录
                    today = datetime.now().strftime('%Y-%m-%d')
                    directory = f"{self.mfs_base_dir}/{today}"

                self.client.create_directory(directory)
                mfs_path = f"{directory}/{filename}"

                # 复制到MFS
                self.client.files_cp(f"/ipfs/{ipfs_cid}", mfs_path)

            # 构建下载URL (使用原始文件名作为下载文件名)
            download_url = f"{self.client.gateway}/{ipfs_cid}?filename={urllib.parse.quote(original_filename)}"

            # 获取文件大小
            file_stat = os.stat(temp_filepath)
            file_size = file_stat.st_size

            # 确定MIME类型
            mime_type, _ = mimetypes.guess_type(original_filename)
            if mime_type is None:
                mime_type = "application/octet-stream"

            # 返回完整信息
            return {
                "success": True,
                "filename": original_filename,  # 返回原始文件名用于显示
                "stored_filename": filename,  # 存储的带有时间戳的文件名
                "ipfs_cid": ipfs_cid,
                "ipfs_path": f"/ipfs/{ipfs_cid}",
                "mfs_path": mfs_path,
                "download_url": download_url,
                "size": file_size,
                "mime_type": mime_type,
                "uploaded_at": datetime.now().isoformat()
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "filename": original_filename
            }
        finally:
            # 清理临时文件
            try:
                os.unlink(temp_filepath)
            except:
                pass  # 忽略清理临时文件的错误

    def upload_multiple_files(self, files, directory=None, parallel=True, add_timestamp=True):
        """
        批量上传多个文件到IPFS

        Args:
            files: 文件对象列表 [(文件对象, 文件名), ...] 或 Flask FileStorage对象列表
            directory: MFS中的目标目录，默认使用按日期组织的目录
            parallel: 是否并行上传
            add_timestamp: 是否添加时间戳避免重名

        Returns:
            包含每个文件上传结果的列表
        """
        # 准备文件列表
        file_list = []
        for file_item in files:
            if isinstance(file_item, tuple):
                # 已经是(文件对象, 文件名)格式
                file_list.append(file_item)
            else:
                # 假设是Flask FileStorage对象
                file_list.append((file_item, secure_filename(file_item.filename)))

        if parallel and len(file_list) > 1:
            # 并行上传
            results = []
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # 创建上传任务
                future_to_file = {
                    executor.submit(
                        self.upload_file, file_obj, filename, directory, add_timestamp
                    ): (filename, file_obj)
                    for file_obj, filename in file_list
                }

                # 收集结果
                for future in concurrent.futures.as_completed(future_to_file):
                    filename, _ = future_to_file[future]
                    try:
                        result = future.result()
                        results.append(result)
                    except Exception as exc:
                        # 处理上传过程中的异常
                        results.append({
                            "success": False,
                            "error": str(exc),
                            "filename": filename
                        })

            return results
        else:
            # 串行上传
            return [self.upload_file(file_obj, filename=filename, directory=directory, add_timestamp=add_timestamp)
                    for file_obj, filename in file_list]
