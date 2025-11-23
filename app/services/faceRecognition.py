import cv2
import numpy as np
from insightface.app import FaceAnalysis

class FaceRecognition():
    def __init__(self, app, model='buffalo_s',root="app/services/models/models", threshold=0.65, device=-1,):
        self.app = app
        self.app.prepare(ctx_id=device)
        self.threshold = threshold

    def get_face_embedding(self, image_bytes):
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError("Could not decode image from bytes")
        faces = self.app.get(img)

        if len(faces) < 1:
            raise ValueError("No faces detected in the image")
        if len(faces) > 1:
            print("Warning: Multiple faces detected. Using first detected face")

        return faces[0].embedding

    def compare_faces(self, emb1, emb2):
        similatry= np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))

        return  similatry, similatry>self.threshold

