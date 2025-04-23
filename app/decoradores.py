from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user


def admin_required(f):
    """
    Decorador de rota para restringir acesso a administradores.

    Verifica se o usuario atual é administrador. Caso contrário, redireciona para
    a página inicial com uma mensagem de erro.

    Args:
        f (Callable): Função de rota protegida.

    Returns:
        Callable: Função decorada.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash("Você não tem permissão para acessar esta página.", "error")
            return redirect(url_for("main.index"))
        return f(*args, **kwargs)
    return decorated_function