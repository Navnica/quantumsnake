import flet
from src.client.test_create_fragment import TestCreateFragment
import requests
from settings import SETTINGS as settings
from asyncio import sleep as asleep
from src.client.test_component import Test


class TestsComponent(flet.SafeArea):
    def __init__(self):
        super().__init__()

    def reload(self) -> None:
        pass

    def switch_container(self, container: flet.Container) -> None:
        for c in self.content.controls:
            c.visible = c == container

        self.page.update()

    def on_new_test_click(self, event: flet.ControlEvent = None) -> None:
        self.content.controls[1].content = TestCreateFragment(par=self)
        self.switch_container(self.content.controls[1])

    def destroy_create_page(self, event: flet.ControlEvent = None) -> None:
        self.content.controls[1] = flet.Container()
        self.switch_container(self.content.controls[0])
        self.page.update()
        self.build()

    async def get_tests(self):
        def show_load_indicator() -> None:
            self.page.dialog = flet.AlertDialog(
                modal=True,
                open=True,
                content_padding=10,
                content=flet.Row(
                    alignment=flet.MainAxisAlignment.CENTER,
                    vertical_alignment=flet.CrossAxisAlignment.CENTER,
                    controls=[
                        flet.ProgressRing(
                            height=70,
                            width=70
                        )
                    ]
                )
            )
            self.page.update()

        def hide_load_indicator() -> None:
            self.page.dialog.open = False
            self.page.update()

        async def create_test(event: flet.ControlEvent) -> None:
            async def collect_test_questions() -> None:
                test_data: list = requests.get(
                    url=f'{settings.SERVER_URL}/test_question/get_for_test/{test_id}',
                    params={'token': settings.TOKEN}
                ).json()

                await asleep(0.5)
                hide_load_indicator()
                self.page.controls[1].visible = False
                new_test: Test = Test(test_data=test_data, test_id=test_id)
                self.content.controls[1] = new_test
                self.switch_container(self.content.controls[1])

            test_id: int = event.control.data
            show_load_indicator()
            await collect_test_questions()

        tests = requests.get(
            url=f'{settings.SERVER_URL}/test/get_all',
            params={'token': settings.TOKEN}
        ).json()

        sorted_tests = sorted(tests, key=lambda x: x['relevance'])
        for test in sorted_tests:
            finished = requests.get(
                url=f'{settings.SERVER_URL}/finished_test/finished_for_user/{self.page.session.get("session").User.user_id}/{test["id"]}',
                params={'token': settings.TOKEN}
            ).json()

            self.content.controls[0].content.controls[4].controls.append(
                flet.Container(
                    border_radius=10,
                    padding=20,
                    bgcolor=flet.colors.SURFACE_VARIANT if not finished else '#228B22',
                    content=flet.Column(
                        horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                        controls=[
                            flet.IconButton(
                                icon=test['icon_name'],
                                icon_size=50,
                                data=int(test['id']),
                                on_click=lambda e: self.page.loop.create_task(create_test(e)),
                                style=flet.ButtonStyle(
                                    shape=flet.RoundedRectangleBorder(radius=10)
                                )
                            ),
                            flet.Text(value=test['name'])
                        ]
                    )
                )
            )

        test_finished = len(requests.get(
            url=f'{settings.SERVER_URL}/finished_test/get_for_user/{self.page.session.get("session").User.user_id}',
            params={'token': settings.TOKEN}
        ).json())

        total_tests = len(self.content.controls[0].content.controls[4].controls)

        self.content.controls[0].content.controls[0].controls[1].content.controls[1].value = f'{test_finished}/{total_tests}'
        try:
            self.content.controls[0].content.controls[0].controls[0].value = test_finished / total_tests
        except ZeroDivisionError:
            pass

        self.page.update()

    def build(self) -> None:
        self.content = flet.Column(
            scroll=flet.ScrollMode.AUTO,
            controls=[
                flet.Container(
                    visible=True,
                    content=flet.Column(
                        horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                        alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            flet.Stack(
                                width=150,
                                height=150,
                                controls=[
                                    flet.ProgressRing(
                                        value=0,
                                        bgcolor=flet.colors.SURFACE_VARIANT,
                                        width=150,
                                        height=150,
                                    ),
                                    flet.Container(
                                        alignment=flet.alignment.center,
                                        content=flet.Column(
                                            alignment=flet.MainAxisAlignment.CENTER,
                                            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                                            controls=[
                                                flet.Text("Тестов пройдено", weight=flet.FontWeight.BOLD),
                                                flet.Text("0/4")
                                            ]
                                        ),
                                    )
                                ]
                            ),
                            flet.Divider(height=20, color=flet.colors.TRANSPARENT),
                            flet.FilledButton(
                                text='Новый тест',
                                visible=self.page.session.get('session').Role.power_level > 1,
                                on_click=self.on_new_test_click
                            ),
                            flet.Divider(height=10),
                            flet.Column()
                        ]
                    )
                ),
                flet.Container(),
            ]
        )

        self.page.loop.create_task(self.get_tests())
