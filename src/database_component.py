import flet
import ftplib
from settings import SETTINGS


class DatabaseComponent(flet.Column):
    def reload(self) -> None:
        pass

    def build(self):
        # Defs

        def show_word_video(event: flet.ControlEvent) -> None:
            self.page.session.get('show_letter')(event, True)

        # Variables

        ftp: ftplib.FTP = ftplib.FTP(
            host=SETTINGS.FTP_SETTINGS.ADDRESS,
            user=SETTINGS.FTP_SETTINGS.USER,
            passwd=SETTINGS.FTP_SETTINGS.PASSWORD
        )

        words: list = [word.replace('words/', '').replace('.mp4', '') for word in ftp.nlst('words')]
        ftp.close()

        words.remove('.')
        words.remove('..')
        words.sort()

        word_column: flet.Column = flet.Column(alignment=flet.MainAxisAlignment.CENTER)
        new_row: flet.Row = flet.Row(alignment=flet.MainAxisAlignment.SPACE_BETWEEN)

        for word in words[26:]:
            new_row.controls.append(
                flet.FilledButton(
                    text=word,
                    data=word,
                    on_click=show_word_video,
                    style=flet.ButtonStyle(
                        shape=flet.RoundedRectangleBorder(radius=10),
                        bgcolor=flet.colors.SURFACE_VARIANT,
                        color=flet.colors.PRIMARY
                    )
                )
            )

            if len(new_row.controls) == 2:
                word_column.controls.append(new_row)
                new_row: flet.Row = flet.Row(alignment=flet.MainAxisAlignment.SPACE_BETWEEN)

        word_column.controls.append(new_row)

        self.controls.append(
            flet.SafeArea(
                content=flet.Column(
                    controls=[
                        flet.SearchBar(
                            height=40,
                            bar_leading=flet.Icon(name=flet.icons.SEARCH),
                            view_shape=flet.RoundedRectangleBorder(radius=10),
                            controls=[flet.ListTile(title=flet.Text(word), data=word, on_click=show_word_video) for word in words]
                        ),
                        word_column,
                    ]
                )
            )
        )
