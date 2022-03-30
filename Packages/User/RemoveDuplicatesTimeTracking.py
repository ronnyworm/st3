import sublime
import sublime_plugin
import re
from datetime import datetime

class RemoveDuplicatesTimeTracking(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view

        nextstart = 0
        nothingcount = 0
        oldnextstart = 0
        nextnextstart = 0
        iterations = 0
        insert_count = 0
        time_record_pattern = re.compile("^\d{2}.\d{2}.\d{4}\t.*\t.*")
        last_nextstart = []
        last_date = ""
        last_hours = 0
        last_text = ""

        #print("new run")

        while True:
            currentline = view.substr(view.line(nextstart))

            #                                   da kommt schon nichts mehr danach
            if nothingcount < 10 and nextstart != nextnextstart - 1:
                if time_record_pattern.match(currentline) != None:
                    try:
                        arr = currentline.split("\t")
                        date = arr[0]
                        hours = float(arr[1].replace(",", "."))
                        text = arr[2]

                        if iterations != 0:
                            last_call_with_write = False
                            if date == last_date and text == last_text:
                                hours += last_hours
                                #print("h: " + str(hours))
                                last_call_with_write = True
                                last_nextstart.append(nextstart)
                                #print("ln: " + str(last_nextstart))
                            else:
                                if len(last_nextstart) > 1:
                                    #print("do itX " + last_text)
                                    view.insert(edit, nextstart, date + "\t" + str(round(last_hours, 2)).replace(".", ",") + "\t-> SUM " + last_text + "\n")
                                    insert_count += 1
                                    date = ""
                                    # don't actually remove for now
                                    #for i in range(0, len(last_nextstart)):
                                    #    view.replace(edit, view.full_line(last_nextstart[0]), "")
                                last_nextstart = [nextstart]

                        iterations += 1

                        last_date = date
                        last_hours = hours
                        last_text = text

                    except Exception as e:
                        pass
                else:
                    if len(last_nextstart) > 1:
                        #print("do itY " + text)
                        view.insert(edit, oldnextstart, date + "\t" + str(round(last_hours, 2)).replace(".", ",") + "\t-> SUM " + text + "\n")
                        insert_count += 1
                        # don't actually remove for now
                        #for i in range(0, len(last_nextstart)):
                        #    view.replace(edit, view.full_line(last_nextstart[0]), "")

                    last_nextstart = []



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

        view.insert(edit, nextstart - 101, "\n\nDuplicate removal inserted  " + str(insert_count) + " line(s)")