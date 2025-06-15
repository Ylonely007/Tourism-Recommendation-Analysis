from app.models import TravelInfo
from app.utils.getHomeData import getNowTime
import json

def getTravelById(id):
    travel = TravelInfo.objects.get(id=id)
    travel.img_list = json.loads(travel.img_list)
    travel.comments = json.loads(travel.comments)

    return travel

def addComments(commentData):
    # 'author': author,
    # 'content': content,
    # 'date': date,
    # 'score': score
    # authorId
    year,month,day = getNowTime()
    travelInfo = commentData['travelInfo']
    travelInfo.comments.append({
        'author':commentData['userInfo'].username,
        'score':commentData['rate'],
        'content':commentData['content'],
        'date':str(year) + '-' + str(month) + '-' + str(day),
        'userId':commentData['userInfo'].id,
    })
    travelInfo.comments = json.dumps(travelInfo.comments)
    travelInfo.img_list = json.dumps(travelInfo.img_list)
    travelInfo.save()