import flet
from settings import SETTINGS
import requests


class ABCFragment(flet.Column):
    def build(self) -> None:
        self.alignment = flet.MainAxisAlignment.CENTER

        # Defs

        def video_replay(event: flet.ControlEvent):
            self.page.dialog.content.controls[0].seek(0)

        def show_letter(event: flet.ControlEvent, word: bool = False) -> None:
            video_dialog: flet.AlertDialog = flet.AlertDialog(
                modal=False,
                open=True,
                shape=flet.RoundedRectangleBorder(radius=10),
                content=flet.Column(
                    alignment=flet.MainAxisAlignment.START,
                    horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                    height=250,
                    controls=[
                        flet.Video(
                            playlist=[flet.VideoMedia(resource=event.control.data)],
                            autoplay=True,
                            show_controls=False,
                            aspect_ratio=3 / 2,
                            height=500
                        ),
                        flet.Divider(height=10, color=flet.colors.SURFACE_VARIANT),
                        flet.FilledButton(
                            icon=flet.icons.REPLAY,
                            text='Пересмотреть',
                            on_click=video_replay,
                            style=flet.ButtonStyle(
                                shape=flet.RoundedRectangleBorder(radius=10),
                                bgcolor=flet.colors.SURFACE_VARIANT,
                                color=flet.colors.PRIMARY
                            )
                        )
                    ]
                )
            )

            self.page.dialog = video_dialog
            self.page.update()

        # Variables

        letters: list = []

        for letter in requests.get(SETTINGS.SERVER_URL + '/video_file/get_all', params={'token': SETTINGS.TOKEN}).json():
            if not letter['is_word']:
                letters.append(letter)

        letters.sort(key=lambda x: x['name'])
        letters.insert(6, letters[-1])
        letters = letters[:-1]

        abc_column: flet.Column = flet.Column(alignment=flet.MainAxisAlignment.CENTER, )
        new_row: flet.Row = flet.Row(alignment=flet.MainAxisAlignment.CENTER)

        for letter in letters:
            new_row.controls.append(
                flet.Container(
                    width=63,
                    content=flet.FilledButton(
                        width=60,
                        text=letter['name'].upper(),
                        on_click=show_letter,
                        data=letter['url'],
                        style=flet.ButtonStyle(
                            shape=flet.RoundedRectangleBorder(radius=8),
                            bgcolor=flet.colors.SURFACE_VARIANT,
                            color=flet.colors.WHITE
                        )
                    ))
            )

            if len(new_row.controls) == 5:
                abc_column.controls.append(new_row)
                new_row: flet.Row = flet.Row(alignment=flet.MainAxisAlignment.CENTER)

        abc_column.controls.append(new_row)

        self.page.session.set('show_letter', show_letter)

        self.controls.extend([
            abc_column
        ])
