# Painel Operacional — Apache Superset

Dashboard operacional open-source com dados fake de pedidos, rodando em Docker e exposto via Cloudflare Tunnel.

**Live demo:** https://supersetportifolio.sinapsebi.com.br/superset/dashboard/1/?standalone=true

**Dashboard ID:** `1` (numeric — use for direct URL access)

---

## Stack

| Ferramenta | Função |
|---|---|
| Apache Superset 3.1 | BI e visualização |
| PostgreSQL 15 | Banco de dados dos pedidos |
| Docker Compose | Orquestração dos containers |
| Cloudflare Tunnel | Exposição segura sem abrir portas |

## Dataset

1 200 pedidos sintéticos (2024) com:
- **Produtos:** Eletrônicos, Mobiliário, Periféricos
- **5 vendedores · 20 clientes · 5 regiões**
- **Status:** Entregue / Em trânsito / Cancelado
- **Métricas de entrega:** prazo vs realizado

---

## Como rodar

### 1. Subir os containers

```bash
cd projects/superset-panel
docker compose up -d
```

O PostgreSQL já sobe com a tabela `pedidos` carregada automaticamente via `db/init.sql`.

### 2. Inicializar o Superset (apenas na primeira vez)

```bash
chmod +x setup.sh && ./setup.sh
```

Acesse **http://localhost:8089** · login: `admin` / `admin`

### 3. Configurar no Superset

1. **Settings → Database Connections → + Database**
   - PostgreSQL
   - URI: `postgresql+psycopg2://superset:superset@db:5432/operacional`
   - Nome: `Dados Operacionais`

2. **Datasets → + Dataset** → seleciona `pedidos`

3. Cria os charts e monta o Dashboard

---

## Cloudflare Tunnel

No painel do Cloudflare Zero Trust, em **Tunnels → seu tunnel → Edit → Public Hostname**:

| Subdomain | Domain | Service |
|---|---|---|
| `supersetportifolio` | `sinapsebi.com.br` | `http://localhost:8089` |

O dashboard fica acessível em `https://supersetportifolio.sinapsebi.com.br`.

---

## Embed no portfólio

Após criar o dashboard no Superset:

1. Abre o dashboard → menu **⋮ → Embed dashboard**
2. Adiciona `sinapsebi.com.br` nos domínios permitidos
3. Copia o `<iframe>` gerado
4. Cola no `index.html` dentro do card do projeto

Ou usa o link de compartilhamento público com `?standalone=true`:
```
https://supersetportifolio.sinapsebi.com.br/superset/dashboard/1/?standalone=true
```
