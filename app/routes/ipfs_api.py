import os

from flask import Blueprint, request

from app.annotations.permissionAnnot import permission_required
from app.config import config
from app.consts.IPFS import IPFSConsts
from app.consts.Permissions import Permissions
from app.models.response import ResponseModel
from app.service.ipfsService import IPFSService

ipfs_bp = Blueprint('ipfs', __name__)

IPFSService_ = IPFSService(config=config[os.getenv('FLASK_ENV', 'default')])


def allowed_file(filename):
    """检查文件扩展名是否允许上传"""
    allowed_extensions = config[os.getenv('FLASK_ENV', 'default')].UPLOAD_ALLOWED_EXTENSIONS
    if not allowed_extensions:  # 如果没有设置允许的扩展名，则允许所有类型
        return True
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowed_extensions


@ipfs_bp.post('/upload')
@permission_required(Permissions.FILE_UPLOAD.get('permission_name'), True)
def upload_file():
    """
    单个文件上传路由
    """
    if 'file' not in request.files:
        return ResponseModel.fail(msg=IPFSConsts.FILE_NOT_FOUND).to_dict(), 200
    file = request.files['file']
    if not allowed_file(file.filename):
        return ResponseModel.fail(IPFSConsts.FILE_NOT_ALLOWED).to_dict(), 200
    # 获得可选参数 directory
    directory = request.form.get('directory')
    add_timestamp = request.form.get('add_timestamp', type=bool, default=True)
    result = IPFSService_.upload_file(file, file.filename, directory=directory, add_timestamp=add_timestamp)
    if result['success']:
        return ResponseModel.success(msg=IPFSConsts.FILE_UPLOAD_SUCCESS, data=result).to_dict(), 200
    else:
        return ResponseModel.fail(msg=IPFSConsts.FILE_UPLOAD_ERROR, data=result).to_dict(), 200


@ipfs_bp.post('/upload/multiple')
@permission_required(Permissions.FILE_UPLOAD.get('permission_name'), True)
def upload_multiple_files():
    """
    批量上传
    """
    if 'files' not in request.files:
        return ResponseModel.fail(msg=IPFSConsts.FILE_NOT_FOUND).to_dict(), 200
    files = request.files.getlist('files')
    if not files or all(file.filename == '' for file in files):
        return ResponseModel.fail(msg=IPFSConsts.FILE_NOT_FOUND).to_dict(), 200
    valid_files = []
    invalid_files = []
    for file in files:
        if file.filename != '':
            if allowed_file(file.filename):
                valid_files.append(file)
            else:
                invalid_files.append(file.filename)
    if not valid_files:
        return ResponseModel.fail(IPFSConsts.FILE_NOT_ALLOWED).to_dict(), 200
    directory = request.form.get('directory')
    parallel = request.form.get('parallel', type=bool, default=True)
    add_timestamp = request.form.get('add_timestamp', type=bool, default=True)
    # 上传到ipfs
    results = IPFSService_.upload_multiple_files(valid_files, directory, parallel, add_timestamp)
    success_count = sum(1 for r in results if r.get('success'))
    failed_count = len(results) - success_count + len(invalid_files)
    data = {
        'success': success_count > 0,
        'total': len(results) + len(invalid_files),
        'successful': success_count,
        'failed': failed_count,
        'results': results
    }
    if invalid_files:
        data['invalid_files'] = invalid_files
    return ResponseModel.success(IPFSConsts.FILE_UPLOAD_SUCCESS, data=data).to_dict(), 200
