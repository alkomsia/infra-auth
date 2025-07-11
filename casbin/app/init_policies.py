import casbin
from casbin_sqlalchemy_adapter import Adapter
import os

db_url = os.environ.get("DATABASE_URL", "postgresql://user:pass@localhost/casbindb")
adapter = Adapter(db_url)
enforcer = casbin.Enforcer("model.conf", adapter)

enforcer.add_policy("admin", "/dashboard", "GET")
enforcer.add_policy("admin", "/settings", "POST")
enforcer.add_grouping_policy("alice", "admin")
enforcer.save_policy()

print("Policies initialized.")
