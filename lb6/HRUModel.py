class HRUModel:
    def __init__(self, num_users, num_objects):
        self.num_users = num_users
        self.num_objects = num_objects
        self.access_matrix = [[0] * num_objects for _ in range(num_users)]

    def grant_access(self, user_id, object_id):
        if user_id < self.num_users and object_id < self.num_objects:
            self.access_matrix[user_id][object_id] = 1
            print(f"Пользователь {user_id} получил доступ к объекту {object_id}.")
        else:
            print("Некорректные идентификаторы пользователя или объекта.")

    def revoke_access(self, user_id, object_id):
        if user_id < self.num_users and object_id < self.num_objects:
            self.access_matrix[user_id][object_id] = 0
            print(f"Доступ пользователя {user_id} к объекту {object_id} отозван.")
        else:
            print("Некорректные идентификаторы пользователя или объекта.")

    def check_access(self, user_id, object_id):
        if user_id < self.num_users and object_id < self.num_objects:
            access = self.access_matrix[user_id][object_id]
            if access == 1:
                print(f"Пользователь {user_id} имеет доступ к объекту {object_id}.")
            else:
                print(f"Пользователь {user_id} не имеет доступа к объекту {object_id}.")
        else:
            print("Некорректные идентификаторы пользователя или объекта.")


if __name__ == '__main__':
    hru = HRUModel(num_users=3, num_objects=5)
    hru.grant_access(0, 2)
    hru.grant_access(1, 3)
    hru.check_access(0, 2)
    hru.check_access(1, 2)
    hru.revoke_access(0, 2)
    hru.check_access(0, 2)
