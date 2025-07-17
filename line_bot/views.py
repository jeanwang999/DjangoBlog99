from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from linebot.models import LocationMessage, StickerMessage, StickerSendMessage, ImageMessage, ImageSendMessage



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
                            TextSendMessage(text="報到成功!!!")
                        )
                    elif event.message.text == "###我的名牌###":
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text="您的編號是 001 !")
                        )
                    elif event.message.text == "###我要簽名###":
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text="ABC-123 簽名成功")
                        )
                    else:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text="目前尚未開放詢問喔")
                        )
                        
                elif isinstance(event.message, LocationMessage):
                    print("收到定位訊息:", event)
                    line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text="緯度:{}, 經度:{}".format(event.message.latitude, event.message.longitude))
                        )
                elif isinstance(event.message, StickerMessage):
                    print("收到貼圖:", event.message)                        
                    line_bot_api.reply_message(
                        event.reply_token,
                        StickerSendMessage(
                            446,
                            1988,
                        )
                    )
                elif isinstance(event.message, ImageMessage):
                    print("收到圖片", event.message)
                    image_name = event.message.id + ".jpg"
                    image_content = line_bot_api.get_message_content(event.message.id)
                    path = "./public/uploads/" + image_name
                    with open(path, 'wb') as fd:
                        for chunk in image_content.iter_content():
                            fd.write(chunk)
                    reply_image_path = "https://{}/media/{}".format(request.get_host(), image_name)
                    line_bot_api.reply_message(
                        event.reply_token,
                        ImageSendMessage(
                            preview_image_url=reply_image_path,
                            original_content_url=reply_image_path,
                        )
                    )

                else:
                    print("文字以外的類型\n")
            else:
                print("非訊息事件")
    return HttpResponse()
