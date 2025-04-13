import os

import dotenv
import pytest

from app.ipfs.Client import IPFSClient

dotenv.load_dotenv()


@pytest.mark.skip(reason='avoid duplicate upload file to IPFS')
def test_ipfs_client():
    # 初始化客户端
    host = os.getenv('IPFS_HOST')
    port = int(os.getenv('IPFS_PORT'))
    client = IPFSClient(host=host, port=port)

    try:
        # Get IPFS version info
        version = client.version()
        print(f"IPFS Version: {version['Version']}")
        result = client.add('test_image.png')
    except Exception as e:
        print(f"Error: {str(e)}")

def test_ipfs_node():
    # Get node info
    # 初始化客户端
    host = os.getenv('IPFS_HOST')
    port = int(os.getenv('IPFS_PORT'))
    client = IPFSClient(host=host, port=port)
    node_info = client.id()
    print(f"Node ID: {node_info['ID']}")
    print(f"Node addresses: {node_info['Addresses']}")
