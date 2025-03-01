from drf_spectacular.utils import OpenApiExample


class CreateUserExample():
    request = OpenApiExample('Request Example',
                             description='This api used to create user',
                             value={
                                 'username': 'Ali',
                                 'password': 'Ali@001',
                                 'email': 'ali@gmail.com',
                             }
                             )

    response = OpenApiExample('Response Example',
                              description='Response dont return password',
                              value={
                                  'username': 'Ali',
                                  'email': 'ali@gmail.com',
                              }
                              )


class UserPostListExample():
    response = OpenApiExample('Response Example',
                              description='Response dont return password',
                              value=[
                                    {
                                        "id": 23,
                                        "title": "Django rest framework",
                                        "date": "2024-11-05",
                                        "view_count": 1,
                                        "photo": "/Mdeia/Posts_Photo/Address/photo.jpg",
                                        "tags": [1,2,]
                                    },
                                    {
                                        "id": 42,
                                        "title": "Machine learning",
                                        "date": "2024-11-05",
                                        "view_count": 1,
                                        "photo": "/Mdeia/Posts_Photo/address/photo2.png",
                                        "tags": []
                                    }
                                ]
                              )


class AllUsersExample():
    response = OpenApiExample('Respose Example',
                              description='Thos API return all users information',
                              value=[
                                    {
                                        "username": "malmal",
                                        "age": 19,
                                        "email": "malmal@gmail.com",
                                        "number": 9171002000
                                    },
                                    {
                                        "username": "sara",
                                        "age": 40,
                                        "email": "sara@gmail.com",
                                        "number": 'null'
                                    }
                                ])


class UserInfoExample():
    response = OpenApiExample('Response Example',
                             description='This API return all posts of user',
                             value={
                                    "username": "erfan",
                                    "email": "erfan@gmail.com",
                                    "name": "erfan mor",
                                    "age": 19,
                                    "number": 9171002000,
                                    "address": "Shiraz",
                                    "photo": "/Mdeia/Profile/Address/profile.jpg",
                                    "date_joined": "2024-11-04",
                                    "SocialMedia": {
                                        "website": "website.com",
                                        "github": "erfanmor",
                                        "twitter": "",
                                        "instagram": "",
                                        "facebook": ""
                                    }
                                    })
           