from datetime import datetime
import parsedatetime

class DatePreprocessor:

    calender = parsedatetime.Calendar()

    def preprocess(self, date):
        time_struct = self.calender.parse("date")[0]
        parsed_date = datetime(*time_struct[:6])

        return {
            "date": date,
            "parsedDate": parsed_date
        }
