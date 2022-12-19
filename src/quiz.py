import os
import random

from question import Question
from scraper import QuestionScraper


class Quiz:
    def __init__(self, quiz_dir=None) -> None:
        self.scraper = QuestionScraper(quiz_dir, self._get_html_files(quiz_dir))
        self.title = self.scraper._getExamTitle()
        self.questions = self._extract_questions()

    def _get_html_files(self, quiz_dir: str):
        html = []
        for file in os.listdir(quiz_dir):
            _ = os.path.join(quiz_dir, file)
            if os.path.isfile(_):
                html.append(_)
        return html

    def _extract_questions(self):
        all_questions_raw = self.scraper.get_all_questions()
        questions = []
        for question in all_questions_raw:
            question_number = self.scraper.get_question_number(question)
            text, introduction, img = self.scraper.get_question_body(question)
            answers = self.scraper.get_answers(question)
            correct_community_answer = self.scraper.get_correct_community_answer(
                question
            )
            correct_et_answer = self.scraper.get_correct_et_answer(question)
            questions.append(
                Question(
                    question_number,
                    introduction,
                    text,
                    img,
                    answers,
                    correct_community_answer,
                    correct_et_answer,
                )
            )

        return questions
