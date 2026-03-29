
```
# Sub-diretórios
commands     # Commands made available to manage.py
forms        # WTForms
models       # Database Models and their Forms
static       # Static asset files that will be mapped to the "/static/" URL
templates    # Jinja2 HTML template files
views        # Routes + Controllers = views 
```


Não trocar a ordem de 
```python
@login_required
@role_required(...)
```
