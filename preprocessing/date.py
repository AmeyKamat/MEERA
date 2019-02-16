from datetime import datetime
import parsedatetime

class DatePreprocessor(object):

	calender = parsedatetime.Calendar()

	def preprocess(self, date):
		timeStruct, parseStatus = self.calender.parse("date")
		parsedDate = datetime(*timeStruct[:6])

		return { 
			"date": date,
			"parsedDate": parsedDate
		 }