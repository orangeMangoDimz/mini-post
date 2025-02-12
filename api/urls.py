from django.urls import include, path
from api.views import UpdatePostStats, SignIn

urlpatterns = [
    # TODO: fix redirect error when hit from insomnia
    path("users/", include(
        [
            path("v1/", include(
                [
                    path("login/", SignIn.as_view(), name="api.login"),
                ]
            ))
        ]
    )),
    path("post/", include(
        [
            path("v1/", include(
                [
                    path("update_stat/<int:postId>", UpdatePostStats.as_view(), name="api.update_post_stat"),
                ]
            ))
        ]
    ))
]
