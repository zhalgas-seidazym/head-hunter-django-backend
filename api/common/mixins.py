from rest_framework import permissions


class ActionSerializerMixin:
    serializers = {}
    default_serializer_class = None  # опционально

    def get_serializer_class(self):
        """Return serializer class based on action."""
        if hasattr(self, "serializers") and self.action in self.serializers:
            return self.serializers[self.action]

        if self.default_serializer_class is not None:
            return self.default_serializer_class

        if hasattr(self, "serializer_class") and self.serializer_class is not None:
            return self.serializer_class

        raise AssertionError(
            f"'{self.__class__.__name__}' should include a 'serializer_class', "
            f"'default_serializer_class', or entry for action '{self.action}' in 'serializers'."
        )



class ActionPermissionMixin:
    DEFAULT_PERMISSION_CLASS = permissions.IsAuthenticated
    permissions = {}

    def get_permissions(self):
        if self.action in self.permissions:
            return [
                permission()
                for permission in self.permissions[self.action]
            ]

        return [self.DEFAULT_PERMISSION_CLASS()]