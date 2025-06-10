import os
import dotenv
from weaviate.classes.init import Auth
import weaviate
dotenv.load_dotenv()
class WeaviateClient:
    def __init__(self):
        self.client = weaviate.connect_to_local(
            host=os.getenv("WEAVIATE_HOST"),
            port=int(os.getenv("WEAVIATE_TCP_PORT")),
            grpc_port=int(os.getenv("WEAVIATE_GRPC_PORT")),
            auth_credentials=Auth.api_key(os.environ.get('WEAVIATE_API_KEY')),
            headers={
                "X-OpenAI-BaseURL": os.getenv("OPENAI_BASE_URL").replace('/v1',''),
                "X-OpenAI-Api-Key": os.getenv('OPENAI_API_KEY'),
            }
        )
    def getClient(self):
        return self.client