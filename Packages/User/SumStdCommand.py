import re
import sublime
import sublime_plugin

class SumStdCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		sum = 0

		nextstart = 0
		nothingcount = 0
		oldnextstart = 0
		nextnextstart = 0
		keyword = "Std"
		while True:
			currentline = view.substr(view.line(nextstart))

			# da kommt schon nichts mehr danach
			if nothingcount < 10 and nextstart != nextnextstart - 1:
				num = 0

				stdpattern = re.compile(".*?(?P<num>[0-9,.]+) ?" + keyword + ".*")
				the_split = currentline.split(keyword)

				for idx, part in enumerate(the_split):
					if idx < len(the_split) - 1:
						m = stdpattern.match(part + keyword)
						if m:
							try:
								found = m.group("num")
								num += float(found.replace(',', '.'))
							except Exception as e:
								pass
				sum += num



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

		view.insert(edit, nextstart - 101, "\n\nThe sum of all " + keyword + " contained is " + str(round(sum, 6)))