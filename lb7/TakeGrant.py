class TakeGrantModel:
    def __init__(self):
        self.graph = {}

    def add_subject(self, subject):
        if subject not in self.graph:
            self.graph[subject] = {}

    def add_object(self, subject, obj):
        if subject in self.graph:
            self.graph[subject][obj] = []

    def add_right(self, subject, obj, right):
        if subject in self.graph and obj in self.graph[subject]:
            self.graph[subject][obj].append(right)

    def verify_leak(self, subject, target_obj, visited=None):
        if visited is None:
            visited = set()

        visited.add(subject)

        if subject not in self.graph:
            return False

        for obj, rights in self.graph[subject].items():
            if obj == target_obj:
                return True
            for right in rights:
                if right == "grant" and obj not in visited:
                    if self.verify_leak(obj, target_obj, visited):
                        return True

        return False


if __name__ == '__main__':
    model = TakeGrantModel()

    model.add_subject("UserA")
    model.add_subject("UserB")

    model.add_object("UserA", "File1")
    model.add_object("UserA", "File2")

    model.add_right("UserA", "File1", "read")
    model.add_right("UserA", "File1", "write")
    model.add_right("UserA", "File2", "read")

    print(model.verify_leak("UserA", "File2"))
    print(model.verify_leak("UserB", "File1"))
