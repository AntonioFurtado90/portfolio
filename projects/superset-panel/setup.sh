#!/bin/bash
# Executa UMA VEZ após o primeiro `docker compose up -d`
# Aguarda o Superset estar pronto e configura admin + conexão com o banco

set -e

echo "⏳ Aguardando Superset inicializar..."
until docker exec portfolio-superset superset version &>/dev/null; do sleep 3; done

echo "📦 Atualizando schema do banco de metadados..."
docker exec portfolio-superset superset db upgrade

echo "👤 Criando usuário admin..."
docker exec portfolio-superset superset fab create-admin \
  --username admin \
  --firstname Admin \
  --lastname Superset \
  --email ae.furtado90@gmail.com \
  --password admin \
  2>/dev/null || echo "  (usuário já existe, ignorando)"

echo "🔑 Inicializando roles e permissões..."
docker exec portfolio-superset superset init

echo ""
echo "✅ Pronto! Acesse http://localhost:8089"
echo "   Login: admin / admin"
echo ""
echo "👉 Próximos passos dentro do Superset:"
echo "   1. Settings → Database Connections → + Database"
echo "      URI: postgresql+psycopg2://superset:superset@db:5432/operacional"
echo "   2. Datasets → + Dataset → tabela pedidos"
echo "   3. Charts → criar gráficos → montar Dashboard"
echo "   4. Dashboard → ⋮ → Embed dashboard → copiar link"
