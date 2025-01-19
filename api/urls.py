from django.urls import include, path
from api.views import UpdatePostStats

urlpatterns = [
    path("v1/", include(
        [
            path("post/", include(
                [
                    path("update_stat/<int:postId>", UpdatePostStats.as_view(), name="api.update_post_stat"),
                ]
            ))
        ]
    ))
]
