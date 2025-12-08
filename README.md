# como rodar

```
docker compose build

docker compose up -d

// executar somente depois de rodar as migrations com o up -d, backend necessita estar de pé
docker compose exec backend python manage.py create_initial_data

usuarios cadastrados:

# permissao pra tudo
admin
123

# permissao pra editar somente os conteudo dele
autor
123

# leitor permissao para salvar favoritos
leitor
123
```

### Como testar

O frontend vai estar rodando em localhost:3000
