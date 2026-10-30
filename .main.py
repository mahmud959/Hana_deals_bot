import os
import time
import requests

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

API = f"https://api.telegram.org/bot{TOKEN}"

def send_message(text):
    requests.post(
        f"{API}/sendMessage",
        json={"chat_id": CHAT_ID, "text": text},
        timeout=30
    ).raise_for_status()

def main():
    send_message(
        "✅ بوت محمود شغال بنجاح!\n"
        "قريباً هنبدأ مراقبة عروض Amazon.eg\n"
        "الحد الأدنى للخصم: 50%"
    )

    offset = None

    while True:
        try:
            response = requests.get(
                f"{API}/getUpdates",
                params={"offset": offset, "timeout": 30},
                timeout=35
            )
            response.raise_for_status()

            for update in response.json().get("result", []):
                offset = update["update_id"] + 1
                message = update.get("message", {})
                chat = message.get("chat", {})
                text = message.get("text", "")

                if str(chat.get("id")) == CHAT_ID:
                    if text == "/start":
                        send_message("أهلاً محمود! البوت جاهز لاستقبال أوامرك.")
                    elif text == "/test":
                        send_message("✅ الاتصال شغال تمام!")

        except Exception as error:
            print("Error:", error)
            time.sleep(10)

if __name__ == "__main__":
    main()
