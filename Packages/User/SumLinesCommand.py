import sublime
import sublime_plugin
import re
from datetime import datetime

class Helper:
	def process_timestamp_line(currentline):
		try:
			timestamp_a = currentline[0:19]
			timestamp_b = currentline[-19:]
			datetime1 = datetime.strptime(timestamp_a, '%Y-%m-%d %H:%M:%S')
			datetime2 = datetime.strptime(timestamp_b, '%Y-%m-%d %H:%M:%S')
			return (datetime2 - datetime1).seconds / 60
		except Exception as e:
			return 0

class SumLinesCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		sum = 0

		nextstart = 0
		nothingcount = 0
		oldnextstart = 0
		nextnextstart = 0
		mode = "Numbers"
		mode_search = True

		timestamp_pattern = re.compile("^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.*")
		while True:
			currentline = view.substr(view.line(nextstart))

			#                                   da kommt schon nichts mehr danach
			if nothingcount < 10 and nextstart != nextnextstart - 1:
				num = 0

				if mode == "Numbers":
					try:
						num = float(currentline)
						mode_search = False
					except Exception as e:
						num = 0
						try:
							num = float(currentline.split(" ")[0].replace(',', '.'))
						except Exception as e:
							try:
								num = float(currentline.split("\t")[0].replace(',', '.'))
							except Exception as e:
								num = 0
								if timestamp_pattern.match(currentline) != None:
									mode = "Timestamps"
									mode_search = False
									num = Helper.process_timestamp_line(currentline)

				elif mode == "Timestamps":
					if timestamp_pattern.match(currentline) != None:
						num = Helper.process_timestamp_line(currentline)

					
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

		if mode == "Numbers":
			view.insert(edit, nextstart - 101, "\n\nThe sum of all lines starting with one number is " + str(round(sum, 6)))
		elif mode == "Timestamps":
			view.insert(edit, nextstart - 101, "\n\nThe sum of all timestamps is " + str(round(sum)) + " minutes == " + str(round(sum / 60, 2)) + " hours")

