import flet
from random import choice
import asyncio
import requests
from settings import SETTINGS
import json


class Question(flet.Container):
    video_file_name: str = None

    def __init__(self) -> None:
        super().__init__()

    def on_search_bar_change(self, event: flet.ControlEvent) -> None:
        async def on_question_word_select_click(e: flet.ControlEvent):
            search_bar.close_view()
            self.content.controls[1].controls[0].value = e.control.data
            self.content.controls[1].controls[0].focus()
            self.page.update()

            self.video_file_name = e.control.data

            await asyncio.sleep(0.1)
            search_bar.value = e.control.data
            self.page.update()

        search_bar: flet.SearchBar = event.control
        search_bar.controls[0].controls.clear()

        for word in self.page.session.get('session').VideoFiles().get_all():
            if word.name.lower() in search_bar.value.lower():
                search_bar.controls[0].controls.append(
                    flet.ListTile(
                        title=flet.Text(word.name),
                        data=word.name,
                        on_click=on_question_word_select_click
                    )
                )

        search_bar.update()

    def on_correct_check_box_click(self, event: flet.ControlEvent) -> None:
        color: str = flet.colors.GREEN_500 if event.control.value else flet.colors.RED_ACCENT
        event.control.parent.parent.controls[0].border_color = color
        self.update()

    def on_randomize_check_box_click(self, event: flet.ControlEvent) -> None:
        event.control.parent.parent.controls[0].read_only = event.control.value

        if event.control.value:
            event.control.parent.parent.controls[0].value = choice(
                self.page.session.get('session').VideoFiles().get_all()).name
        else:
            event.control.parent.parent.controls[0].value = ''

        self.update()

    def build(self) -> None:
        self.border = flet.border.all(width=2, color=flet.colors.PRIMARY)
        self.border_radius = 15
        self.padding = 10
        self.alignment = flet.alignment.center
        self.content = flet.Column(
            alignment=flet.MainAxisAlignment.START,
            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
            controls=[
                flet.SearchBar(
                    view_leading=flet.Container(),
                    height=45,
                    on_change=self.on_search_bar_change,
                    full_screen=True,
                    controls=[
                        flet.Column(

                        )
                    ]
                ),
                flet.Row(
                    alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        flet.TextField(
                            label='Ответ №1',
                            border_radius=10,
                            border_width=2,
                            border_color=flet.colors.GREEN_ACCENT,
                            width=200,
                            height=50,
                            dense=True,
                            read_only=False
                        ),
                        flet.Column(
                            alignment=flet.MainAxisAlignment.CENTER,
                            controls=[
                                flet.Checkbox(
                                    label='Верный',
                                    value=True,
                                    on_change=self.on_correct_check_box_click
                                ),
                                flet.Checkbox(
                                    label='Случайный',
                                    value=False,
                                    on_change=self.on_randomize_check_box_click
                                )
                            ]
                        )

                    ]
                ),
                flet.Divider(height=5, color=flet.colors.SURFACE_TINT),
                flet.Row(
                    alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        flet.TextField(
                            label='Ответ №2',
                            border_radius=10,
                            border_width=2,
                            border_color=flet.colors.RED_ACCENT,
                            width=200,
                            height=50,
                            dense=True,
                            read_only=True,
                            value=choice(self.page.session.get('session').VideoFiles().get_all()).name
                        ),
                        flet.Column(
                            alignment=flet.MainAxisAlignment.CENTER,
                            controls=[
                                flet.Checkbox(
                                    label='Верный',
                                    value=False,
                                    on_change=self.on_correct_check_box_click
                                ),
                                flet.Checkbox(
                                    label='Случайный',
                                    value=True,
                                    on_change=self.on_randomize_check_box_click
                                )
                            ]
                        )

                    ]
                ),
                flet.Divider(height=5, color=flet.colors.SURFACE_TINT),
                flet.Row(
                    alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        flet.TextField(
                            label='Ответ №3',
                            border_radius=10,
                            border_width=2,
                            border_color=flet.colors.RED_ACCENT,
                            width=200,
                            height=50,
                            dense=True,
                            read_only=True,
                            value=choice(self.page.session.get('session').VideoFiles().get_all()).name
                        ),
                        flet.Column(
                            alignment=flet.MainAxisAlignment.CENTER,
                            controls=[
                                flet.Checkbox(
                                    label='Верный',
                                    value=False,
                                    on_change=self.on_correct_check_box_click
                                ),
                                flet.Checkbox(
                                    label='Случайный',
                                    value=True,
                                    on_change=self.on_randomize_check_box_click
                                )
                            ]
                        )

                    ]
                ),
                flet.Divider(height=5, color=flet.colors.SURFACE_TINT),
                flet.Row(
                    alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        flet.TextField(
                            label='Ответ №4',
                            border_radius=10,
                            border_width=2,
                            border_color=flet.colors.RED_ACCENT,
                            width=200,
                            height=50,
                            dense=True,
                            read_only=True,
                            value=choice(self.page.session.get('session').VideoFiles().get_all()).name
                        ),
                        flet.Column(
                            alignment=flet.MainAxisAlignment.CENTER,
                            controls=[
                                flet.Checkbox(
                                    label='Верный',
                                    value=False,
                                    on_change=self.on_correct_check_box_click
                                ),
                                flet.Checkbox(
                                    label='Случайный',
                                    value=True,
                                    on_change=self.on_randomize_check_box_click
                                )
                            ]
                        )

                    ]
                ),
                flet.Divider(height=5, color=flet.colors.SURFACE_TINT),
            ]
        )


class TestCreateFragment(flet.SafeArea):
    def __init__(self, par: flet.SafeArea) -> None:
        super().__init__()
        self.par = par

    async def show_icon_select_panel(self, event: flet.ControlEvent) -> None:
        self.content.controls[1].content.controls[2].open_view()
        self.update()

    async def on_search_bar_change(self, event: flet.ControlEvent) -> None:
        async def on_select_icon(event: flet.ControlEvent) -> None:
            self.content.controls[1].content.controls[1].icon = event.control.data
            self.content.controls[1].content.controls[2].close_view()
            search_bar_content.controls.clear()
            self.update()

        search_bar_content = event.control.controls[0]

        search_bar_content.controls.clear()

        similar_strings: list = []

        for icon in flet.icons.__dict__:
            if event.data.upper() in icon:
                if str(icon).startswith('__') and str(icon).endswith('__'):
                    continue

                similar_strings.append(icon)
                search_bar_content.controls.append(
                    flet.ListTile(
                        title=flet.Text(
                            value=icon
                        ),
                        leading=flet.Icon(
                            name=icon,
                            color=flet.colors.SURFACE_TINT
                        ),
                        data=icon,
                        on_click=on_select_icon
                    )
                )

                if len(similar_strings) == 100:
                    break

        self.update()

    def update_relevance_count(self, event: flet.ControlEvent) -> None:
        text_field: flet.TextField = self.content.controls[2].content.controls[3].controls[0]
        current_num: int = int(text_field.value) + int(event.control.data)

        if current_num < 1:
            current_num = 1

        text_field.value = str(current_num)
        self.update()

    def show_about_relevance_count(self, event: flet.ControlEvent) -> None:
        def close_info(event: flet.ControlEvent) -> None:
            self.page.overlay[-1].open = False
            self.page.update()

        self.page.overlay.append(
            flet.BottomSheet(
                open=True,
                content=flet.Column(
                    alignment=flet.MainAxisAlignment.SPACE_AROUND,
                    horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                    controls=[
                        flet.Text(
                            value='Ролевантность текста показывает насколько важен будет данный тест. Например, тест с ролевантностью 1 будет отображен выше, чем тест с ролевантностью 2',
                            selectable=False,
                            text_align=flet.TextAlign.CENTER
                        ),
                        flet.FilledButton(
                            text='Понятно',
                            on_click=close_info
                        ),
                    ]
                )
            )
        )

        self.page.update()

    def on_add_question_click(self, event: flet.ControlEvent) -> None:
        event.control.parent.controls.insert(-1, Question())
        self.update()

    def on_drop_button_click(self, event: flet.ControlEvent) -> None:
        self.par.destroy_create_page()
        self.par.on_new_test_click()

    def on_save_click(self, event: flet.ControlEvent) -> None:
        name: str = self.content.controls[2].content.controls[1].value
        icon_name: str = self.content.controls[1].content.controls[1].icon
        relevance: int = int(self.content.controls[2].content.controls[3].controls[0].value)

        new_test: dict = requests.post(
            url=f'{SETTINGS.SERVER_URL}/test/create',
            json={
                'name': name,
                'icon_name': icon_name,
                'relevance': relevance
            },
            params={
                'token': SETTINGS.TOKEN
            }
        ).json()

        for question in self.content.controls[3].content.controls:
            def on_ok_click():
                self.page.dialog.open = False
                self.page.update()
                self.par.destroy_create_page()

            if type(question) is Question:
                correct_answers: list[str] = []
                incorrect_answers: list[str] = []
                video_file: str = question.video_file_name

                for q in question.content.controls:
                    if type(q) is flet.Row:
                        if q.controls[0].border_color == flet.colors.GREEN_ACCENT:
                            correct_answers.append(q.controls[0].value)
                        else:
                            incorrect_answers.append(q.controls[0].value)

                requests.post(
                    url=f'{SETTINGS.SERVER_URL}/test_question/create',
                    json={
                        'test': new_test['id'],
                        'video_file': requests.get(f'{SETTINGS.SERVER_URL}/video_file/get_by_name/{video_file}').json()['id'],
                        'correct_answers': json.dumps(correct_answers),
                        'incorrect_answers': json.dumps(incorrect_answers),
                    },
                    params={
                        'token': SETTINGS.TOKEN
                    }
                )

        self.page.dialog = flet.AlertDialog(
            open=True,
            actions=[
                flet.FilledButton(
                    text='Ок',
                    icon=flet.icons.DONE,
                    on_click=lambda _: on_ok_click()
                )
            ],
            content=flet.Column(
                alignment=flet.MainAxisAlignment.CENTER,
                horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                controls=[
                    flet.Text('Тест создан')
                ]
            )
        )

        self.page.update()

    def build(self):
        self.content = flet.Column(
            scroll=flet.ScrollMode.AUTO,
            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
            controls=[
                flet.Row(
                    alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        flet.TextButton(
                            text='Назад',
                            icon=flet.icons.ARROW_BACK,
                            on_click=lambda _: self.par.switch_container(self.par.content.controls[0])
                        ),
                        flet.TextButton(
                            text='Сохранить',
                            icon=flet.icons.SAVE,
                            on_click=self.on_save_click
                        ),
                        flet.TextButton(
                            text='Сбросить',
                            icon=flet.icons.AUTORENEW,
                            on_click=self.on_drop_button_click
                        )
                    ]
                ),
                flet.Container(
                    bgcolor=flet.colors.SURFACE_VARIANT,
                    border_radius=15,
                    padding=10,
                    alignment=flet.alignment.center,
                    content=flet.Column(
                        horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                        controls=[
                            flet.Text('Иконка теста'),
                            flet.IconButton(
                                icon='EMOJI_EMOTIONS',
                                icon_size=80,
                                on_click=self.show_icon_select_panel,
                                style=flet.ButtonStyle(
                                    shape=flet.RoundedRectangleBorder(
                                        radius=15
                                    ),
                                    bgcolor=flet.colors.SURFACE
                                )
                            ),
                            flet.SearchBar(
                                height=0,
                                width=0,
                                visible=True,
                                full_screen=True,
                                controls=[flet.Column()],
                                on_change=self.on_search_bar_change
                            ),
                        ]
                    )
                ),
                flet.Container(
                    bgcolor=flet.colors.SURFACE_VARIANT,
                    border_radius=15,
                    padding=10,
                    alignment=flet.alignment.center,
                    content=flet.Column(
                        horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                        controls=[
                            flet.Text(value='Настройки теста'),
                            flet.TextField(
                                label='Название',
                                border_radius=10,
                                border_width=2,
                                border_color=flet.colors.PRIMARY,
                            ),
                            flet.Divider(height=5, color=flet.colors.TRANSPARENT),
                            flet.Row(
                                alignment=flet.MainAxisAlignment.CENTER,
                                controls=[
                                    flet.TextField(
                                        dense=True,
                                        height=60,
                                        expand=True,
                                        label='Ролевантность',
                                        border_radius=10,
                                        border_width=2,
                                        border_color=flet.colors.PRIMARY,
                                        value='1',
                                        text_align=flet.TextAlign.CENTER,
                                        read_only=True,
                                        prefix=flet.IconButton(
                                            icon=flet.icons.ARROW_LEFT,
                                            icon_color=flet.colors.SURFACE_VARIANT,
                                            width=40,
                                            height=40,
                                            on_click=self.update_relevance_count,
                                            data=-1,
                                            style=flet.ButtonStyle(
                                                bgcolor=flet.colors.SURFACE_TINT,
                                                shape=flet.RoundedRectangleBorder(
                                                    radius=10
                                                )
                                            )
                                        ),
                                        suffix=flet.IconButton(
                                            icon=flet.icons.ARROW_RIGHT,
                                            icon_color=flet.colors.SURFACE_VARIANT,
                                            width=40,
                                            height=40,
                                            on_click=self.update_relevance_count,
                                            data=1,
                                            style=flet.ButtonStyle(
                                                bgcolor=flet.colors.SURFACE_TINT,
                                                shape=flet.RoundedRectangleBorder(
                                                    radius=10
                                                )
                                            )
                                        )
                                    ),
                                    flet.IconButton(
                                        icon=flet.icons.QUESTION_MARK,
                                        on_click=self.show_about_relevance_count,
                                    )
                                ]
                            )
                        ]
                    )
                ),
                flet.Container(
                    bgcolor=flet.colors.SURFACE_VARIANT,
                    border_radius=15,
                    padding=10,
                    alignment=flet.alignment.center,
                    content=flet.Column(
                        horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                        controls=[
                            flet.Text(value='Вопросы'),
                            Question(),
                            flet.FilledButton(
                                width=200,
                                text='Добавить',
                                icon=flet.icons.ADD,
                                on_click=self.on_add_question_click
                            )
                        ]
                    )
                )
            ]
        )
