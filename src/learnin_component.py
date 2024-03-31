import flet


class AbcComponent(flet.UserControl):
    def __init__(self) -> None:
        super().__init__()

    def build(self):
        self.visible = False

        column: flet.Column = flet.Column(alignment=flet.MainAxisAlignment.CENTER)
        new_row: flet.Row = flet.Row(alignment=flet.MainAxisAlignment.CENTER)

        for letter in ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С',
                       'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']:
            new_row.controls.append(flet.FilledButton(
                text=letter,
                on_click=self.on_letter_pressed,
                style=flet.ButtonStyle(
                    shape=flet.RoundedRectangleBorder(radius=8),
                    bgcolor=flet.colors.GREY_800,
                    color=flet.colors.WHITE
                ),
                width=60
            ))

            if len(new_row.controls) == 5:
                column.controls.append(new_row)
                new_row = flet.Row(alignment=flet.MainAxisAlignment.CENTER)

        column.controls.append(new_row)

        return column

    def on_letter_pressed(self, event: flet.ControlEvent) -> None:
        letter: str = event.control.text
        d = flet.AlertDialog(
            modal=False,
            content=flet.Video(
                playlist=[flet.VideoMedia('./assets/1.mp4')],
                autoplay=True,
                show_controls=False,
                height=200,
                aspect_ratio=4/3
            )
        )

        self.page.dialog = d
        d.open = True
        self.page.update()


class GrammarComponent(flet.UserControl):
    def __init__(self) -> None:
        super().__init__()

    def build(self) -> flet.Column:
        self.visible = False
        return flet.Column(
            alignment=flet.MainAxisAlignment.CENTER,
            controls=[
                flet.Row(
                    alignment=flet.MainAxisAlignment.CENTER,
                    controls=[
                        flet.Text("Grammar Page")
                    ]
                )
            ]
        )


class DictComponent(flet.UserControl):
    def __init__(self) -> None:
        super().__init__()

    def build(self) -> flet.Column:
        self.visible = False
        return flet.Column(
            alignment=flet.MainAxisAlignment.CENTER,
            controls=[
                flet.Row(
                    alignment=flet.MainAxisAlignment.CENTER,
                    controls=[
                        flet.Text("Dict Page")
                    ]
                )
            ]
        )


class LearningComponent(flet.UserControl):
    pages: dict[str, flet.UserControl] = {
        'abc_page': AbcComponent(),
        'dict_page': DictComponent(),
        'grammar_page': GrammarComponent()
    }

    def __init__(self) -> None:
        super().__init__()

    def build(self) -> flet.Column:

        self.learning_menu = flet.Column(
            controls=[
                flet.Row(
                    controls=[
                        flet.IconButton(
                            icon=flet.icons.ABC,
                            icon_size=40,
                            icon_color=flet.colors.GREY,
                            style=flet.ButtonStyle(
                                shape=flet.RoundedRectangleBorder(radius=13),
                                bgcolor=flet.colors.GREY_800
                            ),
                            on_click=lambda e: self.on_button_click(event=e, page='abc_page')
                        ),
                        flet.IconButton(
                            icon=flet.icons.MENU_BOOK,
                            icon_size=40,
                            icon_color=flet.colors.GREY,
                            style=flet.ButtonStyle(
                                shape=flet.RoundedRectangleBorder(radius=13),
                                bgcolor=flet.colors.GREY_800
                            ),
                            on_click=lambda e: self.on_button_click(event=e, page='dict_page')
                        ),
                    ],
                    alignment=flet.MainAxisAlignment.CENTER,
                ),

                flet.Row(
                    controls=[
                        flet.IconButton(
                            icon=flet.icons.ASSIGNMENT_RETURNED,
                            icon_size=40,
                            icon_color=flet.colors.GREY,
                            style=flet.ButtonStyle(
                                shape=flet.RoundedRectangleBorder(radius=13),
                                bgcolor=flet.colors.GREY_800
                            ),
                            on_click=lambda e: self.on_button_click(event=e, page='grammar_page')
                        )
                    ],
                    alignment=flet.MainAxisAlignment.CENTER
                ),
            ],
            alignment=flet.MainAxisAlignment.CENTER
        )

        end_column: flet.Column = flet.Column(controls=[self.learning_menu], alignment=flet.MainAxisAlignment.CENTER)
        [end_column.controls.append(page) for page in self.pages.values()]

        return end_column

    def reload(self) -> None:
        self.learning_menu.visible = True

        for page in self.pages:
            self.pages[page].visible = False

        self.update()

    def on_button_click(self, event: flet.ControlEvent, page: str) -> None:
        self.learning_menu.visible = False

        for key, value in self.pages.items():
            value.visible = True if key == page else False

        self.update()
