from kafka import KafkaConsumer
import psycopg2
import json

consumer = KafkaConsumer(
    'scraped_urls_topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='scrape-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

conn = psycopg2.connect(
    dbname='ScrapeMultiweb',
    user='admin',
    password='NoLimit123',
    host='localhost',
    port='5432'
)
cur = conn.cursor()

print("Consumer berjalan dan menunggu pesan...")

for message in consumer:
    item = message.value
    print(f"[Kafka → DB] Menerima item: {item['url']}")
    try:
        cur.execute(
            "INSERT INTO scraped_urls (url, domain) VALUES (%s, %s) ON CONFLICT (url) DO NOTHING",
            (item['url'], item['domain'])
        )
        conn.commit()
        print(f"[DB] Tersimpan: {item['url']}")
    except Exception as e:
        print(f"[DB] Gagal simpan: {e}")
