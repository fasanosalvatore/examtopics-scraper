import argparse
import random

import jsonpickle
from jinja2 import Environment, FileSystemLoader

from quiz import Quiz

if __name__ == "__main__":
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument("--src", action="store", type=str, required=True)
    my_parser.add_argument("--start", action="store", nargs="?", default=0, type=int)
    my_parser.add_argument("--count", action="store", type=int)
    args = my_parser.parse_args()

    quiz = Quiz(args.src)
    title = quiz.getExamTitle()
    questions = quiz.convert()[args.start : args.start + args.count]
    random.shuffle(questions)
    for question in questions:
        random.shuffle(question.answers)
    questions_json = jsonpickle.encode(questions)
    environment = Environment(loader=FileSystemLoader("./src/templates/"))
    template = environment.get_template("index.html")
    content = template.render(title=title, questions=questions_json)
    with open("./input/result.html", mode="w", encoding="utf-8") as f:
        f.write(content)
        print("Wrote")
