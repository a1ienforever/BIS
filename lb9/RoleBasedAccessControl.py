class RoleBasedAccessControl:
    def __init__(self):
        self.users = {}
        self.roles = {}

    def add_user(self, user, roles):
        self.users[user] = roles

    def add_role(self, role, permissions, inherits=None):
        self.roles[role] = {"permissions": permissions, "inherits": inherits}

    def check_permission(self, user, permission):
        if user not in self.users:
            return False

        user_roles = self.users[user]
        checked_roles = set()

        while user_roles:
            role = user_roles.pop()
            if role not in checked_roles:
                if role in self.roles:
                    if permission in self.roles[role]["permissions"]:
                        return True
                    inherits = self.roles[role]["inherits"]
                    if inherits:
                        user_roles.extend(inherits)
                checked_roles.add(role)

        return False

# Пример использования:

# Создание модели
rbac = RoleBasedAccessControl()

# Добавление ролей с правами и наследованием
rbac.add_role("admin", ["read", "write", "delete"])
rbac.add_role("manager", ["read", "write"])
rbac.add_role("employee", ["read"])

# Наследование ролей
rbac.add_role("superadmin", [], inherits=["admin", "manager"])

# Добавление пользователей с ролями
rbac.add_user("user1", ["admin"])
rbac.add_user("user2", ["manager"])
rbac.add_user("user3", ["employee"])
rbac.add_user("user4", ["superadmin"])

# Проверка доступов
print(rbac.check_permission("user1", "read"))  # True, user1 имеет право на чтение (admin)
print(rbac.check_permission("user2", "delete"))  # False, user2 не имеет права на удаление (manager)
print(rbac.check_permission("user4", "write"))  # True, user4 имеет право на запись, так как унаследовано от admin
