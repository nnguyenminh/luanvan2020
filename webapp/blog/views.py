import json
from urllib.parse import unquote
from random import randrange
import pymongo
from bson import ObjectId, json_util
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from blog.models import Post
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed

MAX_POST = 4
MAX_PAGE = 3
MAX_SEARCH_RESULT = 10


# Create your views here.

def post_comment(request):
    print(request.body)
    return render(request, 'blog.html')


def add_post(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body)
        # category = received_json_data['category']
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
            # "category": post[index].category,
            "title": post[index].title,
            "content": post[index].content,
            "comment": post[index].comment,
            "date": post[index].date})
        print(json.dumps(post[index]._id, default=json_util.default))
    return JsonResponse(data, safe=False)


def get_recent_posts(page):
    post = Post.objects.all().order_by('created_at')
    max_length = len(post)
    data = []
    for i in range(MAX_POST):
        index = i + (page - 1) * MAX_POST
        if index < max_length:
            if len(post[index].title) > 40:
                post[index].title = post[index].title[:27] + '...'
            data.append({
                # "id": json.loads(json.dumps(post[index]._id, default=json_util.default))["$oid"],
                "id": post[index].id,
                "category": post[index].category,
                "title": post[index].title,
                "content": post[index].content,
                "date": post[index].created_at
            })
        else:
            break
    return data, max_length


def get_post(id):
    # post = Post.objects.get(_id=ObjectId(id))
    post = get_object_or_404(Post, id=int(id))
    parents = []
    children = {}
    comments = post.comments.all().order_by('created_at').values()
    comments_count = len(comments)
    for comment in comments:
        if comment["group"] == "0":
            parents.append(comment)
        else:
            if comment["group"] in children.keys():
                children[comment["group"]].append(comment)
            else:
                children[comment["group"]] = [comment]

    for parent in parents:
        group = str(parent['id'])
        if group in children.keys():
            parent["children"] = children[group]

    data = {
        "id": post.id,
        "category": post.category,
        "title": post.title,
        "content": post.content,
        "comments": parents,
        "comments_count": comments_count,
        "date": post.created_at,
    }
    return data


def modify_bottom_nav_bar(max_length, page, MAX):
    div = int(max_length / MAX) + 1
    mod = int(max_length % MAX)
    page_nav = 0

    if mod == 0:
        div -= 1

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

    if page == 1:
        first = 0
    else:
        first = 1

    if page == div:
        last = 0
    else:
        last = div

    nav_bar = [first, page_nav, last]
    return nav_bar


def home(request, page=1):
    data, max_length = get_recent_posts(page)
    nav_bar = modify_bottom_nav_bar(max_length, page, MAX_POST)
    context = {
        "data": data,
        "nav_bar": nav_bar,
        "page": page,
    }
    return render(request, 'home.html', context)


def contact(request):
    return render(request, 'contact.html')


def random_int(num, fr, to):
    result = []
    while True:
        x = randrange(int(fr), int(to))
        if x not in result:
            result.append(x)
        if len(result) == num:
            break

    return result


def post(request, id):
    post_data = get_post(id)
    # recent_posts_data = get_recent_posts(1)
    # indexes = random_int(2, 0, MAX_POST-1)
    # recent_posts = []
    # for i in indexes:
    #     recent_posts.append(recent_posts_data[i])
    context = {'post': post_data}
    return render(request, 'post.html', context)


def category(request, cat):
    context = {
        "nav_tab": cat
    }
    return render(request, f'{cat}.html', context)


def search_in_mongo(list_keywords):
    client = pymongo.MongoClient()
    db = client['blog_data']
    collection = db["blog_post"]
    collection.create_index([('title', 'text'), ('content', 'text')])
    keywords = []
    result_id = []
    result = []

    for raw_keyword in list_keywords:
        # x = collection.find({"$text": {"$search": f'"{keyword}"'}})
        search_result = collection.find({"$text": {"$search": raw_keyword}})
        keyword = collection.find({"$text": {"$search": raw_keyword}}).explain()["queryPlanner"]["winningPlan"][
            "parsedTextQuery"]["terms"]
        if keyword:
            keywords.append(keyword[0])
        print(keywords)
        for item in search_result:
            if item not in result_id:
                result_id.append(item['id'])
                result.append(get_post(item['id']))

    return keywords, result


def load_dictionary():
    f = open("blog\\static\\dictionary.txt", "r")
    temp = f.read()
    temp = temp.replace("'", '"')
    temp = temp[temp.find("{"):-1]
    dictionary = json.loads(temp)
    f.close()
    return dictionary


def add_css_highlight_background(word):
    return fr'<span style=color:red;font-weight:500;background-color:yellow>{word}</span>'


def search(request, page=1):
    raw_request = str(request)
    raw_keywords = raw_request[raw_request.find("keyword") + 8:-2]
    list_raw_keywords = raw_keywords.split(" ")
    keywords, search_result = search_in_mongo(list_raw_keywords)

    dictionary = load_dictionary()
    new_font = add_css_highlight_background
    data = []

    for item in search_result:
        for keyword in keywords:
            if keyword in dictionary:
                for value in dictionary[keyword]:
                    item['title'] = item['title'].replace(value, new_font(value))
                    item['content'] = item['content'].replace(value, new_font(value))
            else:
                item['title'] = item['title'].replace(keyword, new_font(keyword))
                item['content'] = item['content'].replace(keyword, new_font(keyword))
    max_length = len(search_result)

    nav_bar = modify_bottom_nav_bar(max_length, page, MAX_SEARCH_RESULT)

    for i in range(MAX_SEARCH_RESULT):
        index = i + (page - 1) * MAX_POST
        if index < max_length:
            data.append({
                "id": search_result[index]["id"],
                "category": search_result[index]["category"],
                "title": search_result[index]["title"],
                "content": search_result[index]["content"],
                "date": search_result[index]["date"]
            })
        else:
            break

    if not search_result:
        context = {
            "not_found": True,
            "keyword": raw_keywords
        }
    else:
        context = {
            "data": data,
            "nav_bar": nav_bar,
            "page": page,
            "keyword": raw_keywords
        }

    return render(request, 'search.html', context)
