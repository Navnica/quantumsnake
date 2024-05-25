import asyncio
import flet


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
            self.search_bar_content.controls.clear()
            await self.update_async()

        self.search_bar_content.controls.clear()

        similar_strings: list = []

        for icon in flet.icons.__dict__:
            if event.data.upper() in icon:
                if str(icon).startswith('__') and str(icon).endswith('__'):
                    continue

                similar_strings.append(icon)
                self.search_bar_content.controls.append(
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

    def build(self):
        self.search_bar_content: flet.Column = flet.Column()
        self.content = flet.Column(
            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
            controls=[
                flet.Row(
                    alignment=flet.MainAxisAlignment.START,
                    controls=[
                        flet.IconButton(
                            icon=flet.icons.ARROW_BACK,
                            on_click=lambda _: self.par.switch_container(self.par.content.controls[0])
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
                                icon=flet.icons.EMOJI_EMOTIONS,
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
                                bar_hint_text="Выбор иконки",
                                full_screen=True,
                                controls=[self.search_bar_content],
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
                )
            ]
        )
