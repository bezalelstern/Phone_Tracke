# מערכת ניטור מכשירי טלפון


### מבוא
מערכת זו פותחה לניטור אינטראקציות בין מכשירים
- Neo4j לניתוח קשרים וגרפים
- Redis לשמירת נתונים בזיכרון וחישוב בזמן אמת
- Flask ליצירת שירותי REST
- Docker לקונטיינריזציה

### דרישות מקדימות
- Python
- Docker & Docker Compose
- Postman
- Git

### הוראות התקנה
1. שכפול המאגר:
```bash
git clone https://github.com/bezalelstern/Phone_Tracke.git
cd Phone_Tracke
``` 
### התקנת סימולטור ליצירת שיחות
git clone https://github.com/EnoshTsur/phone_dispatcher.git
pip install -r requirements.txt


2. יצירת סביבת Python:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# או
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

3. הרצת האימג'ים הנדרשים:
```bash
docker-compose up -d
```

### משימות הפרויקט
 הכנסה נכונה של המכשירים והאינטרקציות ביניהם לדאטה בייס.
כתיבת אנדפוינטס לקבלת נתונים כמו מסלולי אינטראקציות הפועלות על בלוטוס, האם יש מכשירים מקושרים וכמה מהם, וקבלת השיחה האחרונה לפי מכשיר מסויים.
### API Endpoints

```
POST /api/phone_tracker
GET /api/bluetooth_paths
GET /api/signal_strength
GET /api/connected_device/{id}
GET /api/is_connected/{from_device_id}&{to_device_id}
GET /api/recent_connection/{device_id}
```
