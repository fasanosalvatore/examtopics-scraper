import re
import string

from bs4 import BeautifulSoup as bs

import firebase


class QuestionScraper:
    def __init__(self, quiz_dir, html_files=[]):
        self.parsed = self._parse_file(html_files)
        self.quiz_dir = quiz_dir

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
        introduction = ""
        question_text = ""
        img_src = ""

        question_body = question.find("p", attrs={"class": "card-text"})

        imgs = question_body.find_all("img")
        if imgs:
            img_src = firebase.uploadImg(
                self.quiz_dir.split("/")[-1], self.quiz_dir + "/" + imgs[0]["src"][2:]
            )
            for img in imgs:
                img.decompose()

        spans = question_body.find_all("span", attrs={})
        if spans:
            introduction = self._clean_string(
                str(question_body).split(str(spans[0]))[1].split(str(spans[1]))[0]
            )
            question_text = self._clean_string(
                str(question_body).split(str(spans[1]))[1]
            )
        else:
            question_text = self._clean_string(str(question_body))

        return [question_text, introduction, img_src]

    def get_question_number(self, question):
        return self._clean_string(
            question.find(
                "div", attrs={"class": "card-header text-white bg-primary"}
            ).text
        ).split(" ")[1]

    def get_answers(self, question):
        answers = []

        # imgs = question.find_all("img", attrs={"class": "in-exam-image"})
        # if imgs:
        #     answers = [
        #         {
        #             "id": string.ascii_uppercase[index],
        #             "text": "",
        #             "img": firebase.uploadImg("./input/" + img["src"][2:]),
        #         }
        #         for index, img in enumerate(imgs)
        #     ]
        # else:
        answers = [
            {
                "id": self._clean_string(answer.text)[0],
                "text": self._clean_string(answer.text)[3:],
                "img": "",
            }
            for answer in question.find_all("li", attrs={"class": "multi-choice-item"})
        ]

        return answers

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
