web: gunicorn jogovarejoweb.wsgi --log-file -

# Depois de inserir a linha abaixo (indicada por https://devcenter.heroku.com/articles/getting-started-with-python#provision-and-use-a-database,
# em conjunto com seu aplicativo de demonstracao do deploy), coloquei ela em comentário porque no deploy o "manage.py" não está funcionando, e 
# com isso o deploy não se completa. 
# Sem ela, pelo que estou entendendo, as migrações do banco de dados precisam ser executadas manualmente
# Segue também abaixo o comentario original explicativo da mesma: 

# Uncomment this `release` process if you are using a database, so that Django's model
# migrations are run as part of app deployment, using Heroku's Release Phase feature:
# https://docs.djangoproject.com/en/4.2/topics/migrations/
# https://devcenter.heroku.com/articles/release-phase

# release: ./manage.py migrate --no-input
