class Question:
    def __init__(
        self,
        question_number: str,
        introduction: str,
        question: str,
        question_img: str,
        answers: list,
        correct_community_answer: str,
        correct_et_answer: str,
    ):
        self.question_number = question_number
        self.introduction = introduction
        self.question = question
        self.question_img = question_img
        self.answers = answers
        self.correct_community_answer = correct_community_answer
        self.correct_et_answer = correct_et_answer

    def print(self):
        print(f"{self.question_number}. {self.question}")
        print("Answers:")
        print(self.answers)
        print(f"Correct community answer: {self.correct_community_answer}")
        print(f"Correct ExamTopics answer: {self.correct_et_answer}")
