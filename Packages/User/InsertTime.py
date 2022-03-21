import sublime
import sublime_plugin

import datetime

class InsertTimeCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		selection = view.sel()

		view.insert(edit, selection[0].begin(), str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
