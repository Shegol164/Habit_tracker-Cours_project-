from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from .models import User # Убедитесь, что models.py существует и содержит User, или импортируйте правильно
from django.conf import settings

@method_decorator(csrf_exempt, name='dispatch')
class TelegramWebhookView(View):
    def post(self, request, *args, **kwargs):
        try:
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            message = body_data.get('message')
            if not message:
                return JsonResponse({'status': 'ok'})

            chat_id = message['from']['id']
            username = message['from'].get('username', 'Unknown')
            text = message.get('text', '')

            # Простая диалоговая логика на русском
            if text == '/start':
                reply_text = (
                    f"Привет, {username}! Это бот для напоминаний о привычках.\n"
                    "Чтобы я мог отправлять тебе напоминания, тебе нужно связать свой аккаунт в приложении с этим Telegram-аккаунтом.\n"
                    "Пожалуйста, введи команду вида: `/set_chat_id`"
                )
            elif text == '/set_chat_id':
                reply_text = (
                    "Введите свой ID пользователя из веб-приложения в формате:\n"
                    "`/link 123`"
                )
            elif text.startswith('/link'):
                try:
                    # ... (логика обработки /link)
                    # Пример (проверьте импорт User):
                    from users.models import User # Импортируйте правильно
                    parts = text.split()
                    if len(parts) != 2:
                        raise ValueError
                    user_id = int(parts[1])
                    user = User.objects.get(id=user_id)
                    # ... (остальная логика)
                except (ValueError, IndexError, User.DoesNotExist):
                     reply_text = "❌ Неверный формат команды или ID пользователя не найден. Попробуйте еще раз."
            else:
                reply_text = "Я понимаю только команды:\n/start\n/set_chat_id\n/link <user_id>"

            from notifications.telegram import send_telegram_message
            send_telegram_message(chat_id, reply_text)

            return JsonResponse({'status': 'ok'})
        except Exception as e:
            print(f"Ошибка обработки вебхука Telegram: {e}")
            return JsonResponse({'status': 'error'}, status=500)