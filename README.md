# project_10 - Django (Pair Programming)

## 1. 목표

협업을 통한 데이터베이스 모델링 및 기능 구현



## 2.준비 사항

- Django 2.2.x

- Python 3.7.x 

- Github Flow



## 3. 프로젝트 설명

### 3.1. 데이터베이스 설계

- `db.sqlite3`은 다음과 같이 설계되었습니다.
- ERD

![image](https://user-images.githubusercontent.com/52685373/69303483-88d0cb00-0c60-11ea-82fc-e89225500d5b.png)

### 3.2 seeddata 구성

```bash
$python manage.py dumpdata --indent 2 > movies movies.json
$python manage.py dumpdata --indent 2 > accounts accounts.json
```

각각의 fixures /app_name 의 폴더안에 덤프데이터를 구성해두었습니다. 



### 3.3 accounts App

#### 3.3.1 로그인, 로그아웃, 회원가입

유저 회원가입과 로그인, 로그아웃을 구성하였습니다.

![image](https://user-images.githubusercontent.com/52685373/69305122-3a262f80-0c66-11ea-9445-b4d30dd56ee3.png)

> 로그인

![image](https://user-images.githubusercontent.com/52685373/69305256-9ab56c80-0c66-11ea-9849-bb0db01b7fa9.png)

> 회원 가입





#### 3.3.1 유저목록

![image](https://user-images.githubusercontent.com/52685373/69305093-2975b980-0c66-11ea-8684-2db050066f59.png)

- 사용자의 목록이 나타나며, 사용자의 username 을 클릭하면 유저 상세보기 페이지로 넘어 갑니다.



#### 3.3.2 유저 상세 정보

![image](https://user-images.githubusercontent.com/52685373/69306023-8a52c100-0c69-11ea-8fbb-4a3f692747b6.png)

1. 해당 유저가 작성한 평점 정보가 모두 출력됩니다.
2. 해당 유저가 좋아하는 영화 정보가 모두 출력됩니다.
3. 해당 유저를 팔로우한 사람의수, 팔로잉한 사람의 수가 출력됩니다.



### 3.4 movies App

#### 3.4.1 영화목록

- 영화의 이미지를 클릭하면 영화 상세보기 페이지로 넘어갑니다.
  - 좋아요 기능 구현
  -  좋아하는 영화를 담아 놓을 수 있도록 구현합니다.
  - 하트를 누르는것으로 동작합니다.
  - 로그인한 유저만 해당기능을 사용할 수 있습니다.

![image](https://user-images.githubusercontent.com/52685373/69305418-39da6400-0c67-11ea-92cc-ffc21d300f0a.png)



#### 3.4.2 상세 영화 정보

![image](https://user-images.githubusercontent.com/52685373/69305518-a2c1dc00-0c67-11ea-99dc-4ece79cbe0d0.png)

- 영화 관련 정보가 모두 나열됩니다.
- 로그인한 사람만 영화 평점을 남길 수 있습니다.
- 모든 사람은 평점목록을 볼 수 있습니다.
- 영화 평점은 로그인 한 사람만 남길 수 있습니다.
- URL은 ` /movies/1/reviews/new/` 등으로 동적으로 할당하는 부분이 존재합니다.
- 동적으로 할당되는부분에는 데이터베이스에 저장된 영화 정보의 Primary Key가 들어갑니다.

![image](https://user-images.githubusercontent.com/52685373/69305767-76f32600-0c68-11ea-81b6-97adba692cfc.png)

> 팔로우 역시 이곳에서 가능합니다.



## 4. 에러 사항

```python
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followings')
#models.py
```

```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields
        
# form.py
```

```python
AUTH_USER_MODEL = 'accounts.User'

# settings.py
```

followers를 사용하기위해 유저를 변경하여 이를 셋팅즈랑 연결했을때 장고에서 제공하는 Form과 달라 고생을 했습니다. 이는 커스텀 유저모델을 작성하며 해결이 가능하였습니다.



```python
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    reviews = movie.review_set.all()
    person = get_object_or_404(get_user_model(), pk=request.user.id)
    genres = movie.genres.all()
    review_form = ReviewForm()
    context = {'movie': movie, 'reviews':reviews, 'review_form':review_form, 'person': person, 'genres': genres,}
    return render(request, 'movies/detail.html', context)
```

 detail.html 에서 사용하지 않는 person을 변수로 지정해서 로그인 하지 않았을 때 request에서 user가 넘어오지 않아 오류가 발생하는것을 확인하였습니다.  이는 person변수를 삭제함으로써 해결했습니다.



## 5. 협업 과정

조규홍 - movies

김준호 - accounts



조규홍 - 내가 모르는 것을 팀원에게 물어보고 같이 찾아봄으로써 프로젝트를 혼자 하는것보다 더 수월하게 진행할 수 있엇습니다.

김준호 - 처음 깃으로 협업을 진행하면서 오류가 많이 발생하였는대 이를 팀원과 같이 해결함으로써 당황하지않을수 있엇습니다.





