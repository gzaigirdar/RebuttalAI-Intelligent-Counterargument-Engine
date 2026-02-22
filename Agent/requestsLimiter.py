import sqlite3
import time

class RateLimiter:
    def __init__(self):
        self.limit_size = 500
        self.db_path = "rate_limit_db.sqlite"
        self.window_max = 3600
        self._init_db() 

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS rate (
                    id INTEGER PRIMARY KEY,
                    count INTEGER NOT NULL,
                    window_start INTEGER NOT NULL
                )
            """)
         
            conn.execute(
                "INSERT OR IGNORE INTO rate (id, count, window_start) VALUES (1, 0, 0)"
            )

    def is_limit_reached(self):
        now = int(time.time())
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
          
            cursor.execute("BEGIN IMMEDIATE")
            
            cursor.execute("SELECT count, window_start FROM rate WHERE id=1")
            row = cursor.fetchone()
            count, window_start = row['count'], row['window_start']

            if now > (window_start + self.window_max):
                new_count = 1
                new_window_start = now
            else:
                if count >= self.limit_size:
                    return True 
                new_count = count + 1
                new_window_start = window_start

           
            cursor.execute(
                "UPDATE rate SET count=?, window_start=? WHERE id=1",
                (new_count, new_window_start)
            )
            conn.commit()
            
        return False