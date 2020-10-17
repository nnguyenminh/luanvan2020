# from pymongo import MongoClient
#
# client = MongoClient('192.168.1.10', port=27017)
# db = client.blog_data
# data = [{
#     'title': 'how to hack wifi',
#     'description': 'co cl ay',
#     'date': '17/10/2020',
# }, {
#     'title': 'how to hack wifi - cach 2',
#     'description': 'co cl ay luon',
#     'date': 'nam sau co'
# }]
#
# newvalues = {"$set":
#     {'author':
#         {
#             'name': 'XXX',
#             'age': 21
#         }
#     }
# }
# # col = db.bai_viet
# # col.insert_many(data)
#
# # cursor = col.find()
# # for each in cursor:
# #     print(each)
#
# # x = col.update_many({}, newvalues)
# # print(x.modified_count, "documents updated.")
