#render函数用于将数据渲染到指定的模板中，并返回生成的HTML内容
#redirect允许你将用户从一个URL重定向到另一个URL，通常用于处理单表提交、用户登录、注册等操作后的页面跳转

from django.shortcuts import render,redirect
from app.models import User,TravelInfo
from django.http import HttpResponse
from app.recommdation import getUser_ratings,user_bases_collaborative_filtering
from app.utils import errorResponse,getHomeData,getPublicData,getChangeSelfInfoData,getAddCommentsData,getEchartsData,getRecommendationData

def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            User.objects.get(username=username, password=password)
            request.session['username'] = username
            return redirect('/app/home')

        except:
            return errorResponse.errorResponse(request,'账号或密码错误')


def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
        try:
            User.objects.get(username=username)
        except:
            if not username or not password or not confirmPassword:return errorResponse.errorResponse(request,'不允许为空值')
            if  password != confirmPassword:return errorResponse.errorResponse(request,'两次密码不一致')
            User.objects.create(username=username,password=password)
            return redirect('/app/login')

        return errorResponse.errorResponse(request,'该账号已存在')

def logOut(request):
    request.session.clear() #退出登录时，清除request.session
    return redirect('/app/login') #退出登录 转到登陆页面

def home(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    a5Len,commentsLenTitle,provienceDicSort = getHomeData.getHomeTagData()
    scoreTop10Data,saleCountTop10 = getHomeData.getAnthorData()
    year,mon,day = getHomeData.getNowTime()
    geoData = getHomeData.getGeoData()
    userBarCharData = getHomeData.getUserCreateTimeData()
    #字典
    return render(request,'home.html',{
        'userInfo':userInfo,
        'a5Len':a5Len,
        'commentsLenTitle':commentsLenTitle,
        'provienceDicSort':provienceDicSort,
        'scoreTop10Data':scoreTop10Data,
        'nowTime':{
            'year':year,
            'mon':getPublicData.monthList[mon - 1],
            'day':day
        },
        'geoData':geoData,
        'userBarCharData':userBarCharData,
        'saleCountTop10':saleCountTop10
    })

def changeSelfInfo(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year,mon,day = getHomeData.getNowTime()
    if request.method == 'POST':
        getChangeSelfInfoData.changeSelfInfo(username,request.POST,request.FILES)
        userInfo = User.objects.get(username=username)

    return render(request,'changeSelfInfo.html',{
        'userInfo':userInfo,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        },
    })

def changePassword(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()
    if request.method == 'POST':
        res = getChangeSelfInfoData.getChangePassword(userInfo,request.POST)
        if res != None:
            return errorResponse.errorResponse(request,res)

    return render(request, 'changePassword.html', {
        'userInfo': userInfo,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        },
    })

def tableData(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()
    talbeData = getPublicData.getAllTravelInfoMapData()
    return render(request, 'tableData.html', {
        'userInfo': userInfo,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        },
        'talbeData':talbeData
    })

def addComments(request,id):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()
    travelInfo = getAddCommentsData.getTravelById(id)
    if request.method == 'POST':
        getAddCommentsData.addComments({
            'id':id,
            'rate':int(request.POST.get('rate')),
            'content':request.POST.get('content'),
            'userInfo':userInfo,
            'travelInfo':travelInfo
        })
        return redirect('/app/tableData')
    return render(request, 'addComments.html', {
        'userInfo': userInfo,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        },
        'travelInfo':travelInfo,
        'id':id
    })

def cityChar(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()
    Xdata,Ydata = getEchartsData.cityCharDataOne()
    resultData = getEchartsData.cityCharDataTwo()
    return render(request, 'cityChar.html', {
        'userInfo': userInfo,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        },
        'cityCharOneData':{
            'Xdata':Xdata,
            'Ydata':Ydata
        },
        'cityCharTwoData':resultData
    })

def rateChar(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()
    cityList = getPublicData.getCityList()
    travelList = getPublicData.getAllTravelInfoMapData(cityList[0])
    charOneData = getEchartsData.getRateCharDataOne(travelList)
    charTwoData = getEchartsData.getRateCharDataTwo(travelList)
    if request.method == 'POST':
        travelList = getPublicData.getAllTravelInfoMapData(request.POST.get('province'))
        charOneData = getEchartsData.getRateCharDataOne(travelList)
        charTwoData = getEchartsData.getRateCharDataTwo(travelList)


    return render(request, 'rateChar.html', {
        'userInfo': userInfo,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        },
        'cityList':cityList,
        'charOneData':charOneData,
        'charTwoData':charTwoData
    })

def priceChar(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()
    cityList = getPublicData.getCityList()
    travelList = getPublicData.getAllTravelInfoMapData()
    xData,yData = getEchartsData.getPriceCharDataOne(travelList)
    x1Data,y1Data = getEchartsData.getPriceCharDataTwo(travelList)
    disCountPieData = getEchartsData.getPriceCharDataThree(travelList)
    return render(request, 'priceChar.html', {
        'userInfo': userInfo,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        },
        'cityList': cityList,
        'echartsData':{
            'xData':xData,
            'yData':yData,
            'x1Data':x1Data,
            'y1Data':y1Data,
            'disCountPieData':disCountPieData
        }
    })

def commentsChar(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()
    xData,yData = getEchartsData.getCommentsCharDataOne()
    commentsScorePieData = getEchartsData.getCommentsCharDataTwo()
    x1Data,y1Data = getEchartsData.getCommentsCharDataThree()
    return render(request, 'commentsChar.html', {
        'userInfo': userInfo,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        },
        'echartsData':{
            'xData':xData,
            'yData':yData,
            'commentsScorePieData':commentsScorePieData,
            'x1Data':x1Data,
            'y1Data':y1Data
        }
    })

def recommendation(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()
    try:
        user_ratings = getUser_ratings()
        recommended_items = user_bases_collaborative_filtering(userInfo.id, user_ratings)
        resultDataList = getRecommendationData.getAllTravelByTitle(recommended_items)
    except:
        resultDataList = getRecommendationData.getRandomTravel()

    return render(request, 'recommendation.html', {
        'userInfo': userInfo,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        },
        'resultDataList':resultDataList
    })

def detailIntroCloud(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()
    return render(request, 'detailIntroCloud.html', {
        'userInfo': userInfo,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        }
    })

def commentContentCloud(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()
    return render(request, 'commentContentCloud.html', {
        'userInfo': userInfo,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        }
    })