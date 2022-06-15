#1 args, kwargs 를 사용한 예제
def average_score(a, b, *args, **kwargs):
    
    print(f"평균점수는 {(a+b+args[0]+kwargs['d'])/4} 점 입니다.")

    return

average_score(80, 94, 68, d=90)

def pizza_info(brand, *pizzas, **pizza_toppings):
    
    print(brand)
    for name in pizzas :
        print(name)
    for pizza, toppings in pizza_toppings.items():
        print(f"{pizza} 의 토핑은 {toppings} 입니다.")
    
    return

pizza_info("도미노", "페퍼로니", "하와이안", "치즈", 페퍼로니="페퍼로니", 하와이안="파인애플", 치즈="치즈")
#2 mutable , imutable 의 특성과 어떤 자료형이 어느것에 해당하는지 서술

# mutable : 한국어로 변할 수 있다. 즉 객체를 메모리의 주소로 생각을 하여 변수를 객체로 지정해서 변수에 추가하거나 했을때 같은 주소로 인식을 해서 객체도 같이 변한다. 종류 - List, Dict
# immutable : 불변 , 즉 객체를 지정하면 변하지 않는 것 종류 - int(숫자), str(문자), tuple, bool(참거짓), float(실수)

mutable = [1, 2, 3]
immutable = 4

int = immutable
list = mutable

int += 1
list.append(1)

print(mutable, immutable, int, list)


#3 DB field 에서 사용되는 Key 종류와 특징 서술

# Foreign Key : 외래키, 다른 테이블과 연결하는데 사용되는 키
# Unique Key : 중복값이 없는 키 , 하지만 여러개의 UK가 한테이블에 존재 할 수 있음.
# Primary Key : 마찬가지로 중복값이 없는 키, 하지만 한테이블에 단 1개의 PK가 존재함. 없거나, 2개이상 있을수 없다. 


#4 django 에서 queryset 과 object는 어떻게 다른지 서술

# queryset : 쿼리셋은 filter메소드로 QuerySet자료형을 가져오고 .values()를 해야 객체를 가져와서 값을 꺼낼 수 있다.쿼리셋은 DB에서 전달받은 객체들의 모음(list) . 쿼리셋은 값이 없어도, filter() 메소드로 QuerySet이라는 자료형형태로  QuerySet[]를 반환한다.
# object : 오브젝트는 get메소드로 객체를 가져와서 값을 꺼낼 수 있고, 오브젝트는 가져올 오브젝트가 없으면, get()메소드로 불러왔을때 불러오지 못한다. 그래서 try, except문으로 예외처리를 하게된다.

def queryset(request, id):
    genre = Genre.objects.filter(id=id).values()
    print(genre)
    # 쿼리셋 자료형으로 반환된것을.values() 로 딕셔너리 형태로 가져오게됨.
    return 

def object(request, id):
    
    try:
        genre = Genre.objects.get(id=id)
        print(genre)
    except Genre.DoesNotExist:
        
        return #장르가 없음
    return 