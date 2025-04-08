## 🧠 Gujuferro ChatBot

> O‘zbek tilida muloqot qiladigan, doimiy o‘rganishga tayyor, PostgreSQL bazasiga ulangan chatbot.

---

### ⚙️ Texnologiyalar

- `Python`
- [`ChatterBot`](https://github.com/gunthercox/ChatterBot)
- `PostgreSQL` (psycopg2 orqali)
- Custom JSON training dataset (`[{input, output}]` formatda)

---

### 📦 O‘rnatish

```bash
git clone https://github.com/sizningusername/gujuferro-chatbot.git
cd gujuferro-chatbot

# Virtual environment yaratish
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate

# Kutubxonalarni o‘rnatish
pip install -r requirements.txt
```

---

### ⚠️ Xatolik: `AttributeError: module 'time' has no attribute 'clock'`

Agar quyidagidek xatolik chiqsa:

```
AttributeError: module 'time' has no attribute 'clock'
```

🔧 **Yechim**:

1. Loyihangizdagi virtual environment ichiga kiring:
   ```
   env\Lib\site-packages\flask_sqlalchemy\__init__.py
   ```

2. Quyidagi kodni toping:
   ```python
   if sys.platform == 'win32':
       _timer = time.clock
   else:
       _timer = time.time
   ```

3. `time.clock` o‘rniga `time.perf_counter()` deb yozing:
   ```python
   _timer = time.perf_counter
   ```

> `time.clock()` Python 3.8+ versiyalarda o‘chirib tashlangan. Bu fix uni to‘g‘rilaydi.

---

### 🛠 Sozlash

`.env` fayl ichida PostgreSQL sozlamalarini yozing:

```
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/gujuferro
```

---

### 🧠 Trening

JSON fayllar `data/` papkasiga quyidagicha joylashtiriladi:

```json
[
  {
    "input": "Salom",
    "output": "Salom-salom! Qanday yordam bera olaman?"
  },
  {
    "input": "Qalaysiz?",
    "output": "Zo‘r, siz-chi?"
  }
]
```

**Training kodi:** (qarang yuqoridagi javoblarda bor)

---

### 🐘 PostgreSQL xatolik: `varchar(255)` cheklovi

Agar quyidagi xatolik chiqsa:

```
sqlalchemy.exc.DataError: значение не умещается в тип character varying(255)
```

🔧 **Yechim**:

```sql
ALTER TABLE statement
ALTER COLUMN text TYPE TEXT,
ALTER COLUMN in_response_to TYPE TEXT,
ALTER COLUMN search_text TYPE TEXT,
ALTER COLUMN search_in_response_to TYPE TEXT;
```

---

### 🗣 Chat rejimi

```python
while True:
    msg = input("Siz ➤ ")
    if msg.lower() in ["exit", "chiqish"]:
        break
    response = chatbot.get_response(msg)
    print("Gujuferro 🤖 ➤", response)
```

