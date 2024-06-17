import flet
import json
from settings import SETTINGS as settings
import requests


class Question(flet.SafeArea):
    def __init__(self, test_data: dict) -> None:
        super().__init__()
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

    def build(self) -> None:
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
                flet.GridView(
                    runs_count=2,
                    horizontal=True,
                    controls=[
                        flet.FilledButton(
                            text=str(answer),
                            width=100,
                            height=40
                        ) for answer in self.incorrect_answers
                    ]
                )
            ]
        )


class Test(flet.SafeArea):
    def __init__(self, test_data: list) -> None:
        super().__init__()
        self.test_datas = test_data

    def on_test_finish_click(self, event: flet.ControlEvent) -> None:
        self.page.controls[1].visible = True
        self.parent.parent.parent.destroy_create_page()

    def build(self) -> None:
        self.expand = True
        self.content = flet.Column(
            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
            controls=[
                flet.Container(
                    content=Question(self.test_datas[0])
                ),
                flet.TextButton(
                    text='Завершить тест',
                    on_click=self.on_test_finish_click
                )
            ],
        )
