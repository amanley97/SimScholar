# ----------------------------------------------------------------------------
# NOTICE: This code is the exclusive property of University of Kansas
#         Architecture Research and is strictly confidential.
#
#         Unauthorized distribution, reproduction, or use of this code, in
#         whole or in part, is strictly prohibited. This includes, but is
#         not limited to, any form of public or private distribution,
#         publication, or replication.
#
# For inquiries or access requests, please contact:
#         Alex Manley (amanley97@ku.edu)
#         Mahmudul Hasan (m.hasan@ku.edu)
# ----------------------------------------------------------------------------

from tkinter import ttk


class SimScholarStyling:
    def __init__(self) -> None:
        pass

    def apply_style(self, theme):
        style = ttk.Style()

        if theme == "darkmode":
            style.theme_create(
                "darkmode",
                parent="alt",
                settings={
                    "TNotebook": {
                        "configure": {
                            "background": "#333333",
                            "foreground": "white",
                            "borderwidth": 2,
                        }
                    },
                    "TNotebook.Tab": {
                        "configure": {
                            "background": "#444444",
                            "foreground": "white",
                            "padding": [5, 1],
                            "borderwidth": 2,
                            "relief": "raised",
                        },
                        "map": {
                            "background": [("selected", "#222222")],
                            "foreground": [("selected", "#ffffff")],
                            "expand": [("selected", [1, 1, 1, 0])],
                        },
                    },
                    "TFrame": {"configure": {"background": "#333333"}},
                    "TLabel": {
                        "configure": {"background": "#333333", "foreground": "white"}
                    },
                    "TCombobox": {
                        "configure": {
                            "selectbackground": "#444444",
                            "fieldbackground": "#444444",
                            "background": "#333333",
                            "foreground": "white",
                        }
                    },
                    "TEntry": {
                        "configure": {
                            "fieldbackground": "#444444",
                            "background": "#333333",
                            "foreground": "white",
                        }
                    },
                    "TButton": {
                        "configure": {
                            "background": "#444444",
                            "foreground": "white",
                            "padding": [10, 5],
                            "anchor": "center",
                            "relief": "raised",
                            "borderwidth": 2,
                        },
                        "map": {
                            "background": [("active", "#555555")],
                            "foreground": [("active", "white")],
                        },
                    },
                    "TRadiobutton": {
                        "configure": {
                            "background": "#333333",
                            "foreground": "white",
                            "indicatorbackground": "#333333",
                            "selectcolor": "#444444",
                        },
                        "map": {
                            "background": [("active", "#555555")],
                            "foreground": [("active", "white")],
                        },
                    },
                },
            )
            style.theme_use("darkmode")

        elif theme == "lightmode":
            style.theme_create(
                "lightmode",
                parent="alt",
                settings={
                    "TNotebook": {
                        "configure": {
                            "background": "#f0f0f0",
                            "foreground": "black",
                            "borderwidth": 2,
                        }
                    },
                    "TNotebook.Tab": {
                        "configure": {
                            "background": "#e0e0e0",
                            "foreground": "black",
                            "padding": [5, 1],
                            "borderwidth": 2,
                            "relief": "raised",
                        },
                        "map": {
                            "background": [("selected", "#d0d0d0")],
                            "foreground": [("selected", "#000000")],
                            "expand": [("selected", [1, 1, 1, 0])],
                        },
                    },
                    "TFrame": {"configure": {"background": "#f0f0f0"}},
                    "TLabel": {
                        "configure": {"background": "#f0f0f0", "foreground": "black"}
                    },
                    "TCombobox": {
                        "configure": {
                            "selectbackground": "#e0e0e0",
                            "fieldbackground": "#e0e0e0",
                            "background": "#f0f0f0",
                            "foreground": "black",
                        }
                    },
                    "TEntry": {
                        "configure": {
                            "fieldbackground": "#e0e0e0",
                            "background": "#f0f0f0",
                            "foreground": "black",
                        }
                    },
                    "TButton": {
                        "configure": {
                            "background": "#e0e0e0",
                            "foreground": "black",
                            "padding": [10, 5],
                            "anchor": "center",
                            "relief": "raised",
                            "borderwidth": 2,
                        },
                        "map": {
                            "background": [("active", "#d0d0d0")],
                            "foreground": [("active", "black")],
                        },
                    },
                    "TRadiobutton": {
                        "configure": {
                            "background": "#f0f0f0",
                            "foreground": "black",
                            "indicatorbackground": "#f0f0f0",
                            "selectcolor": "#e0e0e0",
                        },
                        "map": {
                            "background": [("active", "#d0d0d0")],
                            "foreground": [("active", "black")],
                        },
                    },
                },
            )
            style.theme_use("lightmode")
