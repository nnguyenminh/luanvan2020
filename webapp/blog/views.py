import json

from bson import ObjectId, json_util
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from blog.models import Post
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed


# Create your views here.
@csrf_exempt
def add_post(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body)
        category = received_json_data['category']
        title = received_json_data["title"]
        content = received_json_data["content"]
        for section in content:
            section["section_content"] = section["section_content"].split("\n")
        comment = received_json_data["comment"]
        # tag = received_json_data["tag"].split(",")
        # date = received_json_data["date"]
        # author_details = {
        #     "first_name": received_json_data["author_details"]["first_name"],
        #     "last_name": received_json_data["author_details"]["last_name"]
        # }
        post = Post(category=category,
                    title=title,
                    content=content,
                    comment=comment)
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


def read_post_all(request, page=1):
    post = Post.objects.all().order_by('date')
    data = []
    for i in range(9):
        index = i + (page - 1) * 9
        data.append({
            "id": json.loads(json.dumps(post[index]._id, default=json_util.default))["$oid"],
            "category": post[index].category,
            "title": post[index].title,
            "content": post[index].content,
            "comment": post[index].comment,
            "date": post[index].date})
        print(json.dumps(post[index]._id, default=json_util.default))
    return JsonResponse(data, safe=False)


def get_recent_posts(page):
    post = Post.objects.all().order_by('date')
    length = len(post)
    print(length)
    data = []
    for i in range(9):
        index = i + (page - 1) * 9
        if index < length:
            data.append({"id": json.loads(json.dumps(post[index]._id, default=json_util.default))["$oid"],
                         "category": post[index].category,
                         "title": post[index].title,
                         "content": post[index].content,
                         "comment": post[index].comment,
                         "date": post[index].date})
        else:
            break
    return data


def get_post(id):
    post = Post.objects.get(_id=ObjectId(id))
    data = {
        "category": post.category,
        "title": post.title,
        "content": post.content,
        "comment": post.comment,
        "date": post.date,
    }
    return data


def home(request, page=1):
    data = get_recent_posts(page)
    context = {"data": data}
    return render(request, 'home.html', context)


def article(request):
    return render(request, 'article.html')


def blog(request):
    return render(request, 'blog.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def post(request, id):
    post_data = get_post(id)
    recent_posts_data = get_recent_posts(1)
    context = {'post': post_data,
               'recent': recent_posts_data}
    return render(request, 'post.html', context)
    pass
