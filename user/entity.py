class Entity:
    def __init__(self, id, password, name, phone, email):
        self.id = id
        self.password = password
        self.name = name
        self.phone = phone
        self.email = email

    @property
    def id(self):
        return self.id
    @id.setter
    def id(self, id):
        self.id = id
    @property
    def password(self):
        return self.password
    @password.setter
    def password(self, password):
        self.password = password
    @property
    def name(self):
        return self.name
    @name.setter
    def name(self, name):
        self.name = name
    @property
    def phone(self):
        return self.phone
    @phone.setter
    def phone(self, phone):
        self.phone = phone
    @property
    def email(self):
        return self.email
    @email.setter
    def email(self, email):
        self.email = email