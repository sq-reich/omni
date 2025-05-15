class NoLCD:
    def display_two_lines(self, *args, **kwargs):
        print("🖥️ [Kein LCD] →", *args)

    def display_text(self, *args, **kwargs):
        print("🖥️ [Kein LCD] →", *args)

    def scroll_text(self, *args, **kwargs):
        print("🖥️ [Kein LCD scroll]")

    def clear(self):
        print("🖥️ [LCD gelöscht]")
