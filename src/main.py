import os

import firebase
from quiz import Quiz

if __name__ == "__main__":
    quiz_folders = [
        os.path.join("./input", name)
        for name in os.listdir("./input")
        if os.path.isdir(os.path.join("./input", name))
    ]
    for quiz_path in quiz_folders:
        quiz = Quiz(quiz_path)
        firebase.uploadQuiz(quiz)
