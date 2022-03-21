import sublime
import sublime_plugin


class SwitchStyleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        s = sublime.load_settings("Preferences.sublime-settings")
        current = s.get("font_face")

        if current == "Consolas":
            s.set("font_size", 18)
            s.set("font_face", "Georgia")
            s.set("line_numbers", False)
        elif current == "Georgia":
            s.set("font_size", 18)
            s.set("font_face", "Nexa Light")
            s.set("line_numbers", False)
        else:
            s.set("font_size", 12)
            s.set("font_face", "Consolas")
            s.set("line_numbers", True)

        sublime.save_settings("Preferences.sublime-settings")