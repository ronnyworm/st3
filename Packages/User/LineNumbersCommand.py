import sublime
import sublime_plugin


class LineNumbersCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        s = sublime.load_settings("Preferences.sublime-settings")
        current = s.get("line_numbers")

        if current == False:
            s.set("line_numbers", True)
        else:
            s.set("line_numbers", False)

        sublime.save_settings("Preferences.sublime-settings")
