from rest_framework import serializers
from blog.serializers import ArticleSerializer

from blog.models import (
    Category as CategoryModel,
    Article as ArticleModel,
    Comment as CommentModel
    )

from user.models import (
    User as UserModel,
    UserProfile as UserProfileModel,
    Hobby as HobbyModel
)

VALID_EMAIL_LIST = ["naver.com", "gmail.com", "daum.net"]

class HobbySerializer(serializers.ModelSerializer):
    same_hobby_users = serializers.SerializerMethodField()
    
    def get_same_hobby_users(self, obj):
        user = self.context["request"].user
        
        return [up.user.username for up in obj.userprofile_set.exclude(user=user)]

    class Meta:
        model = HobbyModel
        fields = ["name", "same_hobby_users"]


class UserProfileSerializer(serializers.ModelSerializer):
    hobby = HobbySerializer(many=True, read_only=True)
    get_hobbys = serializers.ListField(required=False)
    
    class Meta:
        model = UserProfileModel
        fields = ["introduction", "birthday", "age", "hobby", "get_hobbys"]
        
        
class UserSerializer(serializers.ModelSerializer):  
    userprofile = UserProfileSerializer()
    articles = ArticleSerializer(many=True, source="article_set", read_only=True)
    # login_user_username = serializers.SerializerMethodField()
    
    # def get_login_user_username(self, obj):
    #     return self.context["request"].user.username
    
    def validate(self, data):
        
        # try:
        #     # POST, PUT 따로 이벤트 관리 할때 쓰는 법
        #     http_method = self.context.get("request", {}).method
        # except:
        #     http_method = ""
            
        # if http_method == "POST":
        
        if data.get("email", "").split('@')[-1] not in VALID_EMAIL_LIST:
            raise serializers.ValidationError(
                detail={"error": "유효한 이메일 주소가 아닙니다."}
            )
            
        return data
        
    def create(self, validated_data):
        # object를 생성할때 다른 데이터가 입력되는 것을 방지하기 위해 미리 pop 해준다.
        user_profile = validated_data.pop("userprofile")
        get_hobbys = user_profile.pop("get_hobbys", [])
        password = validated_data.pop("password")
        
        # User object 생성
        user = UserModel(**validated_data)
        #Password 해쉬 저장
        user.set_password(password)
        user.save()

        # UserProfile object 생성
        user_profile = UserProfileModel.objects.create(user=user, **user_profile)
        
        # hobby 등록
        user_profile.hobby.add(*get_hobbys)
        user_profile.save()
        
        return user
    
    def update(self, instance, validated_data):
        user_profile = validated_data.pop("userprofile")
        get_hobbys = user_profile.pop("get_hobbys", [])
        
        #instance에는 입력된 object가 담긴다.
        #회원 정보 수정 
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
                continue
            #setattr 은 instance.key = "value"와 똑같다 
            setattr(instance, key, value)
        instance.save()
        
        #프로필 수정
        user_profile_object = instance.userprofile
        for key, value in user_profile.items():
            setattr(user_profile_object, key, value) #instance.userprofile은 역참조
        user_profile_object.save()
        user_profile_object.hobby.set(get_hobbys)
        
        return instance
    
    class Meta:
        model = UserModel
        fields = ["username", "email", "fullname", "userprofile", "articles", "join_date", "password"]
        # 각 필드에 해당하는 다양한 옵션 지정
        extra_kwargs = {
            # write_only : 해당 필드를 쓰기 전용으로 만들어 준다.
            # 쓰기 전용으로 설정 된 필드는 직렬화 된 데이터에서 보여지지 않는다.
            'password': {'write_only': True}, # default : False
            #이메일
            'email': {
                # error_messages : 에러 메세지를 자유롭게 설정 할 수 있다.
                'error_messages': {
                    # required : 값이 입력되지 않았을 때 보여지는 메세지
                    'required': '이메일을 입력해주세요.',
                    # invalid : 값의 포맷이 맞지 않을 때 보여지는 메세지
                    'invalid': '알맞은 형식의 이메일을 입력해주세요.'
                    },
                    # required : validator에서 해당 값의 필요 여부를 판단한다.
                    'required': False # default : True
                    },
            #유저네임(아이디)
            'username': {
                'error_messages': {
                    'required': '아이디를 입력해주세요.',
                    # 'invalid': '아이디는 영문으로 입력해주세요.',
                },
                'required': True
            }, 
            #풀네임(이름)
            'fullname': {
                'error_messages': {
                    'required' : '이름을 입력해주세요.',
                },
                'required': True
            }
            }