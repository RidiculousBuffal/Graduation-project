import os

import dotenv

from app import config
from app.DTO.file import FileDTO
from app.service.ipfsService import IPFSService

dotenv.load_dotenv()
def test_ipfs_download(app):
    IPFSService_ = IPFSService(config=config[os.getenv('FLASK_ENV', 'default')])
    f = {"size": 41078, "success": True, "filename": "Sc_270.bmp",
         "ipfs_cid": "QmUT6bBPb7xckRqa1J66QW7VDtErsFKUNy517ZxAW1xk1T",
         "mfs_path": "/uploads/2025-07-13/Sc_270_1752396768.bmp",
         "ipfs_path": "/ipfs/QmUT6bBPb7xckRqa1J66QW7VDtErsFKUNy517ZxAW1xk1T", "mime_type": "image/bmp",
         "uploaded_at": "2025-07-13T08:52:48.918028",
         "download_url": "http://localhost:8080/ipfs/QmUT6bBPb7xckRqa1J66QW7VDtErsFKUNy517ZxAW1xk1T?filename=Sc_270.bmp",
         "stored_filename": "Sc_270_1752396768.bmp"}
    fileDTO = FileDTO.model_validate(f)
    path = IPFSService_.download_file(fileDTO)
    print(path)
