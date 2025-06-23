import os

from app.lib.face.faceRecognition import get_singleton

frc = None
if os.getenv('MODE') == 'worker':
    frc = get_singleton()
