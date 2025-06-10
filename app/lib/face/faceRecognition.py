import base64
from typing import Union

import cv2
import numpy as np
from insightface.app import FaceAnalysis
from weaviate.collections.classes.config import Configure, Property, DataType
from weaviate.collections.classes.grpc import MetadataQuery

from app.lib.vector.weaviate import WeaviateClient


class FaceRecognition:
    app = FaceAnalysis()

    def __init__(self):
        client = WeaviateClient()
        self.app.prepare(ctx_id=0)
        #     weaviate连接器
        client = client.getClient()
        if not client.collections.exists("Face"):
            client.collections.create("Face", vectorizer_config=[
                Configure.NamedVectors.none(
                    name='face_vector',
                    vector_index_config=Configure.VectorIndex.hnsw()
                )
            ], properties=[
                Property(name='uuid', data_type=DataType.UUID)
            ])
        client.close()

    def face_embedding(self, data: Union[str, bytes, object]) -> np.ndarray:
        """
        data: 可以是图片路径(str)、base64字符串(str)、文件类(BinaryIO)、bytes
        """
        # 图片路径
        if isinstance(data, str) and not data.strip().startswith(('data:', '/9j/')):
            img = cv2.imread(data)
        # base64 字符串
        elif isinstance(data, str):
            img_bytes = base64.b64decode(data.split(',')[-1])
            img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
        # 文件类或 bytes
        elif hasattr(data, 'read'):
            img_bytes = np.asarray(bytearray(data.read()), dtype=np.uint8)
            img = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)
        elif isinstance(data, bytes):
            img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
        else:
            raise ValueError('Unsupported input type for face_embedding()')

        faces = self.app.get(img)
        if not faces:
            raise ValueError('No face found!')
        return faces[0].embedding

    def delete_embedding(self, uuid):
        client = WeaviateClient()
        client = client.getClient()
        face = client.collections.get('Face')
        try:
            face.data.delete_by_id(uuid)
        except Exception as e:
            pass
        client.close()
        return True

    def put_embedding_to_weaviate(self, embeddings, uuid):
        client = WeaviateClient()
        client = client.getClient()
        face = client.collections.get('Face')
        try:
            uuid = face.data.insert(
                properties={'uuid': uuid},
                uuid=uuid,
                vector=embeddings
            )
        except Exception as e:
            uuid = face.data.update(
                properties={'uuid': uuid},
                uuid=uuid,
                vector=embeddings
            )
        finally:
            client.close()
        return uuid

    def search(self, embeddings):
        client = WeaviateClient()
        client = client.getClient()
        face = client.collections.get('Face')
        response = face.query.near_vector(
            near_vector=embeddings,
            limit=3,
            distance=0.20,
            return_metadata=MetadataQuery(distance=True),
        )
        client.close()
        return response

    def check(self, embeddings, uuid):
        client = WeaviateClient()
        client = client.getClient()
        res = self.search(embeddings).objects
        if res and res.objects and isinstance(res.objects, list):
            for o in res.objects:
                u = o.get('uuid')
                if u == uuid:
                    return True
        return False

    def check_without_uuid(self, embeddings):
        client = WeaviateClient()
        client = client.getClient()
        res = self.search(embeddings).objects
        if res and res.objects and isinstance(res.objects, list):
            for o in res.objects:
                return o.get('uuid')
        return None


frc = FaceRecognition()
