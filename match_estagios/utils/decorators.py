from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user


def roles_required(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Faça login para acessar", "warning")
                return redirect(url_for("auth.login"))

            if current_user.role not in roles:
                flash("Você não tem permissão para acessar esta página", "danger")
                return redirect(url_for("main.index"))

            return func(*args, **kwargs)

        return wrapper

    return decorator
