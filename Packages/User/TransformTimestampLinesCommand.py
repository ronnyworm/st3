import sublime
import sublime_plugin
import re
from datetime import datetime

class TransformTimestampLinesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        sum = 0

        nextstart = 0
        nothingcount = 0
        oldnextstart = 0
        nextnextstart = 0
        write_target = ""

        timestamp_pattern = re.compile("^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.*")
        while True:
            currentline = view.substr(view.line(nextstart))

            #                                   da kommt schon nichts mehr danach
            if nothingcount < 10 and nextstart != nextnextstart - 1:
                if timestamp_pattern.match(currentline) != None:
                    try:
                        timestamp_a = currentline[0:19]
                        timestamp_b = currentline[-19:]
                        datetime1 = datetime.strptime(timestamp_a, '%Y-%m-%d %H:%M:%S')
                        datetime2 = datetime.strptime(timestamp_b, '%Y-%m-%d %H:%M:%S')
                        std = (datetime2 - datetime1).seconds / 60

                        text = currentline[20:-20]
                        view.insert(edit, nextstart, write_target)
                        write_target = datetime1.strftime("%d.%m.%Y") + "\t" + str(round(std / 60, 2)) + "\t" + text + "\n"
                    except Exception as e:
                        pass


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

