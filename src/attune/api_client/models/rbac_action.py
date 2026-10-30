from enum import Enum


class RbacAction(str, Enum):
    CANCEL = "cancel"
    CONFIGURE = "configure"
    CREATE = "create"
    DECRYPT = "decrypt"
    DELETE = "delete"
    EXECUTE = "execute"
    INSTALL = "install"
    MANAGE = "manage"
    READ = "read"
    RESPOND = "respond"
    UPDATE = "update"
    USE = "use"

    def __str__(self) -> str:
        return str(self.value)
