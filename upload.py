import os

from roboflow import Roboflow
import dotenv
dotenv.load_dotenv()
rf = Roboflow(api_key=os.getenv("ROBOFLOW_API_KEY"))
workspace = rf.workspace(os.getenv('ROBOFLOW_WORKSPACE'))

workspace.deploy_model(
  model_type="yolov11",
  model_path=r"C:\Users\Administrator\Downloads\train3\train3",
  project_ids=[os.getenv("ROBOFLOW_PROJECT_ID")],
  model_name="third"
)