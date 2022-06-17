from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# custom usermodel  사용시 UserManager class와 create_user, create_superuser 함수가 정의 되어있어야한다.
class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('username must not be empty')
        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db) # 이게모지
        return user
    
    #createsuperuser
    def create_superuser(self, username, password=None):
        user = self.create_user(
            username=username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser):
    username = models.CharField("사용자 계정", max_length=20, unique=True)
    email = models.EmailField("이메일 주소", max_length=100)
    password = models.CharField("비밀번호", max_length=128)
    fullname = models.CharField("이름", max_length=20)
    join_date = models.DateTimeField("가입일", auto_now_add=True)
    
    
    #is_active False일 경우 계정 비활성화
    is_active = models.BooleanField(default=True)
    
    #is_staff 에서 해당 값 사용
    is_admin = models.BooleanField(default=False)
    
    #id로 사용할 필드 지정 custom User 모델 사용시 필수적으로 설정해야됨.
    #로그인 시 USERNAME_FIELD에 설정된 필드와 password가 사용됨
    USERNAME_FIELD = 'username'
    
    #user를 생성할 때 입력받은 필드 지정 email, fullname 등을 리스트안에 넣으면 superuser 생성할때 입력칸이 생김
    REQUIRED_FIELDS = []
    
    objects = UserManager() #custom user 생성시 필요
    
    def __str__(self):
        return self.username
    
    
    # 로그인 사용자의 특정 테이블의 crud 권한을 설정, perm table의 crud 권한이 들어간다.
    # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
    def has_perm(self, perm, obj=None):
        return True
    
    # 로그인 사용자의 특정 app에 접근 가능 여부를 설정, app_label에는 app 이름이 들어간다.
    # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
    def has_module_perms(self, app_label): 
        return True
    
    # admin 권한 설정
    @property
    def is_staff(self): 
        return self.is_admin


class Hobby(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name="유저", on_delete=models.CASCADE)
    introduction = models.TextField("자기소개", max_length=255)
    birthday = models.DateTimeField("생일")
    age = models.IntegerField("나이")
    hobby = models.ManyToManyField(Hobby, verbose_name="취미")
    
    
    def __str__(self):
        return f"{self.user.username} 님의 프로필입니다."
    
    
    
    
    
    
    
    
    
    