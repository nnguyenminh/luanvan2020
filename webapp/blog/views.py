import json
from urllib.parse import unquote
from random import randrange
import pymongo
from bson import ObjectId, json_util
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import re
from blog.models import Post, Comment, Category
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest

MAX_POST = 4
MAX_PAGE = 3
MAX_SEARCH_RESULT = 10


# Create your views here.

def format_datetime(datetime):
    return datetime.strftime("%m/%d/%Y, %H:%M:%S")

def load_comments(request,id):
    post = get_object_or_404(Post, id=int(id))
    parents = []
    children = {}
    comments = []
    query_comments = post.comments.all().order_by('created_at').values()

    for comment in query_comments:
        if comment["hidden"]:
            continue
        comment["created_at"] = format_datetime(comment["created_at"])
        comments.append(comment)



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
    return HttpResponse(json.dumps(parents), content_type='application/json')

@csrf_exempt
def post_comment(request):
    try:
        if request.method == 'POST':
            print(request.body)
            received_json_data = json.loads(request.body)
            # category = received_json_data['category']
            author = received_json_data["author"]
            content = received_json_data["content"]
            post_id = received_json_data["post_id"]
            comment = Comment(post_id=post_id,
                        author=author,
                        content=content)
            comment.save()

            post = get_object_or_404(Post, id=int(post_id))
            latest_comment = post.comments.all().order_by('created_at').values().last()
            latest_comment["created_at"] = format_datetime(latest_comment["created_at"])

            return HttpResponse(json.dumps(latest_comment), content_type='application/json')
        return HttpResponseBadRequest("Bad Request", content_type='application/json')
    except TypeError:
        return HttpResponseBadRequest("Bad Request", content_type='application/json')
    except json.decoder.JSONDecodeError:
        return HttpResponseBadRequest("Bad Request", content_type='application/json')

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
    return HttpResponseBadRequest("Bad Request", content_type='application/json')


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
    return HttpResponseBadRequest("Bad Request", content_type='application/json')


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
    post = Post.objects.all().order_by('created_at').reverse()
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


def find_category(regex):
    categories = ["Technology", "Tutorials", "Design"]
    for category in categories:
        if re.search(regex, category, re.IGNORECASE):
            return category

def category(request, cat):
    
    post = Category.objects.get(name=find_category(cat)).posts.all()
    print(post)
    return render(request, f'{cat}.html')


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
            keywords = keyword.copy()
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

def find_keyword_pos(regex, item):
    matches = re.finditer(regex, item, re.MULTILINE | re.IGNORECASE)
    result = []
    for matchNum, match in enumerate(matches, start=1):
        result.append(item[match.start():match.end()])
    
    return result

def search(request, page=1):
    raw_request = unquote(str(request))
    raw_keywords = raw_request[raw_request.find("keyword") + 8:-2]
    list_raw_keywords = raw_keywords.split(" ")
    keywords, search_result = search_in_mongo(list_raw_keywords)
    dictionary = load_dictionary()
    new_format = add_css_highlight_background
    data = []

    for item in search_result:
        for keyword in keywords:
            if keyword in dictionary:
                for value in dictionary[keyword]:
                    for word in find_keyword_pos(value, item['title']):
                        item['title'] = item['title'].replace(word, new_format(word))
                    for word in find_keyword_pos(value, item['content']):
                        item['content'] = item['content'].replace(word, new_format(word))
            else:
                for word in find_keyword_pos(keyword, item['title']):
                    item['title'] = item['title'].replace(word, new_format(word))
                for word in find_keyword_pos(keyword, item['content']):
                    item['content'] = item['content'].replace(word, new_format(word))
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
