from uuid import uuid4

import cv2
import insightface
from weaviate.classes.config import Configure, Property, DataType
from weaviate.collections.classes.grpc import MetadataQuery

from backend.weaviateClient import WeaviateClient

weaviateClient = WeaviateClient()


def face_embedding(path):
    model = insightface.app.FaceAnalysis()
    model.prepare(ctx_id=0)
    img = cv2.imread(path)
    faces = model.get(img)
    return faces[0].embedding


def create_collection():
    client = weaviateClient.getClient()
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


def put_embedding_to_weaviate(embeddings):
    client = weaviateClient.getClient()
    face = client.collections.get('Face')
    uuid = str(uuid4())
    uuid = face.data.insert(
        properties={'uuid': uuid},
        uuid=uuid,
        vector=embeddings
    )
    client.close()
    return uuid

def search(vector):
    client = weaviateClient.getClient()
    face = client.collections.get('Face')
    response = face.query.near_vector(
        near_vector=vector,
        limit=2,
        return_metadata=MetadataQuery(distance=True),
    )
    client.close()
    return response

def main():
    embed = face_embedding('./p2.jpg')
    res = search(embed)
    for o in res.objects:
        print(o.properties)
        print(o.metadata.distance)


if __name__ == "__main__":
    # uid a16395f3-b6ab-4a00-a075-b693003c527b
    main()
