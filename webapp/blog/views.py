import json

from bson import ObjectId
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from blog.models import Posts
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed


# Create your views here.
@csrf_exempt
def add_post(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body)
        post_title = received_json_data["post_title"]
        post_description = received_json_data["post_description"]
        comment = received_json_data["comment"]
        tag = received_json_data["tag"].split(",")
        date = received_json_data["date"]
        author_details = {
            "first_name": received_json_data["author_details"]["first_name"],
            "last_name": received_json_data["author_details"]["last_name"]
        }
        post = Posts(post_title=post_title,
                     post_description=post_description,
                     comment=comment,
                     tag=tag,
                     date=date,
                     author_details=author_details)
        post.save()
        return HttpResponse("Inserted")
    return HttpResponseNotAllowed


def update_post(request, id):
    pass


def delete_post(request, id):
    pass


def read_post(request, id):
    if request.method == 'GET':
        post = Posts.objects.get(_id=ObjectId(id))
        data = {
            "post_title": post.post_title,
            "post_description": post.post_description,
            "comment": post.comment,
            "date": post.date,
            "tag": post.tag,
            "author_details": {
                "first_name": post.author_details["first_name"],
                "last_name": post.author_details["last_name"]
            }
        }
        return JsonResponse(data, safe=False)
    return HttpResponseNotAllowed


def read_post_all(request):
    pass
