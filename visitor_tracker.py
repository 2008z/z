from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

# ملف لحفظ البيانات
DATA_FILE = "visitors.json"

def save_visitor_data(data):
    """حفظ بيانات الزائر في ملف JSON"""
    visitors = []
    
    # قراءة البيانات الموجودة
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            visitors = json.load(f)
    
    # إضافة بيانات جديدة
    visitors.append(data)
    
    # حفظ البيانات
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(visitors, f, indent=2, ensure_ascii=False)

@app.route('/')
def track_visitor():
    """تتبع بيانات الزائر"""
    
    # جمع البيانات
    visitor_info = {
        'timestamp': datetime.now().isoformat(),
        'ip_address': request.remote_addr,
        'user_agent': request.headers.get('User-Agent'),
        'referrer': request.headers.get('Referer'),
        'country': request.headers.get('CF-IPCountry', 'Unknown'),  # إذا استخدمت Cloudflare
        'path': request.path,
        'method': request.method
    }
    
    # حفظ البيانات
    save_visitor_data(visitor_info)
    
    # إرجاع صفحة بسيطة
    return '''
    <!DOCTYPE html>
    <html dir="rtl">
    <head>
        <title>مرحبا بك</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 50px;
                background: #f0f0f0;
            }
        </style>
    </head>
    <body>
        <h1>أهلا وسهلا!</h1>
        <p>شكراً لزيارتك</p>
    </body>
    </html>
    '''

@app.route('/admin/visitors')
def get_visitors():
    """عرض بيانات الزوار (محمي بكلمة مرور)"""
    
    # تحقق من كلمة المرور (غيّرها!)
    password = request.args.get('pass')
    if password != "123456":
        return jsonify({"error": "Unauthorized"}), 401
    
    # قراءة البيانات
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            visitors = json.load(f)
        return jsonify(visitors)
    
    return jsonify([])

if __name__ == '__main__':
    # لا تشغل debug=True في الإنتاج!
    app.run(debug=True, host='0.0.0.0', port=5000)
