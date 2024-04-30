import flet
from src.client.abc_fragment import ABCFragment
from src.client.grammar_fragment import GrammarFragment
from src.client.dict_fragment import DictFragment


class LearningComponent(flet.Column):
    def reload(self) -> None:
        self.controls[-1].visible = True
        for fragment in self.fragments:
            fragment.visible = False

        self.update()

    def build(self):
        # Setting component
        self.alignment = flet.MainAxisAlignment.CENTER

        # Defs

        def open_fragment(event: flet.ControlEvent, fragment_id: int) -> None:
            self.controls[-1].visible = False
            self.fragments[fragment_id].visible = True
            self.update()

        # Variables

        self.fragments: list = [
            flet.Container(
                content=ABCFragment(),
                visible=False,
                expand=True
            ),
            flet.Container(
                content=DictFragment(),
                visible=False,
                expand=True
            ),
            flet.Container(
                content=GrammarFragment(),
                visible=False,
                expand=True
            )
        ]

        self.controls.extend([
            self.fragments[0],
            self.fragments[1],
            self.fragments[2],
            flet.Column(
                controls=[
                    flet.Row(
                        alignment=flet.MainAxisAlignment.CENTER,
                        controls=[
                            flet.IconButton(
                                icon=flet.icons.ABC,
                                icon_size=40,
                                on_click=lambda event: open_fragment(event, 0),
                                style=flet.ButtonStyle(
                                    shape=flet.RoundedRectangleBorder(radius=10),
                                    bgcolor=flet.colors.SURFACE_VARIANT
                                )
                            ),
                            flet.IconButton(
                                icon=flet.icons.MENU_BOOK,
                                icon_size=40,
                                on_click=lambda event: open_fragment(event, 1),
                                style=flet.ButtonStyle(
                                    shape=flet.RoundedRectangleBorder(radius=10),
                                    bgcolor=flet.colors.SURFACE_VARIANT
                                )
                            )
                        ]
                    ),
                    flet.Row(
                        alignment=flet.MainAxisAlignment.CENTER,
                        controls=[
                            flet.IconButton(
                                icon=flet.icons.ASSIGNMENT_RETURNED,
                                icon_size=40,
                                on_click=lambda event: open_fragment(event, 2),
                                style=flet.ButtonStyle(
                                    shape=flet.RoundedRectangleBorder(radius=10),
                                    bgcolor=flet.colors.SURFACE_VARIANT
                                )
                            )
                        ]
                    )
                ]
            )
        ])
