import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))  # ✅ ดึง PORT จาก Railway ถ้ามี ถ้าไม่มีใช้ 5001
    app.run(host='0.0.0.0', port=port, debug=False)
