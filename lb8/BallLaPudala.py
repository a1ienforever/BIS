class BellLaPadulaModel:
    def __init__(self):
        self.subjects = {}
        self.objects = {}

    def add_subject(self, subject, clearance):
        self.subjects[subject] = clearance

    def add_object(self, obj, classification):
        self.objects[obj] = classification

    def can_read(self, subject, obj):
        if subject not in self.subjects or obj not in self.objects:
            return False
        subject_clearance = self.subjects[subject]
        obj_classification = self.objects[obj]
        return subject_clearance >= obj_classification

    def can_write(self, subject, obj):
        if subject not in self.subjects or obj not in self.objects:
            return False
        subject_clearance = self.subjects[subject]
        obj_classification = self.objects[obj]
        return subject_clearance <= obj_classification


if __name__ == '__main__':
    model = BellLaPadulaModel()

    # Добавление субъектов и объектов с классификацией
    model.add_subject("UserA", 1)
    model.add_subject("UserB", 3)

    model.add_object("File1", 3)
    model.add_object("File2", 2)

    # Проверка доступов
    print(model.can_read("UserA", "File1"))
    print(model.can_read("UserB", "File1"))
    print(model.can_write("UserA", "File2"))
    print(model.can_write("UserB", "File2"))
