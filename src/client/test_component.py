import flet
import json
from settings import SETTINGS as settings
import requests
from random import shuffle


class Question(flet.SafeArea):
    def __init__(self, test_data: dict, self_id: int) -> None:
        super().__init__()
        self.self_id = self_id

        video_file: dict = requests.get(
            url=f'{settings.SERVER_URL}/video_file/get/{test_data['video_file']}',
            params={
                'token': settings.TOKEN,
            }
        ).json()
        self.video_file_name: str = video_file['name']
        self.correct_answers: dict = json.loads(test_data['correct_answers'])
        self.incorrect_answers: dict = json.loads(test_data['incorrect_answers'])

    def video_replay(self, event: flet.ControlEvent) -> None:
        self.content.controls[0].seek(0)
        self.content.controls[0].play()

    def on_answer_click(self, event: flet.ControlEvent) -> None:
        if event.control.data == 'correct':
            self.parent.parent.parent.parent.correct_answers += 1
        else:
            self.parent.parent.parent.parent.incorrect_answers += 1

        self.next_button.visible = True
        self.update()

    def on_next_click(self) -> None:
        self.parent.parent.parent.parent.switch_question(self.self_id + 1)

    def build(self) -> None:
        answers: list = []
        self.next_button: flet.TextButton = flet.TextButton(
            text='Следующий',
            icon=flet.icons.ARROW_RIGHT,
            visible=False,
            on_click=lambda _: self.on_next_click()
        )

        for answer in self.incorrect_answers:
            answers.append(
                flet.FilledButton(
                    text=str(answer),
                    width=180,
                    data='incorrect',
                    on_click=self.on_answer_click
                )
            )

        for answer in self.correct_answers:
            answers.append(
                flet.FilledButton(
                    text=str(answer),
                    width=180,
                    data='correct',
                    on_click=self.on_answer_click
                )
            )

        shuffle(answers)

        self.content = flet.Column(
            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
            controls=[
                flet.Video(
                    aspect_ratio=19 / 10,
                    autoplay=True,
                    volume=0,
                    show_controls=False,
                    playlist=[
                        flet.VideoMedia(
                            resource=f'{settings.SERVER_URL}/video_file/get_file_by_filename/{self.video_file_name}')
                    ]
                ),
                flet.FilledButton(
                    icon=flet.icons.REPLAY,
                    text='Пересмотреть',
                    on_click=self.video_replay,
                    style=flet.ButtonStyle(
                        shape=flet.RoundedRectangleBorder(radius=10),
                        bgcolor=flet.colors.SURFACE_VARIANT,
                        color=flet.colors.PRIMARY
                    )
                ),
                flet.Divider(height=20),
                flet.Column(
                    horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                    controls=[
                        flet.Row(
                            alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
                            controls=answers[:2]
                        ),
                        flet.Row(
                            alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
                            controls=answers[2:]
                        )
                    ]
                ),
                self.next_button
            ]
        )


class Test(flet.SafeArea):
    def __init__(self, test_data: list, test_id: int) -> None:
        super().__init__()
        self.test_datas = test_data
        self.test_id = test_id
        self.correct_answers = 0
        self.incorrect_answers = 0

    def on_test_finish_click(self) -> None:
        self.page.controls[1].visible = True
        self.parent.parent.destroy_create_page()

    def switch_question(self, question_id: int) -> None:
        test_ended = False
        self.questions.controls.clear()

        for ni, test_data in enumerate(self.test_datas):
            self.questions.controls.append(
                Question(
                    test_data=test_data,
                    self_id=ni
                )
            )

        self.update()
        for question in self.questions.controls:
            question.visible = question.self_id == question_id
            question.update()

            self.progress_bar.value = question_id / len(self.test_datas)

            if question_id == len(self.questions.controls):
                test_ended = True

        if test_ended:
            self.content.controls = [
                flet.Text(value=f'Тест{" " if self.incorrect_answers == 0 else " не "}завершен'),
                flet.Row(
                    alignment=flet.MainAxisAlignment.CENTER,
                    controls=[
                        flet.Column(controls=[flet.Text('Верных ответов: ' + str(self.correct_answers))]),
                        flet.Column(controls=[flet.Text('Неверных ответов: ' + str(self.incorrect_answers))])
                    ]
                ),
                flet.Divider(height=100),
                flet.TextButton(
                    text='Завершить тест',
                    on_click=lambda _: self.on_test_finish_click()
                )
            ]

        self.update()

        if self.incorrect_answers == 0 and test_ended:
            finished_tests = requests.get(
                url=f'{settings.SERVER_URL}/finished_test/get_for_user/{self.page.session.get("session").User.user_id}',
                params={'token': settings.TOKEN}
            ).json()

            if not any(test['user'] == self.page.session.get('session').User.user_id and test['test'] == self.test_id for test in finished_tests):
                requests.post(
                    url=f'{settings.SERVER_URL}/finished_test/create',
                    params={'token': settings.TOKEN},
                    json={'test': self.test_id, 'user': self.page.session.get('session').User.user_id}
                )

    def build(self) -> None:
        self.questions = flet.Column()
        self.progress_bar = flet.ProgressBar(value=0 / len(self.test_datas))

        for ni, test_data in enumerate(self.test_datas):
            self.questions.controls.append(
                Question(
                    test_data=test_data,
                    self_id=ni
                )
            )

        for q in self.questions.controls:
            q.visible = False

        self.questions.controls[0].visible = True

        self.content = flet.Column(
            alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
            controls=[
                flet.Container(content=self.questions),
                flet.Divider(height=20),
                self.progress_bar,
                flet.TextButton(
                    text='Завершить тест',
                    on_click=lambda _: self.on_test_finish_click()
                )
            ],
        )