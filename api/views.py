from rest_framework.generics import UpdateAPIView
from rest_framework.views import Response, status, APIView
from rest_framework.permissions import AllowAny
from posts.models import PostsStat
from .serializers import PostsStatsSerializers
from likes.models import Likes
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from config.views import AppLogger
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from rest_framework.authtoken.models import Token

logger = AppLogger(__name__)

class FormatResponse:
    def success_request(self, message, data):
        return Response({
            "message": message,
            "data": data
        }, status=status.HTTP_200_OK)

    def bad_request(self, message, detail_error):
        return Response({
            "message": message,
            "detail": detail_error
        }, status=status.HTTP_400_BAD_REQUEST)

    def not_found_request(self, message):
        return Response({
            "message": message
        }, status=status.HTTP_404_NOT_FOUND)

    def internal_server_error(self):
        return Response({
            "message": "Internal server error"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SignIn(APIView, FormatResponse):
    permission_classes = [AllowAny]

    @method_decorator(ratelimit(key="ip", rate="5/5s", block=True))
    def post(self, request, format=None):
        data = request.data
        username = data.get("username", None)
        password = data.get("password", None)

        if username is None or password is None:
            return self.bad_request("Bad request", "Please provide both username and password")

        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                return self.bad_request("Bad request", "Invalid username or password!")

            token, _ = Token.objects.get_or_create(user=user)
            data = {
                "token": token.key,
                "user": {
                    "username": user.username,
                    "email": user.email,
                },
            }
            return self.success_request("Success login", data)

        except User.DoesNotExist:
            return self.not_found_request("Invalid username or password!")

class UpdatePostStats(UpdateAPIView, FormatResponse):
    # NOTE: Why do I need this serializer meanwhile I don't use the data in my Frontend?
    serializer_class = PostsStatsSerializers

    @method_decorator(ratelimit(key="user", rate="5/5s", block=True))
    def put(self, request, postId, *args, **kwargs):
        try:
            poststat = PostsStat.objects.get(pk=postId)
            serialize = self.serializer_class(poststat, data=request.data, partial=True)

            if serialize.is_valid():
                update_type = request.data.get("type")
                action = request.data.get("action")

                if update_type == "likes":
                    content_type = ContentType.objects.get_for_model(poststat.post)
                    if action == "like":
                        _, created =Likes.objects.get_or_create(
                            content_type=content_type,
                            object_id=poststat.post.id,
                            type="posts",
                            user=request.user
                        )
                        if created:
                            info_message = f"{request.user.username} #{request.user.id} has liked post #{poststat.post.id}"
                            logger.info(info_message)
                            poststat.total_likes += 1
                    elif action == "unlike":
                        deleted, _ = Likes.objects.get(
                            content_type=content_type,
                            object_id=poststat.post.id,
                            type="posts",
                            user=request.user
                        ).delete()
                        if deleted:
                            info_message = f"{request.user.username} has unliked post #{poststat.post.id}"
                            logger.info(info_message)
                            poststat.total_likes -= 1
                    else:
                        warning_message = f"Action {action} not found"
                        logger.info(warning_message)
                        return self.bad_request("Bad request", "Action not found")
                    poststat.save()

                # TODO: add comments logic
                elif update_type == "commets":
                    poststat.total_comments += 1
                    poststat.save()

                serialize = self.serializer_class(poststat)
                response_data = serialize.data
                response_data["notification_message"] = f"{request.user.username} has liked your post"
                response_data["post_user_id"] = poststat.post.user.id

                return self.success_request("Success update data", response_data)
            return self.bad_request("Bad request", serialize.errors)

        except PostsStat.DoesNotExist:
            return self.not_found_request("Post not found")

        except Likes.DoesNotExist:
            return self.not_found_request("Like not found")

        except Exception as e:
            error_message = f"Something is wroing with the server! {e}"
            logger.error(error_message)
            return self.internal_server_error()
