import sublime
import sublime_plugin

import datetime

class VerrechenbarCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		sum = 0
		sumVerrechenbar = 0
		sumVerkauf = 0

		nextstart = 0
		nothingcount = 0
		oldnextstart = 0
		nextnextstart = 0
		while True:
			currentline = view.substr(view.line(nextstart))

			#                                   da kommt schon nichts mehr danach
			if nothingcount < 10 and nextstart != nextnextstart - 1:
				num = 0
				try:
					num = float(currentline)
				except Exception as e:
					num = 0
					try:
						num = float(currentline.split(" ")[0].replace(',', '.'))
					except Exception as e:
						num = 0

				sum += num
				if currentline.endswith(" P"):
					sumVerrechenbar += num
				elif currentline.endswith(" V"):
					sumVerkauf += num



			oldnextstart = nextstart
			nextstart = view.line(nextstart).b + 1
			# um zu prüfen, ob nach nextstart was sinnvolles kommt. Wenn nicht, ist wsl schon Schluss
			nextnextstart = view.line(nextstart).b + 1
			#print("o:", oldnextstart, "n:", nextstart, "nn:", nextnextstart)

			if nextstart - oldnextstart == 1:
				nothingcount += 1

				if nothingcount == 100:
					# nach hundert Mal nichts ist die Datei wahrscheinlich zu Ende ...
					break
			else:
				nothingcount = 0

		now = datetime.datetime.now()
		td = datetime.timedelta(hours=sum)
		since = now - td
		view.insert(edit, nextstart - 101, "\n\nEs wurden " + str(sum) + " Std. gearbeitet zu " + str(int((sumVerrechenbar * 100.0) / sum)) + "% verr. (" + str(sumVerrechenbar) + " verr. Std.)\n" +
			"Außerdem " + str(int((sumVerkauf * 100.0) / sum)) + "% Verkauf (insg. " + str(sumVerkauf) + " Std.)")
