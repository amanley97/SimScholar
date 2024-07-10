ttk::style theme create darkmode -parent alt -settings {
    ttk::style configure TNotebook -background #333333 -foreground white -borderwidth 2
    ttk::style configure TNotebook.Tab -background #444444 -foreground white -padding {5 1} -borderwidth 2 -relief raised
    ttk::style map TNotebook.Tab -background {selected #222222} -foreground {selected white} -expand {selected {1 1 1 0}}

    ttk::style configure TFrame -background #333333
    ttk::style configure TLabel -background #333333 -foreground white
    ttk::style configure TCombobox -selectbackground #444444 -fieldbackground #444444 -background #333333 -foreground white
    ttk::style configure TEntry -fieldbackground #555555 -background #333333 -foreground white
    ttk::style configure TButton -background #444444 -foreground white -padding {10 5} -anchor center -relief raised -borderwidth 2
    ttk::style map TButton -background {active #555555} -foreground {active white}

    ttk::style configure TRadiobutton -background #333333 -foreground black
    ttk::style map TRadiobutton -background {active #666666 !active #777777}
    ttk::style configure TMenubutton -background #555555 -foreground white -arrowcolor white
    ttk::style map TMenubutton -background {active #666666} -foreground {active white}

    ttk::style configure TOptionMenu -background #555555 -foreground white -arrowcolor white
    ttk::style configure TEntry.Disabled -fieldbackground #222222 -foreground #777777

    ttk::style configure TMenu -background #333333 -foreground white
    ttk::style map TMenu -background {active #444444} -foreground {active white}
}

ttk::style theme create lightmode -parent alt -settings {
    ttk::style configure TNotebook -background #f0f0f0 -foreground black -borderwidth 2
    ttk::style configure TNotebook.Tab -background #e0e0e0 -foreground black -padding {5 1} -borderwidth 2 -relief raised
    ttk::style map TNotebook.Tab -background {selected #d0d0d0} -foreground {selected black} -expand {selected {1 1 1 0}}

    ttk::style configure TFrame -background #f0f0f0
    ttk::style configure TLabel -background #f0f0f0 -foreground black
    ttk::style configure TCombobox -selectbackground #e0e0e0 -fieldbackground #e0e0e0 -background #f0f0f0 -foreground black
    ttk::style configure TEntry -fieldbackground #e0e0e0 -background #f0f0f0 -foreground black
    ttk::style configure TButton -background #e0e0e0 -foreground black -padding {10 5} -anchor center -relief raised -borderwidth 2
    ttk::style map TButton -background {active #d0d0d0} -foreground {active black}

    ttk::style configure TRadiobutton -background #f0f0f0 -foreground black
    ttk::style map TRadiobutton -background {active #d0d0d0 !active #c0c0c0}
    ttk::style configure TMenubutton -background #d0d0d0 -foreground black -arrowcolor black
    ttk::style map TMenubutton -background {active #c0c0c0} -foreground {active black}

    ttk::style configure TOptionMenu -background #d0d0d0 -foreground black -arrowcolor black
    ttk::style configure TEntry.Disabled -fieldbackground #a0a0a0 -foreground #777777

    ttk::style configure TMenu -background #f0f0f0 -foreground black
    ttk::style map TMenu -background {active #e0e0e0} -foreground {active black}
}

ttk::style theme create navymode -parent alt -settings {
    ttk::style configure TNotebook -background #001f3f -foreground white -borderwidth 2
    ttk::style configure TNotebook.Tab -background #003366 -foreground white -padding {5 1} -borderwidth 2 -relief raised
    ttk::style map TNotebook.Tab -background {selected #001a33} -foreground {selected white} -expand {selected {1 1 1 0}}

    ttk::style configure TFrame -background #001f3f
    ttk::style configure TLabel -background #001f3f -foreground white
    ttk::style configure TCombobox -selectbackground #003366 -fieldbackground #003366 -background #001f3f -foreground white
    ttk::style configure TEntry -fieldbackground #002244 -background #001f3f -foreground white
    ttk::style configure TButton -background #003366 -foreground white -padding {10 5} -anchor center -relief raised -borderwidth 2
    ttk::style map TButton -background {active #004080} -foreground {active white}

    ttk::style configure TRadiobutton -background #001f3f -foreground black
    ttk::style map TRadiobutton -background {active #003377 !active #003366}
    ttk::style configure TMenubutton -background #003366 -foreground white -arrowcolor white
    ttk::style map TMenubutton -background {active #004080} -foreground {active white}

    ttk::style configure TOptionMenu -background #003366 -foreground white -arrowcolor white
    ttk::style configure TEntry.Disabled -fieldbackground #001a33 -foreground #777777

    ttk::style configure TMenu -background #001f3f -foreground white
    ttk::style map TMenu -background {active #003366} -foreground {active white}
}
