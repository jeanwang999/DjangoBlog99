from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
# Create your views here.


line_bot_api = LineBotApi(settings.LINE_CHANNEL_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SERCRET)


@csrf_exempt
def callback(request):
    if (request.method == "POST"):
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    print("收到訊息:", event.message.text, "\n")
                    if event.message.text == "###我要報到###":
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text = "報到成功!!!" )
                        )
                    elif event.message.text == "###我的名牌###":
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text = "您的編號是 001 !" )
                        )
                    elif event.message.text == "###我要簽名###":
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text = "ABC-123 簽名成功" )
                        )
                    else:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text = "目前尚未開放詢問喔" )
                        )

                else:
                    print("文字以外的類型\n")
            else:
                print("非訊息事件")
    return HttpResponse()
