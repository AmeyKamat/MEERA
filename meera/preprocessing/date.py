from datetime import datetime
import parsedatetime

class DatePreprocessor:

    calender = parsedatetime.Calendar()

    def preprocess(self, date):
        timeStruct = self.calender.parse("date")[0]
        parsedDate = datetime(*timeStruct[:6])

        return { 
            "date": date,
            "parsedDate": parsedDate
         }