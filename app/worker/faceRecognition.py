from app import celery
from app.worker import frc


@celery.task
def create_user_face_embedding(face_info, user_id):
    try:
        embed = frc.face_embedding(face_info)
        frc.put_embedding_to_weaviate(embed, user_id)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


@celery.task
def get_user_id_by_face(face_info):
    try:
        embed = frc.face_embedding(face_info)
        user_id = frc.check_without_uuid(embed)
        return {"user_id": user_id}
    except Exception:
        return {"user_id": None}


@celery.task
def delete_face_embedding(user_id):
    try:
        frc.delete_embedding(user_id)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}
