import os
import urllib.parse
import requests


class IPFSClient:
    """
    A comprehensive Python client for the IPFS API.
    """

    def __init__(self, host="127.0.0.1", port=5001, base_path="/api/v0", gateway_host='127.0.0.1', gate_way_port=8080,
                 session=None):
        """
        Initialize the IPFS client.
        """
        # 确保URL包含协议前缀
        if not host.startswith(('http://', 'https://')):
            host = f"http://{host}"
        if not gateway_host.startswith(('http://', 'https://')):
            gateway_host = f"http://{gateway_host}"
        if host.startswith("https://"):
            self.api_url = f'''{host}{base_path}'''
        else:
            self.api_url = f"{host}:{port}{base_path}"
        self.gateway = f'{gateway_host}/ipfs' if gateway_host.startswith(
            'https://') else f'{gateway_host}:{gate_way_port}/ipfs'
        self.session = session or requests.Session()

    def _make_request(self, command, files=None, params=None, data=None, method='post'):
        """
        Make a request to the IPFS API.
        """
        url = f"{self.api_url}/{command}"

        # 处理参数，特别是处理arg参数为列表的情况
        final_params = []
        if params:
            for key, value in params.items():
                if key == 'arg' and isinstance(value, list):
                    # 对于arg参数是列表的情况，将其转换为多个(key, value)对
                    for v in value:
                        final_params.append((key, v))
                else:
                    final_params.append((key, value))

        # 发送请求
        if method.lower() == 'post':
            response = self.session.post(url, files=files, params=final_params, data=data)
        else:
            response = self.session.get(url, params=final_params)

        # 处理错误
        if response.status_code >= 400:
            try:
                error_message = response.json().get('Message', response.text)
            except ValueError:
                error_message = response.text
            raise Exception(f"IPFS API error ({response.status_code}): {error_message}")

        # 处理响应内容
        content_type = response.headers.get('Content-Type', '')
        if 'json' in content_type:
            try:
                return response.json()
            except ValueError:
                # 如果响应不是有效的JSON或为空，返回空字典
                if not response.content:
                    return {}
                raise
        else:
            if 'octet-stream' in content_type or 'text/plain' in content_type:
                return response.content
            return {"Text": response.text}

    def _prepare_file(self, file_path_or_obj):
        """
        Prepare a file for upload.
        """
        if isinstance(file_path_or_obj, str) and os.path.isfile(file_path_or_obj):
            return open(file_path_or_obj, 'rb')
        elif isinstance(file_path_or_obj, (bytes, bytearray)):
            import io
            return io.BytesIO(file_path_or_obj)
        else:
            return file_path_or_obj

    def stats_bw(self):
        """
        Get bandwidth statistics.
        """
        return self._make_request('stats/bw')

    def add(self, file_path_or_obj, **kwargs):
        """
        Add file to IPFS.
        """
        params = kwargs
        file_obj = self._prepare_file(file_path_or_obj)
        files = {
            'file': (os.path.basename(file_path_or_obj) if isinstance(file_path_or_obj, str) else 'file', file_obj)}
        response = self._make_request('add', files=files, params=params)

        # Close the file if we opened it
        if isinstance(file_path_or_obj, str):
            file_obj.close()

        return response

    def files_cp(self, source, destination):
        """
        Copy files within MFS or from IPFS to MFS.

        使用直接请求方式，确保正确处理多参数
        """
        url = f"{self.api_url}/files/cp"
        # 使用元组列表确保多参数正确传递
        params = [('arg', source), ('arg', destination)]
        response = self.session.post(url, params=params)

        if response.status_code >= 400:
            try:
                error_message = response.json().get('Message', response.text)
            except ValueError:
                error_message = response.text
            raise Exception(f"IPFS API error ({response.status_code}): {error_message}")

        # 大多数情况下，files/cp成功时返回空内容
        if not response.content:
            return {}

        try:
            return response.json()
        except ValueError:
            return {"Text": response.text}

    def files_stat(self, path="/"):
        """
        Get file or directory status.
        """
        params = {"arg": path}
        return self._make_request('files/stat', params=params)

    def ls(self, path):
        """
        List directory contents.
        """
        params = {"arg": path}
        return self._make_request('ls', params=params)

    def webui_upload(self, file_path, mfs_destination=None):
        """
        Upload a file following the WebUI workflow to preserve filename.
        """
        # Step 1: Get bandwidth stats (like WebUI does)
        self.stats_bw()

        # Step 2: Add the file to IPFS without pinning or wrapping
        filename = os.path.basename(file_path)
        add_result = self.add(file_path, **{
            'stream-channels': 'true',
            'pin': 'false',
            'wrap-with-directory': 'false',
            'progress': 'false'
        })

        # Extract the CID from the response
        ipfs_cid = add_result.get('Hash')
        if not ipfs_cid:
            raise Exception("Failed to get Hash from IPFS add response")

        # Step 3: Copy the file to MFS preserving the filename
        if mfs_destination is None:
            mfs_path = f"/{filename}"
        else:
            # If destination ends with /, append filename
            if mfs_destination.endswith('/'):
                mfs_path = f"{mfs_destination}{filename}"
            else:
                mfs_path = mfs_destination

        # URL encode the MFS path to handle special characters (如果路径包含中文或特殊字符)
        ipfs_path = f"/ipfs/{ipfs_cid}"

        # Copy from IPFS to MFS - 这里使用修复后的files_cp方法
        self.files_cp(ipfs_path, mfs_path)

        # Step 4: Check MFS root status
        try:
            mfs_stat = self.files_stat("/")
        except Exception:
            mfs_stat = {}

        # Step 5: List the content (optional)
        try:
            ls_result = self.ls(ipfs_cid)
        except Exception:
            ls_result = {}

        # Return comprehensive information
        return {
            'filename': filename,
            'ipfs_cid': ipfs_cid,
            'ipfs_path': ipfs_path,
            'mfs_path': mfs_path,
            'add_result': add_result,
            'ls_result': ls_result
        }

    def create_directory(self, path):
        """创建MFS目录"""
        params = {"arg": path, "parents": "true"}
        return self._make_request('files/mkdir', params=params)

    def list_files(self, path="/"):
        """列出MFS中的文件和目录"""
        params = {"arg": path}
        response = self._make_request('files/ls', params=params)
        return response.get('Entries', [])

    def move_file(self, source, destination):
        """在MFS中移动文件或目录"""
        # 处理多参数的情况
        url = f"{self.api_url}/files/mv"
        params = [('arg', source), ('arg', destination)]
        response = self.session.post(url, params=params)

        if response.status_code >= 400:
            try:
                error_message = response.json().get('Message', response.text)
            except ValueError:
                error_message = response.text
            raise Exception(f"IPFS API error ({response.status_code}): {error_message}")

        if not response.content:
            return {}

        try:
            return response.json()
        except ValueError:
            return {"Text": response.text}

    def remove_file(self, path, recursive=False):
        """从MFS中删除文件或目录"""
        params = {"arg": path, "recursive": str(recursive).lower()}
        return self._make_request('files/rm', params=params)

    def read_file(self, path):
        """读取MFS中的文件内容"""
        params = {"arg": path}
        return self._make_request('files/read', params=params)

    def get_download_url(self, path):
        """获取文件的临时下载URL (通过HTTP网关)"""
        # 获取文件的CID
        stat = self.files_stat(path)
        cid = stat.get('Hash')
        if not cid:
            raise Exception(f"Failed to get hash for path: {path}")

        # 构建网关URL
        gateway_url = f"{self.gateway}/{cid}"

        # 添加文件名参数以确保下载时保留文件名
        filename = os.path.basename(path)
        download_url = f"{gateway_url}?filename={urllib.parse.quote(filename)}"

        return download_url