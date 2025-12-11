from app.models.db import open_conn as get_conn

def get_role_id(name: str):
    with get_conn() as c:
        r = c.execute("SELECT id FROM roles WHERE name=?", (name,)).fetchone()
    return r["id"] if r else None

def get_roles_list():
    with get_conn() as c:
        r = c.execute("SELECT id,name FROM roles ").fetchall()    
    return dict(r) if r else None

def assign_role(user_id: int, role_id: int):
    with get_conn() as c:
        c.execute("INSERT INTO user_roles(user_id, role_id) VALUES (?,?)", (user_id, role_id))
        c.commit()
        
def user_roles(user_id: int) -> list[dict]:
    with get_conn() as c:
        rows = c.execute("""
            SELECT roles.name,user_role_id FROM roles
            JOIN user_roles ur ON ur.role_id = roles.id
            WHERE ur.user_id = ?""", (user_id,)).fetchall()
    return [{ "role" : r["name"], "role_id" : r["user_role_id"]} for r in rows]

def repo_odstran_pravo(id):
    print(id)
    with get_conn() as c:
        c.execute("delete from user_roles where user_role_id=?", (id,))
        c.commit()