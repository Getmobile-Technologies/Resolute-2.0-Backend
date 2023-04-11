from django.contrib.auth.base_user import BaseUserManager







class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not phone:
            raise ValueError('The given phone must be set')
        user = self.model(phone=phone, **extra_fields)
        user.save(using=self._db)
        return user


    def create_superuser(self, phone, password=None, **extra_fields):
        user = self._create_user(phone, password, role='superuser', is_admin=True, is_staff=True, is_superuser=True, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        
        return user
    
    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        user=self._create_user(phone, password, is_staff=True, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user


    def create_admin(self, phone, password=None, **extra_fields):
        user = self._create_user(phone, password, is_admin=True, is_staff=True, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        
        return user

