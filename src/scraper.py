import re

from bs4 import BeautifulSoup as bs


class QuestionScraper:
    def __init__(self, html_files=[]):
        self.parsed = self._parse_file(html_files)

    def _clean_string(self, string: str) -> str:
        string = re.sub(r"^[\n\s]+", "", string)
        string = re.sub(r"[\n\s]+$", "", string)
        string = re.sub(r"\n", " ", string)
        string = re.sub(r"\s{2,}", " ", string)
        string = string.rstrip()
        _ = string.split(" ")
        if len(_) >= 2:
            if " ".join(_[-2:]).lower() == "most voted":
                string = " ".join(_[:-2])

        string = string.encode("ascii", errors="ignore").decode()

        return string

    def _getExamTitle(self):
        return " ".join(
            self._clean_string(
                self.parsed[0].find("h1", attrs={"id": "exam-box-title"}).text
            ).split(" ")[:-3]
        )

    def _parse_file(self, html_files):
        parsed_files = []
        for html_file in html_files:
            with open(html_file, "r", encoding="utf8") as fhandler:
                parsed_file = bs(fhandler.read(), "html.parser")
                parsed_files.append(parsed_file)
        return parsed_files

    def get_all_questions(self):
        questions_raw = []
        for page in self.parsed:
            questions_in_page = page.find_all(
                "div", attrs={"class": "card exam-question-card"}
            )
            for question_raw in questions_in_page:
                questions_raw.append(question_raw)

        return questions_raw

    def get_question_body(self, question):
        question_body = question.find("p", attrs={"class": "card-text"})
        img = question_body.find("img")
        if img:
            return [self._clean_string(question_body.text), img["src"]]
        else:
            return [self._clean_string(question_body.text), None]

    def get_question_number(self, question):
        return self._clean_string(
            question.find(
                "div", attrs={"class": "card-header text-white bg-primary"}
            ).text
        ).split(" ")[1]

    def get_answers(self, question):
        return [
            self._clean_string(answer.text)
            for answer in question.find_all("li", attrs={"class": "multi-choice-item"})
        ]

    def get_correct_community_answer(self, question):
        correct_answer_raw = question.find(
            "p", attrs={"class": "card-text question-answer bg-light white-text"}
        )

        community_vote_bar = correct_answer_raw.find(
            "div", attrs={"class": "vote-bar progress-bar bg-primary"}
        )

        if community_vote_bar:
            return self._clean_string(community_vote_bar.text.split(" ")[0])
        else:
            return "None"

    def get_correct_et_answer(self, question):
        correct_answer_raw = question.find(
            "p", attrs={"class": "card-text question-answer bg-light white-text"}
        )
        return self._clean_string(
            correct_answer_raw.find("span", attrs={"class": "correct-answer"}).text
        )
