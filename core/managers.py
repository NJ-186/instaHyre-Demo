from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, phone, name, password = None, **extra_fields):

        if not phone:
            raise ValueError('Users must have a phone number')
        if not name:
            raise ValueError('Users must have a name')

        user = self.model(
            phone = phone,
            name = name,
            **extra_fields
        )

        user.set_password(password)
        user.save(using = self._db)

        return user

    def create_superuser(self, phone, name, password = None, **extra_fields):
    
        user = self.create_user(
            phone = phone,
            name = name,
            password = password,
            **extra_fields
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using = self._db)
        
        return user