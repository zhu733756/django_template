from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import TaskInfo, UserInfo, XinhuaWeb, VideoInfo
import json
from datetime import datetime, timedelta
import hashlib
from django_redis import get_redis_connection
from django.db.models import Q
from django.core.cache import cache
import random
from .lock import acquire_lock, release_lock, redis_db
from .tools import genernate_xml
# from django.db.models import Max
import base64
import logging
import requests

logger = logging.getLogger("filehandler")


# Create your views here.
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def postToCrawlFile(request):
    '''
    缓存txt，解析txt中的link，生成一个task
    '''
    identifier = acquire_lock("postToCrawl")
    if not identifier:
        return JsonResponse({
            'status': 0,
            'taskid': "",
            "message": "当前锁资源还未释放，请稍后重试！"
        })
    req = request.POST
    txtFile = request.FILES['file']
    if not txtFile:
        release_lock("postToCrawl", identifier)
        return JsonResponse({'status': 0, 'taskid': "", "message": "文件不存在！"})

    txtFileName = txtFile.name
    txtFileContent = txtFile.read().decode()
    if not txtFileContent.strip():
        e = "文件不存在link,添加时请用换行符分割！"
        logger.error(f"txtFile-name:{txtFileName},error:{e}")
        release_lock("postToCrawl", identifier)
        return JsonResponse({'status': 0, 'taskid': "", "message": e})

    links = [
        link.strip() for link in txtFileContent.split("\n") if link.strip()
    ]

    switch = int(req.get("switch", 0))
    crawled_links = []
    if switch:
        # 过滤links
        crawled_links = TaskInfo.objects.filter(url__in=links)
        if len(crawled_links) > 0:
            m = map(lambda task: task.url, crawled_links)
            links = list(set(links) - set(m))

    #log
    total = len(links)
    logger.info(
        f"txtFile-name:{txtFileName},total:{total},crawled:{len(crawled_links)}"
    )

    if total == 0:
        release_lock("postToCrawl", identifier)
        logger.error(f"txtFile-name:{txtFileName},error:任务创建失败,url全部重复")
        return JsonResponse({
            'status': 0,
            'taskid': "",
            "message": "任务创建失败,url全部重复！"
        })

    # task_id
    hash_name = hashlib.md5(txtFileName.encode()).hexdigest()[:8]
    taskId = hash_name + str(int(datetime.timestamp(datetime.now())))
    for link in links:
        redis_db.lpush("XinHuaNetCms",
                       json.dumps({
                           "taskId": taskId,
                           "link": link
                       }))
    else:
        UserInfo.objects.create(name=txtFileName, taskId=taskId, total=total)
        # [TaskInfo.objects.create(taskId=taskId,url=url) for url in links]

    logger.info(f"txtFile-name:{txtFileName}创建成功,taskId:{taskId}")
    release_lock("postToCrawl", identifier)
    return JsonResponse({
        'status': 1,
        'taskId': taskId,
        "total": total,
        "message": "ok"
    })


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def postToCrawlSingleLink(request):
    '''
    缓存txt，解析txt中的link，生成一个task
    '''
    req = json.loads(request.body)
    singleLink = req.get("singleLink", None)

    #sigle link
    if singleLink is None:
        logger.error(f"error:link不能为空")
        return JsonResponse({
            'status': 0,
            'taskid': "",
            "message": "没有找到link！"
        })
    links = [singleLink]

    timestamp = str(int(datetime.timestamp(datetime.now())))
    txtFileName = f"sl{timestamp}.txt"
    #log
    total = len(links)
    logger.info(f"txtFile-name:{txtFileName},total:{total}")

    if total == 0:
        logger.error(f"txtFile-name:{txtFileName},error:任务创建失败,url全部重复")
        return JsonResponse({
            'status': 0,
            'taskid': "",
            "message": "任务创建失败,url全部重复！"
        })

    # task_id
    hash_name = hashlib.md5(txtFileName.encode()).hexdigest()[:8]
    taskId = hash_name + timestamp
    for link in links:
        redis_db.lpush("XinHuaNetCms",
                       json.dumps({
                           "taskId": taskId,
                           "link": link
                       }))
    else:
        UserInfo.objects.create(name=txtFileName, taskId=taskId, total=total)
        # TaskInfo.objects.create(taskId=taskId,url=singleLink)
    logger.info(
        f"Single url:{singleLink}任务创建成功,txtFile-name:{txtFileName},taskId:{taskId}"
    )
    return JsonResponse({
        'status': 1,
        'taskId': taskId,
        "total": total,
        "message": "ok"
    })


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def delete_task(request):
    req = json.loads(request.body)
    taskId = req.get("taskId", None)
    if taskId is None:
        return JsonResponse({"status": 0, "message": "没有任务id"})
    tasks = TaskInfo.objects.filter(taskId=taskId)

    today = datetime.strptime(str(datetime.today().date()), "%Y-%m-%d")
    keyword = req.get("searchContent", None)
    startTime = req.get("startTime", str(today))
    endTime = req.get("endTime", str(today + timedelta(days=1)))
    pageNumber = int(req.get("pageNumber", 1))
    pageSize = int(req.get("pageSize", 10))

    def handle_time(date):
        return str(datetime.strptime(date, "%Y-%m-%d %H:%M:%S").date())

    #任务表
    TaskInfo.objects.filter(taskId=taskId).delete()
    #用户表
    UserInfo.objects.filter(taskId=taskId).delete()
    #清空缓存
    cache_key = f"History:{keyword}_{handle_time(startTime)}_{handle_time(endTime)}"
    if cache.has_key(cache_key):
        cache.expire(cache_key, 0)
    return JsonResponse({"status": 1, "message": "ok"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getTaskList(request):
    '''
    获取当前所有task完成进度的回调
    '''
    # request.method get
    today = datetime.strptime(str(datetime.today().date()), "%Y-%m-%d")

    keyword = request.GET.get("searchContent", None)
    startTime = request.GET.get("startTime", str(today))
    endTime = request.GET.get("endTime", str(today + timedelta(days=1)))
    pageNumber = int(request.GET.get("pageNumber", 1))
    pageSize = int(request.GET.get("pageSize", 10))
    order = bool(request.GET.get("order", "descending") == "descending")

    def handle_time(date):
        return str(datetime.strptime(date, "%Y-%m-%d %H:%M:%S").date())

    #建立缓存，保持10s左右
    cache_key = f"History:{keyword}_{handle_time(startTime)}_{handle_time(endTime)}"
    expire_time = 10 + random.random()
    if cache.has_key(cache_key):
        result = json.loads(cache.get(cache_key))
    else:
        result = []
        query = Q(created_at__gte=startTime) & Q(created_at__lte=endTime)
        if keyword:
            query = query & Q(name__contains=keyword) | Q(
                taskId__contains=keyword)
        user_info = UserInfo.objects.filter(query)

        if len(user_info):
            for t in user_info:
                taskId = t.taskId
                tasks = TaskInfo.objects.filter(taskId=taskId)
                success = len([task.status for task in tasks if task.status])
                total = t.total
                result.append({
                    "taskId": taskId,
                    "name": t.name,
                    "progress": int(success / total * 100),
                    "success": success,
                    "total": total,
                    "created_at": str(t.created_at).split(".")[0]
                })
            cache.set(cache_key, json.dumps(result), expire_time)

    result = sorted(result,
                    key=lambda x: datetime.strptime(x.get("created_at"),
                                                    "%Y-%m-%d %H:%M:%S"),
                    reverse=order) if order else result
    res = result[(pageNumber - 1) * pageSize:pageNumber * pageSize]
    return JsonResponse({
        'status': 1,
        'list': res,
        'total': len(result),
        "pageNumber": pageNumber,
        "pageSize": pageSize
    })


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def getXmlList(request):
    req = request.GET or request.POST
    taskId = req.get("taskId", None)
    if taskId is None:
        logger.error("Get xml list error: 没有任务id")
        return JsonResponse({"status": 0, "message": "没有任务id"})
    tasks = TaskInfo.objects.filter(taskId=taskId)
    if len(tasks) == 0:
        logger.error("Get xml list error: 部分url未被爬虫消费,请稍后访问")
        return JsonResponse({"status": 0, "message": "部分url未被爬虫消费,请稍后访问"})
    res = []
    for task in tasks:
        video_url = ""
        #无视频的情况
        video_status = -1
        video_infos = VideoInfo.objects.filter(article_url=task.url)
        if len(video_infos) > 0:
            video_info = video_infos.first()
            video_url = video_info.src_video_url
            video_status = video_info.status
        res.append({
            "url": str(task.url),
            "video_status": video_status,
            "video_url": video_url,
            "title": task.title,
        })
    logger.info(f"Get xml list ok, total:{len(res)}, sample:{res[0]}")
    return JsonResponse({"status": 1, "list": res})


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def showXmlDetails(request):
    req = request.GET
    url = req.get("url", None)
    if url is None:
        logger.error(f"GET xmlDetail error, url:{url}, msg:url不能为空")
        return JsonResponse({"status": 0, "message": "url不能为空"})
    url = base64.b64decode(url).decode()
    data = XinhuaWeb.objects.filter(url=url)
    if len(data) == 0:
        logger.info(f"GET xmlDetail error, url:{url}, msg:Xml暂时无法生成,请等待爬虫抓取")
        return HttpResponse(content="<p>Xml暂时无法生成,请等待爬虫抓取</p>")
    xml_content = data.first().xml_content
    if not xml_content:
        logger.info(f"GET xmlDetail error, url:{url}, msg:Xml暂时无法生成,请等待视频云处理!")
        return HttpResponse(content="<p>Xml暂时无法生成,请等待视频云处理!</p>")
    return HttpResponse(content=xml_content)


@api_view(["GET", "POST"])
def video_callback(request):
    body = request.GET or json.loads(request.body)
    logger.info(f"Video Callback:{str(body)}")
    return JsonResponse({"code": 1, "message": "成功", "data": {}})
