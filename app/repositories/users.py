
from app.models.db import open_conn as get_conn
from app.models.schemas import UserPublic



def get_by_email(email: str):
    with get_conn() as c:
        r = c.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
    return dict(r) if r else None

    
def get_user_data(id) -> UserPublic:
    with get_conn() as c:
        r1 = c.execute("SELECT email,full_name FROM users WHERE id=?", (id,)).fetchone()
        r2 = c.execute("""SELECT user_id,name FROM user_roles join roles
                      on (role_id=id)
                      WHERE user_id=?""", (id,)).fetchall()
        role=[ r[1] for r in r2 ]
        active=1 if len(role) else 0      
        user=UserPublic(id=id,email=r1["email"],full_name=r1["full_name"],roles=role,is_active=active)
    return user if r1 else None

def create_user(email, full_name, password_hash):
    with get_conn() as c:
        cur = c.execute( """INSERT INTO users(email, full_name, password_hash) VALUES 
        (?,?,?)""",(email, full_name, password_hash) )
        c.commit()
    return {"id": cur.lastrowid, "email": email,"full_name": full_name, "password_hash": password_hash,
    "is_active": 1}
    
def set_new_user_full_name(full_name: str, id:int):
    with get_conn() as c:
        cur=c.execute( """
                      UPDATE users set full_name=? where id=?
                      """,(full_name,id))
        c.commit()
        
def set_new_password(hash: str, id:int) -> int:
    with get_conn() as c:
        cur=c.execute( """
                      UPDATE users set password_hash=? where id=?
                      """,(hash,id))
        c.commit()
        if cur.rowcount > 0:
            return 1   # úspěch
        else:
            return 0   # žádná změna (např. id neexistuje)
    
def get_user_list() -> list[UserPublic]:
    with get_conn() as c:
        r = c.execute("SELECT id,email,full_name FROM users order by email", ).fetchall()
        out=[]
        for osoba in r:
            r2 = c.execute("""SELECT user_id,name FROM user_roles join roles
                      on (role_id=id)
                      WHERE user_id=?""", (osoba["id"],)).fetchall()
            role=[ r[1] for r in r2 ]
            active=1 if len(role) else 0      
            user=UserPublic(id=osoba["id"],email=osoba["email"],full_name=osoba["full_name"],roles=role,is_active=active)
            out.append(user)
        return out
        
    