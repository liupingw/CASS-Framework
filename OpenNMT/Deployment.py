import datetime
import random
import re
import time
import urllib
import chardet
import ssl
import signal


from pandas.io.json import json

from Classifer.predict import CnnModel
from OpenNMT.translate import interface

ssl._create_default_https_context = ssl._create_unverified_context







class InputTimeoutError(Exception):
    pass

def interrupted(signum, frame):
    raise InputTimeoutError

signal.signal(signal.SIGALRM, interrupted)

signal.alarm(10)#


#################################################################################################
##############You should fill in your community API and simulative user information##############
#########################and modify time parameter if you want###################################

THRESHOLD = 10  # the threshold for deciding whether the chatbot needs to respond to the overlooked post or not 回帖阈值
STUDY_TIME = 60 * 24 * 7  # the whole deployment period 整个实验周期
OBSERVE_INTERVAL = 9  # the interval time between getting latest posts 每隔一段时间去刷新一下有没有新帖子
COMMENT_INTERVAL = 2  # the interval time detecting if observed posts have been replied 每隔一段时间去检查这些已经被观察的帖子有没有被回复


Community_getLatestPost_Url = ""
Community_toComment_Url = ""
Community_getPostDetail_Url = ""


AI_auth_list = [["username1", "<authorization1>"],
                ["username2", "<authorization2>"],
                ["username3", "<authorization3>"]]
# e.g.
# username = "saltone"
# authorization = "XDS 7.fIC1Fkcg6-Qa6--o9qUP-FyrhLkyLLZOMN6r7Jxxx"

#################################################################################################
##############You should fill in your community API and simulative user information##############
#########################and modify time parameter if you want###################################


user_agent_list = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
]


def get_html_content(original_url):
    ua = random.choice(user_agent_list)
    headers = {'User-Agent': ua}
    request = urllib.request.Request(url=original_url, headers=headers)
    response = urllib.request.urlopen(request, timeout=1000).read()
    #  print("response",response)
    code_info = chardet.detect(response)
    code = code_info['encoding']
    # print("codecodecodeXXXXXXXXXX",code)
    if code == 'utf-8' or code == 'utf-8':
        data = response
    elif code == 'gbk' or code == 'GBK':
        data = response.decode('gbk', 'ignore').encode('utf-8')
    elif code == 'gb2312' or code == 'GB2312':
        data = response.decode('gb2312', 'ignore').encode('utf-8')
    else:
        data = response
    return data


def getLatestNoLast(forum_id):
    original_url = Community_getLatestPost_Url+'&forum_id=' + str(
        forum_id) + '&order=publish_date_desc&size=20'

    data = get_html_content(original_url).decode("utf-8")
    Json = json.loads(data)

    # print("Json", Json)

    data = Json.get("data")
    topics = data.get("topics")

    return topics


def getLatest(forum_id, lastPost):
    original_url = Community_getLatestPost_Url+'&forum_id=' + str(
        forum_id) + '&order=publish_date_desc&size=20&last=' + str(lastPost)

    data = get_html_content(original_url).decode("utf-8")
    Json = json.loads(data)

    # print("Json", Json)

    data = Json.get("data")
    topics = data.get("topics")

    return topics


def GetComment(content):
    # for LSTM
    q = re.findall(r'.{1}', content)
    cut_q = ""
    for word in q:
        cut_q += word + " "

    str = interface(cut_q).replace(" ", "")
    return str





def toComment(topic_id, content, ua, authorization):
    comment = GetComment(content)


    print("content:" + content)
    print("comment:" + comment)

    try:
        comment = input("Do you agree to Comment? Input nothing to confirm or input an appropriate sentence:")
    except InputTimeoutError:
        print('\n Agree to comment')

    print("chatbot will comment on this sentence:"+comment)
    signal.alarm(0)  




    url = Community_toComment_Url
    postdata = {"content": comment, "referenced_id": -1,
                "diff_data": 1,
                "is_watermark": True,
                "topic_id": topic_id}

    para = json.dumps(postdata)

    req = urllib.request.Request(url, para.encode(encoding='UTF8'))
    req.add_header("User-Agent", ua)
    req.add_header("Authorization", authorization)
    req.add_header("Content-Type", "application/json;charset=UTF-8")
    data = urllib.request.urlopen(req).read().decode("utf-8")

    print(data)

    return comment


def save():
    return


def tid_maker():
    return '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now()) + ''.join(
        [str(random.randint(1, 10)) for i in range(5)])





def getPostDetailNoLast(topicId, order_by):
    original_url = Community_getPostDetail_Url + '&topic_id=' + str(
        topicId)
    # print("getPostDetail:"+original_url)
    data = get_html_content(original_url).decode("utf-8")
    Json = json.loads(data)
    data = Json.get("data")
    topic = data.get("topic")
    reviews = data.get("reviews")

    return topic, reviews




cnn_model = CnnModel()



def main():

    nowTime = datetime.datetime.now()


    currentObeserveTime = OBSERVE_INTERVAL + 1  # 

    forumList = [15, 32, 33, 70, 47]
    lastobservedTime15 = nowTime
    lastobservedTime32 = nowTime
    lastobservedTime33 = nowTime
    lastobservedTime70 = nowTime
    lastobservedTime47 = nowTime

    study_startTime = nowTime


    filename = tid_maker()
    isComm = True  #

    obeserveList = []

    time.sleep(1)

    count = 0

    with open('../study/reply/' + filename + "_5" + '.txt', 'w') as f_reply:
        with open('../study/noreply/' + filename + "_5" + '.txt', 'w') as f_noreply:
            with open('../study/hasOthers/' + filename + "_5" + '.txt', 'w') as f_hasOthers:
                while True:

                    ua = random.choice(user_agent_list)
                    ran = random.choice(AI_auth_list)
                    AIName = ran[0]
                    authorization = ran[1]
                    # print(AIName +" "+ authorization+" "+ua)

                    if int((datetime.datetime.now() - study_startTime).seconds / 60) > STUDY_TIME:
                        print("Deployment End ")
                        print(int((datetime.datetime.now() - study_startTime).seconds / 60))
                        for postId in obeserveList:
                            print(postId)
                        break

                    try:

                        if currentObeserveTime > OBSERVE_INTERVAL:
                            print("Time to get latest post")

                            # refresh new posts 刷一遍新出的帖子
                            for forumId in forumList:
                                print("forumId:", forumId)

                                if forumId == 15:
                                    lastobservedTime = lastobservedTime15
                                elif forumId == 32:
                                    lastobservedTime = lastobservedTime32
                                elif forumId == 33:
                                    lastobservedTime = lastobservedTime33
                                elif forumId == 70:
                                    lastobservedTime = lastobservedTime70
                                elif forumId == 47:
                                    lastobservedTime = lastobservedTime47

                                nowobservedTime = datetime.datetime.now()
                                NewestObservedTime = nowobservedTime
                                lastPostId = ""

                                while nowobservedTime > lastobservedTime:
                                    # get new posts 
                                    if lastPostId == "":
                                        topics = getLatestNoLast(forumId)
                                    else:
                                        topics = getLatest(forumId, lastPostId)
                                    for post in topics:

                                        # filter old posts 
                                        published_date = post.get("published_date")

                                        nowobservedTime = datetime.datetime.strptime(published_date,
                                                                                       '%Y-%m-%d %H:%M:%S')
                                        if nowobservedTime < lastobservedTime:
                                            print("has observed!")

                                            break

                                        postId = post.get("id")
                                        lastPostId = postId

                                        # detect if anyone else has replied to this post 看看有没有人回复,有则写入hasOthers
                                        total_review = post.get("total_review")

                                        if total_review == 0:
                                            print("none-replied post")

                                            # 进入观察队列
                                            obeserveList.append(postId)

                                        else:
                                            print("others has replied")

                                            # 已经有人回复了
                                            user_id = post.get("user_id")
                                            title = post.get("title")
                                            forum_id = post.get("forum_id")
                                            f_hasOthers.write(
                                                str(postId) + "\t" + str(forum_id) + "\t" + title.strip().replace("\n",
                                                                                                                  "").replace(
                                                    "\r",
                                                    "") + "\t" + str(user_id) + "\t" + str(
                                                    total_review) + "\t" + published_date + "\n")

                                    if nowobservedTime < lastobservedTime:
                                        break
                                if forumId == 15:
                                    lastobservedTime15 = NewestObservedTime
                                elif forumId == 32:
                                    lastobservedTime32 = NewestObservedTime
                                elif forumId == 33:
                                    lastobservedTime33 = NewestObservedTime
                                elif forumId == 70:
                                    lastobservedTime70 = NewestObservedTime
                                elif forumId == 47:
                                    lastobservedTime47 = NewestObservedTime

                        if currentObeserveTime >= COMMENT_INTERVAL:
                            print("time to check observed posts")

                            print("current observed posts：")
                            # 检查观察队列是否要超过THRESHOLD的
                            for postId in obeserveList[0:]:
                                print(postId)

                                try:
                                    topic, reviewers = getPostDetailNoLast(postId, "reviewed_date")
                                except Exception as e:
                                    print(e)
                                    print(" There is an exception when getting post detail,so remove this post in observed posts list")
                                    obeserveList.remove(postId)
                                    print("remove ", postId)
                                    continue

                                time.sleep(2)
                                total_floor = topic.get("total_floor")
                                published_date = topic.get("published_date")
                                user_id = topic.get("user_id")
                                title = topic.get("title")
                                if title is None:
                                    title = "No Title"
                                forum_id = topic.get("forum_id")
                                total_review = topic.get("total_review")
                                content = topic.get("content")
                                user_name = topic.get("publisher").get("screen_name")
                                if total_floor > 0:
                                    print("others has replied")
                                    f_hasOthers.write(
                                        str(postId) + "\t" + str(forum_id) + "\t" + title.strip().replace("\n",
                                                                                                          "").replace(
                                            "\r",
                                            "") + "\t" + str(user_id) + "\t" + str(
                                            total_review) + "\t" + published_date + "\n")
                                    obeserveList.remove(postId)
                                    print("remove ", postId)
                                    continue
                                timeDiff = int((datetime.datetime.now() - datetime.datetime.strptime(published_date,
                                                                                                     '%Y-%m-%d %H:%M:%S')).seconds / 60)
                                print("timeDiff:", timeDiff)
                                if timeDiff > THRESHOLD:
                                    cat = cnn_model.predict(content)
                                    print("cat", cat)
                                    if cat == "0":
                                        print("cat:0")
                                        f_noreply.write(
                                            "reason:info" + "\t" + str(postId) + "\t" + str(
                                                forum_id) + "\t" + title.strip().replace(
                                                "\n", "").replace("\r", "") + "\t" + content.strip().replace("\n",
                                                                                                             "").replace(
                                                "\r", "") + "\t" +
                                            str(user_id) + "\t" + str(total_review) + "\t" + published_date + "\n")
                                        obeserveList.remove(postId)
                                        print("remove ", postId)
                                        continue

                                    print("cat:1")
                                    # Randomly select half of the posts to reply 达到回复要求，选择half去回复
                                    try:
                                        if isComm:
                                            print("count", count)
                                            count += 1

                                            comment = toComment(postId, content, ua, authorization)
                                            print("will to comment:", AIName + " " + comment)
                                            if comment != "":
                                                logstr = "postId:" + str(
                                                    postId) + "\tAIName:" + AIName + "\tforum_id:" + str(
                                                    forum_id) + "\tuser_id:" + str(user_id) + \
                                                         "\tuser_name:" + user_name + "\ttitle:" + title.strip().replace(
                                                    "\n", "").replace("\r",
                                                                      "") + "\tcontent:" + content.strip().replace("\n",
                                                                                                                   "").replace(
                                                    "\r", "") + "\tdata：" + published_date + \
                                                         "\ttotal_floor:" + str(
                                                    total_floor) + "\tcomment:" + comment + "\ttimeDiff:" + str(
                                                    timeDiff) + "\n"

                                                f_reply.write(logstr)
                                        else:
                                            print("randomly not to reply")
                                            logstr = "reason:randon" + "\tpostId:" + str(postId) + "\tforum_id:" + str(
                                                forum_id) + "\tuser_id:" + str(user_id) + \
                                                     "\tuser_name:" + user_name + "\ttitle:" + title.strip().replace(
                                                "\n", "").replace("\r", "") + "\tcontent:" + content.strip().replace(
                                                "\n", "").replace("\r", "") + "\tdata：" + published_date + \
                                                     "\ttotal_floor:" + str(total_floor) + "\n"
                                            f_noreply.write(logstr)
                                        isComm = not isComm
                                    except Exception as e:
                                        print("Exception", e)
                                        print("AIName", AIName)

                                    obeserveList.remove(postId)
                                    print("remove ", postId)
                            print("current observed posts list：")
                            for postId in obeserveList:
                                print(postId)

                        if currentObeserveTime > OBSERVE_INTERVAL:
                            currentObeserveTime = 0

                        print("sleep with Comment_interval")
                        time.sleep(COMMENT_INTERVAL * 60)
                        currentObeserveTime += COMMENT_INTERVAL
                        print("currentObserveTime", currentObeserveTime)



                    except Exception as e:
                        print('Error:', e)
                        print("wrong！")
                        print("file save as", filename)
                        currentObeserveTime += COMMENT_INTERVAL
                        print("currentObserveTime", currentObeserveTime)

            f_hasOthers.close()
        f_noreply.close()
    f_reply.close()

    print("file save as", filename)
    print("end")


if __name__ == '__main__':
    main()
