# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import psycopg2

class PostgresURLPipeline:

    def __init__(self):
        ## Connection Details
        hostname = 'localhost'
        username = 'admin'
        password = 'NoLimit123'
        database = 'ScrapeMultiweb'
        port = 5432

        ## Create/Connect to database 
        self.connection = psycopg2.connect(
            host=hostname,
            dbname=database,
            user=username,
            password=password,
            port=port
        )

        ## Create cursor, used to execute commands
        self.cur = self.connection.cursor()

        ## Create quotes table if none exists
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS scraped_urls (
                id SERIAL PRIMARY KEY,
                url TEXT UNIQUE,
                domain TEXT
            )
        """)
        self.connection.commit()

    def close_spider(self, spider):
        self.connection.commit()
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        try:
            self.cur.execute(
                "INSERT INTO scraped_urls (url, domain) VALUES (%s, %s) ON CONFLICT (url) DO NOTHING",
                (item["url"], item["domain"])
            )
        except Exception as e:
            spider.logger.warning(f"[DB] Gagal simpan URL: {item.get('url')} | Error: {e}")
        return item

