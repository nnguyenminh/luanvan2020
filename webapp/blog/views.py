import json

from bson import ObjectId, json_util
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from blog.models import Post
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed

MAX_POST = 9
MAX_PAGE = 5


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
    for i in range(MAX_POST):
        index = i + (page - 1) * MAX_POST
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
    max_length = len(post)
    data = []
    for i in range(MAX_POST):
        index = i + (page - 1) * MAX_POST
        if index < max_length:
            data.append({
                "id": json.loads(json.dumps(post[index]._id, default=json_util.default))["$oid"],
                "category": post[index].category,
                "title": post[index].title,
                "content": post[index].content,
                "comment": post[index].comment,
                "date": post[index].date
            })
        else:
            break
    return data, max_length


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


def modify_bottom_nav_bar(max_length, page):
    div = int(max_length / MAX_POST) + 1
    mod = int(max_length % MAX_POST)
    page_nav = 0

    if mod == 0:
        div -= 1

    if page == 1:
        prev_nav = 1
        next_nav = page + 1
    elif page == max_length:
        prev_nav = page - 1
        next_nav = page
    else:
        prev_nav = page - 1
        next_nav = page + 1

    if page < MAX_PAGE:
        if div > MAX_PAGE:
            page_nav = range(1, MAX_PAGE + 1)
        else:
            page_nav = range(1, div + 1)
    if page >= MAX_PAGE:
        if page + 2 > div:
            page_nav = range(div - (MAX_PAGE - 1), div + 1)
        else:
            page_nav = range(page - int(MAX_PAGE / 2), page + int(MAX_PAGE / 2) + 1)

    nav_bar = [1, prev_nav, page_nav, next_nav, div]
    return nav_bar


def home(request, page=1):
    data, max_length = get_recent_posts(page)
    nav_bar = modify_bottom_nav_bar(max_length, page)
    context = {
        "data": data,
        "nav_bar": nav_bar,
        "page": page,
    }
    return render(request, 'home.html', context)


def technology(request):
    return render(request, 'technology.html')


def tutorial(request):
    return render(request, 'tutorial.html')


def blog(request):
    return render(request, 'blog.html')


def design(request):
    return render(request, 'design.html')


def contact(request):
    return render(request, 'contact.html')


def post(request, id):
    post_data = get_post(id)
    recent_posts_data = get_recent_posts(1)
    context = {'post': post_data,
               'recent': recent_posts_data}
    return render(request, 'post.html', context)
    pass


def category(request, cat):
    return render(request, f'{cat}.html')