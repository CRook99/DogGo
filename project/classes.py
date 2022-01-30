class Dog:
    def __init__(self, dog_id, user_id, name, age, sex, breed, lost, last_report, location):
        self.dog_id = dog_id
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sex = sex
        self.breed = breed
        self.lost = lost
        self.last_report = last_report
        self.location = location

class Report:
    def __init__(self, report_id, dog_id, user_id, location, date):
        self.report_id = report_id
        self.dog_id = dog_id
        self.user_id = user_id
        self.location = location
        self.date = date

