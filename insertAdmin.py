from main import db
from sqlalchemy import insert
(
    insert(db).
    values(admin_id=1,admin_username='admin_01', password_hash='pwd')
)


