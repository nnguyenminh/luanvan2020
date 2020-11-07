import json

from bson import ObjectId
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from blog.models import Post
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed


# Create your views here.
@csrf_exempt
def add_post(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body)
        post_title = received_json_data["title"]
        post_content = received_json_data["content"]
        comment = received_json_data["comment"]
        # tag = received_json_data["tag"].split(",")
        date = received_json_data["date"]
        # author_details = {
        #     "first_name": received_json_data["author_details"]["first_name"],
        #     "last_name": received_json_data["author_details"]["last_name"]
        # }
        post = Post(title=post_title,
                    content=post_content,
                    comment=comment,
                    date=date)
        post.save()
        return HttpResponse("Inserted")
    return HttpResponseNotAllowed


def update_post(request, id):
    pass


def delete_post(request, id):
    pass


def read_post(request, id):
    if request.method == 'GET':
        post = Post.objects.get(_id=ObjectId(id))
        data = {
            "title": post.title,
            "content": post.content,
            "comment": post.comment,
            "date": post.date,
        }
        return JsonResponse(data, safe=False)
    return HttpResponseNotAllowed


def read_post_all(request):
    pass
