import sqlite3

def init_db():
    conn = sqlite3.connect('takaful.db')
    cursor = conn.cursor()

    # إنشاء جدول الفئات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    # إنشاء جدول الاحتياجات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS needs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER,
            title TEXT,
            description TEXT,
            goal REAL,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    ''')

    # إنشاء جدول التبرعات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            need_id INTEGER,
            amount REAL,
            payment_method TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (need_id) REFERENCES needs(id)
        )
    ''')

    # إضافة بيانات افتراضية للفئات
    cursor.execute('SELECT COUNT(*) FROM categories')
    count = cursor.fetchone()[0]
    if count == 0:
        categories = [
        ('Food Support',),
        ('Water & Drinking Projects',),
        ('Refugee & Shelter',),
        ('Education & Capacity Building',),
        ('Medical Aid & Healthcare',),
        ('Clothing & Essentials',),
        ('Psychological Support for Children',),
        ('Special Needs Support',),
        ('Funeral Assistance',),
        ('General Support for Partner Organizations',)
    ]
        cursor.executemany('INSERT INTO categories (name) VALUES (?)', categories)

    # إضافة بعض الاحتياجات للعرض
    cursor.execute('SELECT COUNT(*) FROM needs')
    count_needs = cursor.fetchone()[0]
    if count_needs == 0:
        needs = [
            (1, 'Food Support', 'Emergency food supplies needed for displaced families in Blue Nile state 500 families require immediate food assistance, including rice, lentils, and cooking oil for one month.', 1000),
            (2, 'Water & Drinking Projects', 'Clean drinking water provision Portable water tanks and filtration units are required in Khartoum outskirts where existing water infrastructure is damaged This project aims to serve 2,000 displaced persons.', 2000),
            (3, 'Refugee & Shelter', 'Tents for displaced persons Provision of 300 emergency-grade tents for families fleeing violence in South Kordofan Each tent accommodates 5–6 people and includes weather protection.', 3000),
            (4, 'Education & Capacity Building', 'Supporting burial costs Fund assistance for displaced families unable to cover burial expenses Each funeral package includes shroud, transportation, and grave digging.', 4000),
            (5, 'Medical Aid & Healthcare', 'Educational supplies Back-to-school kits with notebooks, pencils, and backpacks needed for 1,000 displaced children in Omdurman camps.', 5000),
            (6, 'Clothing & Essentials', 'Surgical operations funding Emergency surgical interventions for injured civilians in conflict zones Focus on trauma surgeries in El Fasher with estimated cost per patient: $250.', 6000),
            (7, 'Psychological Support for Children', 'Cash donations for clothing Seasonal clothing stipends for displaced families in North Darfur to buy essential garments for children and adults.', 7000),
            (8, 'Special Needs Support', 'Establish mobile child-friendly spaces with psychological counseling, art therapy, and safe play zones for traumatized children in camps near Port Sudan.', 8000),
            (9, 'Funeral Assistance', 'Infant care essentials Monthly baby care kits for mothers in displacement camps, including diapers, formula milk, and baby soap for 200 infants.', 9000),
            (10, 'General Support for Partner Organizations', 'Joanna Amal.', 10000)
        ]
        cursor.executemany('INSERT INTO needs (category_id, title, description, goal) VALUES (?, ?, ?, ?)', needs)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()