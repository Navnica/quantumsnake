import asyncio
import flet


class TestCreateFragment(flet.SafeArea):
    def __init__(self, par: flet.SafeArea) -> None:
        super().__init__()
        self.par = par

    async def show_icon_select_panel(self, event: flet.ControlEvent) -> None:
        self.content.controls[2].visible = True
        self.content.controls[2].open_view()
        self.update()

    async def on_search_bar_change(self, event: flet.ControlEvent) -> None:
        async def on_select_icon(event: flet.ControlEvent) -> None:
            self.content.controls[1].icon = event.control.data
            self.content.controls[2].close_view()
            await asyncio.sleep(0.1)
            self.content.controls[2].visible = False
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
                flet.IconButton(
                    icon=flet.icons.EMOJI_EMOTIONS,
                    icon_size=80,
                    on_click=self.show_icon_select_panel,
                    style=flet.ButtonStyle(
                        shape=flet.RoundedRectangleBorder(
                            radius=15
                        ),
                        bgcolor=flet.colors.SURFACE_VARIANT
                    )
                ),
                flet.SearchBar(
                    visible=False,
                    view_leading=flet.Container(),
                    view_trailing=[flet.Container()],
                    bar_hint_text="Выбор иконки",
                    full_screen=True,
                    controls=[self.search_bar_content],
                    on_change=self.on_search_bar_change
                )
            ]
        )
