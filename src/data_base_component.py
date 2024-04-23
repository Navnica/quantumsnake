import flet
import ftplib
from settings import SETTINGS
from random import randint


class DataBaseComponent(flet.UserControl):
    def __init__(self) -> None:
        super().__init__()

    def build(self):
        def on_word_press(letter: str):
            def video_replay(event: flet.ControlEvent) -> None:
                video.jump_to(0)


            video: flet.Video = flet.Video(
                playlist=[flet.VideoMedia(f'{SETTINGS.VIDEO_DIR_PATH}/words/{letter}.mp4')],
                autoplay=True,
                show_controls=False,
                aspect_ratio=4 / 3,
            )

            alert_dialog: flet.AlertDialog = flet.AlertDialog(
                modal=False,
                content=flet.Column(
                    controls=[
                        video
                        ,
                        flet.Row(
                            controls=[
                                flet.IconButton(
                                    icon=flet.icons.REPLAY,
                                    icon_size=20,
                                    icon_color=flet.colors.GREY,
                                    style=flet.ButtonStyle(
                                        shape=flet.RoundedRectangleBorder(radius=13),
                                        bgcolor=flet.colors.GREY_800
                                    ),
                                    on_click=video_replay
                                )
                            ],
                            alignment=flet.MainAxisAlignment.CENTER
                        )

                    ],
                    alignment=flet.MainAxisAlignment.START,
                    height=240
                )
            )

            self.page.dialog = alert_dialog
            alert_dialog.open = True
            self.page.update()

        ftp = ftplib.FTP(
            host=SETTINGS.FTP_SETTINGS.ADDRESS,
            user=SETTINGS.FTP_SETTINGS.USER,
            passwd=SETTINGS.FTP_SETTINGS.PASSWORD
        )

        video_list: list[str] = ftp.nlst('words')
        video_list = [word.replace('.mp4', '').replace('words', '').replace('/', '').replace('..', '').replace('.', '')
                      for word in video_list]

        column: flet.Column = flet.Column(alignment=flet.MainAxisAlignment.CENTER)
        new_row: flet.Row = flet.Row(alignment=flet.MainAxisAlignment.CENTER)

        for word in video_list[25:]:
            if word == '':
                video_list.remove(word)
                continue

            new_row.controls.append(flet.FilledButton(
                text=word,
                on_click=lambda _: on_word_press(word),
                style=flet.ButtonStyle(
                    shape=flet.RoundedRectangleBorder(radius=8),
                    bgcolor=flet.colors.GREY_800,
                    color=flet.colors.WHITE
                ),
            ))

            if len(new_row.controls) == 2:
                column.controls.append(new_row)
                new_row = flet.Row(alignment=flet.MainAxisAlignment.CENTER)

        column.controls.append(new_row)

        search_bar = flet.SearchBar(
            view_elevation=4,
            divider_color=flet.colors.AMBER,
            controls=[
                flet.ListTile(title=flet.Text(value=word), data=word, on_click=lambda _: on_word_press(word)) for word in video_list
            ]
        )

        return flet.Column(
            alignment=flet.MainAxisAlignment.END,
            controls=[
                column,
                search_bar
            ]
        )

    def reload(self) -> None:
        pass
