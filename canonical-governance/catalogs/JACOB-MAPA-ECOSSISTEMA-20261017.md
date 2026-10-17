# Jacob OS — mapa canônico consolidado de infraestrutura e projetos
Atualização: 2026-10-17. **Estado: inventário verificado parcialmente, não implantação concluída.**

## Regra de consulta
Antes de nova busca, ler este documento e seus recibos de fonte. Marcar todo item como CONFIRMADO (resultado de CLI/conector), HISTÓRICO (contrato ou relato anterior), ou NÃO COMPROVADO. Nunca converter hipóteses em fatos. Não registrar valores de tokens, URLs contendo senha, variáveis secretas, dumps ou backups em Git.

## Jacob OS 2 — local
- `D:\JacobOS2`, Home/Developer aprovado `8803` (congelado); backend S0 `8787`, Bus `8788` (HISTÓRICO COM EVIDÊNCIAS 17/10). Não modificar Home/ledger.
- `supreme-s0`: SHA `1d7969d384aafe47c8a42783a193871e17d9a5c4`, 965 entradas dirty; `lane-backend`: SHA `b1359f7096ea617e8b2b22a801556c7cc15895d7`, limpo; `deploy-agents-activation-20261016`: SHA `839db2c408b6de919a749831e93cbf81552ac572`, 29 dirty.
- Publicador existente: `D:\JacobOS2\canonical-governance\deploy-center\jacob-deploy.ps1`, `release-dispatch.mjs`, `RELEASE-DISPATCH-20261016.md`, `DEPLOY_ACCESS_MATRIX.json`, `DEPLOY_CAPABILITY_MATRIX.json` e recibos locais; não presumir que testes/recibos antigos representam deploy atual.
- Restore local preexistente `D:\JacobOS2\canonical-governance\restore-points\RP-8787-8803-20261017T171841Z`; 372 hashes verificados conforme relato, restauração efetiva não comprovada. Não é ponto remoto de Staging.

## Jacob Staging — front e back
- Frontend público: `https://staging.jacobos.com.br/`, Cloudflare frontdoor (CONFIRMADO endpoint HTTP 200; versão servida e Pages/Worker projeto **NÃO COMPROVADOS** nesta auditoria).
- Backend público `https://api-staging.jacobos.com.br/health`: HTTP 200 no PowerShell 17/10. Cloudflare DNS CNAME PROXIED: `api-staging.jacobos.com.br` -> `jacob-real-staging-api.onrender.com` (CONFIRMADO pela API Cloudflare, 17/10).
- Origem Render correspondente **EXATA**: `jacob-real-staging-api`, service `srv-d9bh207avr4c73aluds0`; repo `jasonfrancamusic/jacob-os`, branch `feature/jacob-real-integrations-full`, `rootDir=backend`, `autoDeploy=no`. CONFIRMADO via Render.
- **NÃO CONFUNDIR** `jacob-real-staging-api-r2`, service `srv-darbje0u01pc73c7jpn0`, URL diferente, mesmo repo/branch, rootDir vazio. Não é o alvo do CNAME fornecido.
- Cloudflare account `94022a58018cc2b38826702a5f2014d4`; Wrangler 4.151.0 autenticação existente via variável de ambiente (CONFIRMADO). DNS A públicos são IPs de proxy, não origem.
- Google Cloud CLI autenticada, projeto ativo `jacob-os-real-staging`; consulta `gcloud run services list` não retornou serviços; isso não exclui Compute Engine/IAP/recursos em outros projetos. Backend atual se resolve no Render segundo DNS.
- Banco PostgreSQL realmente usado por `srv-d9bh207avr4c73aluds0`: **AINDA NÃO COMPROVADO**. Não assumir que projetos Neon antigos atendem o serviço; identificar somente NOME das variáveis de conexão via configuração e então testar vínculo sem vazar senha.
- Ponto de restauração remoto de banco + frontend + backend **AINDA NÃO CRIADO/VALIDADO**.

## Render — workspace e catálogo atual (23 serviços)
Workspace `tea-d95g75vaqgkc73f375k0` — conexão Render autenticada no ChatGPT e Render CLI 2.29.0 autenticada no Windows. `autoDeploy` de cada serviço requer confirmação antes de commit.

| Serviço | ID Render | Classe |
|---|---|---|
| jacob-real-staging-api | srv-d9bh207avr4c73aluds0 | origem pública api-staging |
| jacob-real-staging-api-r2 | srv-darbje0u01pc73c7jpn0 | candidato separado |
| jacob-cloud-lanes-staging | srv-dah5n0e1egvs73cn85mg | cloud lanes |
| jacob-autonomy-worker-staging | srv-dajnrdbm8hqs7391b8k0 | autonomia |
| jacob-sovereign-brain-staging | srv-dajnm4oae00c73amlgg0 | brain |
| jacob-second-brain-staging | srv-dal1d0ek1f9s73dbo590 | Second Brain serviço |
| jacob-browser-qa-staging | srv-darsf0jbc2fs738c6sgg | browser QA |
| jacob-jev-canary | srv-darrom0jo6nc7396543g | JEV canary |
| jacob-evolution-staging-r165 | srv-dardjlp42hec73aas180 | Evolution |
| jacob-nekocore-staging | srv-dal12je7bikc73e063d0 | NekoCore |
| jacob-p00-test-runner2-staging | srv-dakq90ajnfac73bjbg70 | teste |
| jacob-p00-test-runner-staging | srv-dakq8oajnfac73bjacq0 | teste |
| jacob-cleanroom-colocated-staging-r2 | srv-dakhvs7qj5pc73b8d090 | cleanroom |
| jacob-oss-brain-staging-r2 | srv-dakhpqlg1s2s73ccha20 | OSS brain |
| jacob-oss-brain-staging | srv-dakgj2h594qs73e0liug | OSS brain |
| jacob-ultrarag-staging | srv-dakggt3m8hqs73ehbibg | RAG |
| jacob-cleanroom-sovereign-colocated-staging | srv-dak7pc3l550s73a7vaa0 | cleanroom |
| jacob-google-workspace-staging-preview | srv-dak6idh42hec739o6rqg | Workspace |
| jacob-openbitfun-runtime-staging-r2 | srv-dak5ta7f3r2c73c75n0g | runtime |
| jacob-openbitfun-runtime-staging | srv-dak5sgek1f9s73ehhtd0 | runtime |
| jacob-family-api-free-r1 | srv-d9t8llqjobas73cb47b0 | family API |
| jacob-evolution-canary | srv-d9drunjtqb8s739bb58g | Evolution canary |
| jacob-family-api | srv-d95iura8qa3s73e2oav0 | family API |

## Neon, PostgreSQL, skills e MCP
- Neon CLI Windows `8.8.0`, organização `org-purple-grass-35904219` autenticada. Diretório de contexto criado em `C:\Windows\System32\.neon` por execução a partir dessa pasta; não deslocar ou substituir sem verificar arquivos locais já existentes.
- Neon MCP no ChatGPT CONECTADO: `list_projects` funcionou. No Codex houve `invalid_token` em 17/10, depois servidor MCP neon registrado e fluxo OAuth iniciado; estado final do MCP Codex **NÃO COMPROVADO**. Codex esgotado até 22/10 e Claude até 20/10 segundo Founder. Não requisitar executores indisponíveis.
- **Skill Neon já instalada neste ChatGPT**, com `neon`, `neon-postgres`, `neon-postgres-branches`, `neon-auth`, `neon-functions`, `neon-object-storage`, `neon-ai-gateway`, `neon-postgres-egress-optimizer` (skills list consultada). Skill no Windows/projeto Jacob OS 2 **NÃO INSPECIONADA**; não declarar instalada.
- Projetos Neon listados: `crimson-salad-15823867` (Second Brain preservation, branch READY), `restless-bird-11729639` (staging recovery, branches ARCHIVED), `withered-wind-81012251` e `odd-darkness-67663809` (staging-state históricos, branches ARCHIVED), `twilight-math-53576188` (production bridge), `bitter-hall-59212521` (production-state). A classificação staging/produção não determina serviço consumidor.
- PostgreSQL client Windows `17.11` instalado `C:\Program Files\PostgreSQL\17\bin`; `psql`, `pg_dump`, `pg_restore`, `pg_isready` verificados. Banco confirmado `second_brain_preservation`, host `ep-autumn-shadow-b4mvki3t.c-6.us-east-2.aws.neon.tech`, user `second_brain_preserver`, porta implícita `5432`. `psql` SELECT funcionou; `pgpass.conf` criado no perfil Windows (segredo: jamais copiar); TLS não provado no primeiro comando porque `sslmode=require` foi ignorado. Para pg_dump em servidor PG 18 instalar cliente PG 18.
- O banco principal `D:\JacobOS2` e outros PostgreSQL operacionais **não devem ser confundidos com** esse banco de preservação.

## Jacob Produção
- Backend público histórico: `https://api.jacobos.com.br/` (origem corrente NÃO VERIFICADA nesta auditoria).
- Frontend Produção, plataforma Pages/Worker, branch/tag, release SHA, datastore PostgreSQL, rollback e serviços GCP/Render exatos: **MAPEAMENTO A COMPLETAR** com evidência de DNS e configuração de deploy. Não equiparar frontends Produção e Staging nem acionar deploy de Produção sem ordem.

## Multiverso Social Agents (MSA)
- Produto independente `Multiverso Social Agents`; destino planejado/aprovado `multiversoagents.jacobos.com.br` e intenção anterior `agents.jacobos.com.br` (HISTÓRICO de decisões). Frontend publicado, backend real, serviço Cloud, branch, DB, domínio DNS vigente, último SHA e rollback: **NÃO COMPROVADOS**. Status anterior 404 `/api/v1/social-agents/status` e Cloudflare Worker 1101; não supor que persistem atualmente.

## Férias com Propósito
- Projeto independente com continuidade e inscrições/pagamentos solicitados (HISTÓRICO). Repositório GitHub, domínio frontend, backend, banco, hosting, staging/prod, deploy SHA e rollback **NÃO IDENTIFICADOS** por esta auditoria. Não confundir `jacob-family-api` com Férias com Propósito sem evidência.

## Jacob Jobs
- Repositório comprovado `jasonfrancamusic/jacob-jobs`, projeto decidido `jobs.jacobos.com.br` (domínio planejado). Frontend/backend, hosting, DB e SHA efetivamente servidos: NÃO COMPROVADOS.

## Repositórios GitHub acessíveis
`jasonfrancamusic/jacob-os2-sovereign`, `jasonfrancamusic/jacob-os`, `jasonfrancamusic/jacob`, `jasonfrancamusic/jacob-jobs`, `jasonfrancamusic/jacob-local-agent-sandbox`. Escritas anteriores de contratos foram comprovadas em 17/10, mas a tentativa posterior de atualização via conector GitHub foi bloqueada. Sincronização local via PowerShell anterior falhou no `gh api GET` de arquivo inexistente (404), não implica falha de autenticação GitHub; consertar condição de ausência para criar conteúdo com PUT.

## Regra canônica de publicação
`PUBLICAR` => capturar UM ponto anterior realmente recuperável (banco/artefato/serviço conforme necessário) => publicar frontend/backend no destino correto => confirmar versão servida => opção única `RESTAURAR`. Sem novas confirmações repetitivas, sem Codex/Claude durante cotas, sem reiniciar estruturas congeladas.

## Missões permanentes até mapa 100% comprovado
1. Identificar vínculo efetivo de datastore do Render `srv-d9bh207avr4c73aluds0` pelo NOME das variáveis; não exportar valores secretos.
2. Identificar artefato/frontend Staging em Cloudflare Pages e frontdoor Worker, SHA servido, versão anterior recuperável.
3. Mapear frontend/backend/DB/release de Produção (read-only até ordem explícita), MSA, Férias com Propósito e Jobs por DNS, repos, serviços e variáveis NOMINAIS.
4. Inspecionar presença de agent skills Neon e MCP dentro dos workspaces Windows sem sobrescrever configuração. Instalar somente o que realmente falta mediante CLI oficial.
5. Criar e validar ponto de restauração remoto correto, implantar atualização solicitada e registrar comprovantes reais.
6. Sincronizar atualizações com contratos, trilhas, catálogos e missões locais/Cloud, sem incluir segredos.
