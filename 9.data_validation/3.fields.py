from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    username: str
    email: str
    is_active: bool = True  # simple default
    bio: str | None = None  # optional field
    tags: list[str] = Field(
        default_factory=list
    )  # mutable default (never use `= []` directly)


class SignupRequest(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    age: int = Field(ge=13, le=120, description="User age in years")
    email: EmailStr  # built-in email format validation
    password: str = Field(min_length=8)


# def number_append(num , val=[]):
#     val.append(num)
#     return val

# a = []
# number_append(5, a)
# num = number_append(3, a)
# print(a)

# b = []
# number_append(5, b)
# number_append(3, b)
# print(b)

# print(number_append(5))
# print(number_append(3))


x = 10

def test(a=x):
    print(a)

test()
x = 20
test()