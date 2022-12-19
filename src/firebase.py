import os

import firebase_admin
from firebase_admin import credentials, firestore, storage

cred = credentials.Certificate(os.environ.get("FIREBASE_CREDENTIALS_PATH"))
firebase_admin.initialize_app(
    cred, {"storageBucket": os.environ.get("FIREBASE_BUCKET")}
)

uploaded_imgs = {}


def uploadImg(dir, imgPath):
    if imgPath.split("/")[-1] in uploaded_imgs:
        return uploaded_imgs[imgPath.split("/")[-1]]

    bucket = storage.bucket()
    blob = bucket.blob(dir + "/" + imgPath.split("/")[-1])
    blob.upload_from_filename(imgPath)
    blob.make_public()

    uploaded_imgs[imgPath.split("/")[-1]] = blob.public_url

    return blob.public_url


def uploadQuiz(quiz):
    db = firestore.client()

    questions_objs = [vars(question) for question in quiz.questions]

    exam_ref = db.collection("exams").document()
    exam_ref.set({"name": quiz.title})

    questions_coll = db.collection("questions")
    for question in questions_objs:
        question["exam_id"] = exam_ref.id
        questions_coll.document().set(question)
