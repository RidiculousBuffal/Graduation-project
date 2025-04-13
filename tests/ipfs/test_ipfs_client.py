import os

import pytest

from app.ipfs.Client import IPFSClient

"""
1. 初始化IPFS客户端完成

2. 带宽统计: {'TotalIn': 56160568, 'TotalOut': 17767380, 'RateIn': 30.628348169067877, 'RateOut': 0.5259654571832544}

3. 上传图片到IPFS根目录...
   上传成功! CID: QmX2E4AVG7e2Hu5bgYVHuEFodxQh7DYj9ThR1n3DxR6bhD
   MFS路径: /basepic1.png
   文件名: basepic1.png

4. 创建MFS目录...
   目录创建成功: /test_dir

5. 列出根目录文件...
   根目录文件列表: [{'Name': 'basepic1.png', 'Type': 0, 'Size': 0, 'Hash': ''}, {'Name': 'image-annotation.zip', 'Type': 0, 'Size': 0, 'Hash': ''}, {'Name': 'lingxi-export.png', 'Type': 0, 'Size': 0, 'Hash': ''}, {'Name': 'preview_d4b726ee-c18f-4ede-9526-d9ff6e90cd12.JPEG', 'Type': 0, 'Size': 0, 'Hash': ''}, {'Name': 'test_dir', 'Type': 0, 'Size': 0, 'Hash': ''}, {'Name': 'test_image.png', 'Type': 0, 'Size': 0, 'Hash': ''}, {'Name': '过程考核 - 复习--实操 V2.0 (1).doc', 'Type': 0, 'Size': 0, 'Hash': ''}]

6. 复制图片到新目录...
   复制完成: 已将 /basepic1.png 复制到 /test_dir/basepic1.png

7. 获取文件状态...
   文件状态: {'Hash': 'QmX2E4AVG7e2Hu5bgYVHuEFodxQh7DYj9ThR1n3DxR6bhD', 'Size': 3163261, 'CumulativeSize': 3164076, 'Blocks': 13, 'Type': 'file'}

8. 获取文件下载URL...
   下载URL: http://127.0.0.1:8080/ipfs/QmX2E4AVG7e2Hu5bgYVHuEFodxQh7DYj9ThR1n3DxR6bhD?filename=basepic1.png
"""
@pytest.mark.skip(reason='已测试过,正常')
def test_ipfs_client():
    """测试IPFS客户端的所有功能"""
    TEST_IMAGE = r'E:\codes\large_passenger_aircraft\tests\ipfs\basepic1.png'

    # 初始化客户端 - 注意修正了URL协议
    client = IPFSClient(
        host="http://127.0.0.1",
        port=10503,  # 使用你的Docker端口
        gateway_host='http://127.0.0.1',
        gate_way_port=8080  # Gateway端口
    )

    print("1. 初始化IPFS客户端完成\n")

    # 测试基本带宽状态API
    try:
        bw_stats = client.stats_bw()
        print(f"2. 带宽统计: {bw_stats}\n")
    except Exception as e:
        print(f"获取带宽统计失败: {e}")

    # 测试上传图片到IPFS
    try:
        print("3. 上传图片到IPFS根目录...")
        upload_result = client.webui_upload(TEST_IMAGE)
        print(f"   上传成功! CID: {upload_result['ipfs_cid']}")
        print(f"   MFS路径: {upload_result['mfs_path']}")
        print(f"   文件名: {upload_result['filename']}\n")
    except Exception as e:
        print(f"上传失败: {e}")
        return

    # 测试创建目录
    try:
        print("4. 创建MFS目录...")
        client.create_directory("/test_dir")
        print("   目录创建成功: /test_dir\n")
    except Exception as e:
        print(f"创建目录失败: {e}")

    # 测试列出文件
    try:
        print("5. 列出根目录文件...")
        files = client.list_files("/")
        print(f"   根目录文件列表: {files}\n")
    except Exception as e:
        print(f"列出文件失败: {e}")

    try:
        print("6. 复制图片到新目录...")
        # 获取文件名而不是使用完整路径
        filename = os.path.basename(TEST_IMAGE)
        client.files_cp(f"/{filename}", f"/test_dir/{filename}")
        print(f"   复制完成: 已将 /{filename} 复制到 /test_dir/{filename}\n")
    except Exception as e:
        print(f"复制文件失败: {e}")

    # 测试获取文件状态
    try:
        print("7. 获取文件状态...")
        file_stat = client.files_stat(f"/test_dir/{filename}")
        print(f"   文件状态: {file_stat}\n")
    except Exception as e:
        print(f"获取文件状态失败: {e}")

    # 测试获取下载URL
    try:
        print("8. 获取文件下载URL...")
        download_url = client.get_download_url(f"/test_dir/{filename}")
        print(f"   下载URL: {download_url}\n")
    except Exception as e:
        print(f"获取下载URL失败: {e}")
    print("所有测试完成!")


if __name__ == "__main__":
    test_ipfs_client()
