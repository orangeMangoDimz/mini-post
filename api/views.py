from rest_framework.generics import UpdateAPIView
from rest_framework.views import Response, status
from posts.models import PostsStat
from .serializers import PostsStatsSerializers


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

class UpdatePostStats(UpdateAPIView, FormatResponse):
    serializer_class = PostsStatsSerializers

    def put(self, request, postId, *args, **kwargs):
        try:
            post = PostsStat.objects.get(pk=postId)
            serialize = self.serializer_class(post, data=request.data, partial=True)

            if serialize.is_valid():
                update_type = request.data.get("type")

                if update_type == "likes":
                    post.total_likes += 1
                    post.save()

                elif update_type == "commets":
                    post.total_comments += 1
                    post.save()

                serialize = self.serializer_class(post)
                response_data = serialize.data
                response_data["notification_message"] = f"{request.user.username} has liked your post"
                response_data["post_user_id"] = post.post.user.id

                return self.success_request("Success update data", response_data)
            return self.bad_request("Bad request", serialize.errors)

        except PostsStat.DoesNotExist:
            return self.not_found_request("Post not found")

        except Exception as e:
            print("erorr", e)
            return self.internal_server_error()
