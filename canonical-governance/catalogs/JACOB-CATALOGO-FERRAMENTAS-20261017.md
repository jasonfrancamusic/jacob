# Jacob OS — Catálogo único de ferramentas e integrações

**Atualização:** 2026-10-17. **Referência cruzada:** `JACOB-MAPA-ECOSSISTEMA-20261017.md` já confirmado em 4 arquivos locais e 20 arquivos GitHub (cinco repositórios). As ferramentas abaixo são classificadas como CONFIRMADO (teste recente), HISTÓRICO (conversas/contratos) ou PENDENTE (precisa de teste atual). Não registrar tokens, URL de conexão com senha nem `.env`.

## Fonte de verdade
- Local: `D:\JacobOS2\canonical-governance\catalogs\JACOB-CATALOGO-FERRAMENTAS-20261017.md`, com cópias em `contracts`, `knowledge`, `missions/JACOB-TOOLS-INVENTORY-20261017/MISSION.md` e evidências JSON em `D:\JacobOS2\receipts\TOOLS-INVENTORY-...`.
- Cloud: espelhos canônicos em `jasonfrancamusic/jacob-os2-sovereign`, `jasonfrancamusic/jacob-os`, `jasonfrancamusic/jacob`, `jasonfrancamusic/jacob-jobs`, `jasonfrancamusic/jacob-local-agent-sandbox`. **Espelhos são documentação, não deploy ou garantia de sincronização operacional.**
- Catálogo vivo gerado pelo script: `TOOL-REGISTRY.json` (estado real observável da máquina, sem conteúdo de segredo). Cada linha identifica `provider`, `tipo`, `localizacao`, `ambiente`, `estado`, `comando`, `evidencia_utc`, `responsavel`.
- Em toda retomada, consultar o catálogo antes de buscar/reinstalar. Se faltar um campo, marcar PENDENTE e verificar apenas esse campo. Conservar IDs de serviço e projeto, não credenciais.

## Ferramentas de infraestrutura e publicação
| Ferramenta | Integração / localização conhecida | Verificação |
|---|---|---|
| Git | Windows, em PATH; repos em `D:\JacobOS2` | CONFIRMADO CLI; worktrees sujos NÃO limpar |
| GitHub CLI `gh.exe` | Autenticada `jasonfrancamusic`; `repo,workflow`; cinco repositórios | CONFIRMADO 20 gravações, 0 erros em 17/10 |
| GitHub Actions / colaboração IA | Repos GitHub; consultar workflows por repositório | PENDENTE mapeamento individual de workflows e runners |
| Cloudflare `wrangler.cmd` | CLI v4.151.0; account `94022a58018cc2b38826702a5f2014d4` | CONFIRMADO autenticação; escopo de Pages/Workers PENDENTE |
| Cloudflare DNS | `api-staging.jacobos.com.br` CNAME **proxied** -> `jacob-real-staging-api.onrender.com` | CONFIRMADO API Cloudflare; demais frontdoors PENDENTE |
| Cloudflare Pages / Worker / R2 | Frontend Staging e frontdoor no histórico; listar projects, routes e deploys reais | PENDENTE inventário de projetos e últimas versões |
| Render CLI `render.exe` | `%LOCALAPPDATA%\JacobOS\bin\render.exe`, v2.29.0; workspace `tea-d95g75vaqgkc73f375k0` | CONFIRMADO login; Render conector listou 23 serviços |
| Render Staging API real | `srv-d9bh207avr4c73aluds0`, `jacob-real-staging-api.onrender.com`, repo legado branch `feature/jacob-real-integrations-full`, pasta `backend` | CONFIRMADO vínculo DNS; banco DB pendente |
| Render Staging API r2 | `srv-darbje0u01pc73c7jpn0`, `jacob-real-staging-api-r2.onrender.com` | CONFIRMADO serviço diferente, NÃO é domínio público |
| GCP `gcloud.cmd` | Conta `jasonfrancamusic@gmail.com`, projeto `jacob-os-real-staging` | CONFIRMADO autenticação; Cloud Run sem serviços listados |
| GCP Compute Engine / IAP | Governança e recuperação local/cloud históricas | PENDENTE instâncias, regiões, IPs, rótulos e dependências |
| Node / npm | Windows, PATH | CONFIRMADO; versões no novo recibo |
| PostgreSQL CLI | `C:\Program Files\PostgreSQL\17\bin` 17.11 | CONFIRMADO; `pg_dump 17` incompatível com servidores PG18 para dump |
| Neon CLI `neon.cmd` | 8.8.0, org `org-purple-grass-35904219`; contexto específico pode estar em `C:\Windows\System32\.neon` | CONFIRMADO OAuth, 6 projetos |
| Neon MCP no ChatGPT | Conector Neon disponível e `list_projects/list_branches` funcionam | CONFIRMADO ChatGPT; MCP no Codex apenas REGISTRADO, auth não comprovada |
| Neon Skill ChatGPT | `neon`, `neon-postgres`, `neon-postgres-branches`, `neon-auth`, `neon-functions`, `neon-object-storage`, `neon-ai-gateway`, `neon-postgres-egress-optimizer` | CONFIRMADO neste ChatGPT; diferente da instalação no Windows |
| Neon Skill Windows | `neon skills -s ... -y` falhou: `No coding agents detected`; asserção libuv | NÃO INSTALADO por tentativa 17/10; usar `--agent codex` somente após confirmar target, ou instalar SKILL.md em diretório neutro de skills sem sobrescrever |
| PostgreSQL `pgpass.conf` | `%APPDATA%\postgresql\pgpass.conf` | CONFIRMADO criado e `psql` conectado a `second_brain_preservation` como `second_brain_preserver`; conteúdo segredo proibido |
| Neon preservation | `crimson-salad-15823867`, branch `br-quiet-mode-b4rpmk9c`, banco `second_brain_preservation` | CONFIRMADO READY e `psql` SELECT; não é banco ativo do Staging por definição |

## Ferramentas nativas / serviços Jacob
| Componente | Caminho/endereço | Estado |
|---|---|---|
| Home/Developer 8803 | `D:\JacobOS2\supreme-s0\frontend`; local 8803 | CONFIRMADO histórico; Home congelada |
| S0 8787 | `D:\JacobOS2\s0-local\app\src\main.js`; local 8787 | CONFIRMADO histórico |
| Bus/Agent Mesh 8788 | local 8788, tarefa Windows `\\JacobOS2\\Bus-Agent` | HISTÓRICO; ACK/live workers PENDENTE |
| JEV / roteador | Projeto `D:\JacobOS2`, contratos da cognição e workers | HISTÓRICO; presença e provider real PENDENTE |
| Release Dispatch | `D:\JacobOS2\canonical-governance\deploy-center\release-dispatch.mjs` | CONFIRMADO arquivo em diagnóstico; funcionamento fim a fim PENDENTE |
| Publicador PowerShell | `...\deploy-center\jacob-deploy.ps1` | CONFIRMADO arquivo; publicação real não provada |
| Restore local | `D:\JacobOS2\canonical-governance\restore-points\RP-8787-8803-20261017T171841Z` | CONFIRMADO hashes; restore efetivo pendente |
| Super Agentes VNext Local/Cloud | governança Agent Mesh e painéis Developer | HISTÓRICO; processos/identidades e heartbeats reais PENDENTE |
| BrowserArm/Jacob Live Web Research | nativo planejado e fragmentos de código | HISTÓRICO; runtime real PENDENTE |
| JARVIS/Ultron esfera e voz | Home congelada, voz premium e regras dinâmicas planejadas | HISTÓRICO; provider de voz e serviço atuais PENDENTE |
| WhatsApp Evolution | Render `jacob-evolution-staging-r165` e canary, integrações locais | CONFIRMADO existência Render; sessão/autorização WhatsApp vigente PENDENTE |
| Segundo cérebro e NekoCore | Render `jacob-second-brain-staging`, `jacob-nekocore-staging` | CONFIRMADO existência Render; DB/origem real PENDENTE |
| Cloud Agents | Render `jacob-cloud-lanes-staging`, `jacob-autonomy-worker-staging`, `jacob-sovereign-brain-staging` | CONFIRMADO serviços; workers ativos e ACK PENDENTE |

## Serviços e aplicativos externos integrados ou pretendidos
Classifique individualmente **CONETADO A ESTE CHATGPT** versus **INTEGRADO AO JACOB**. Uma conexão neste chat não prova conexão de runtime do Jacob.

| Serviço | Finalidade | Evidência atual |
|---|---|---|
| GitHub | Repos, PRs, Actions, código | CONFIRMADO ChatGPT/Windows; Jacob runtime PENDENTE |
| Render | Hosts de backend e workers | CONFIRMADO ChatGPT/Windows; Jacob runtime PENDENTE |
| Neon | DB, MCP, branches e Skills | CONFIRMADO ChatGPT/Windows; consumer app PENDENTE |
| Cloudflare | DNS, proxy, frontdoor, Pages | CONFIRMADO DNS/Wrangler; projetos Pages e Worker PENDENTE |
| Google Cloud | Projeto staging, IAP e VM | CONFIRMADO CLI; recursos completos PENDENTE |
| Gmail, Google Calendar, Contacts, Drive | Mensagens, eventos, contatos, knowledge/backup | Conectores disponíveis neste ChatGPT; runtime Jacob NÃO COMPROVADO |
| Slack, GitHub, Zoom | Comunicação/trabalho | Conectores disponíveis neste ChatGPT; runtime Jacob NÃO COMPROVADO |
| Stripe, Mercado Pago | Cobrança e links de pagamento | Stripe conector disponível; Mercado Pago plano histórico MSA, conexão real PENDENTE |
| Instagram / Meta | Agentes Digital Multiverso, Jacob OS, Jasmin | Missões históricas; autorização Meta/API, webhook e atendimento fim a fim PENDENTE |
| Evolution API / WhatsApp | Mensagens, mídia, grupos | Serviços Render encontrados; instâncias efetivas e sessão PENDENTE |
| OpenAI, DeepSeek, Groq, Claude | Modelos de linguagem e voz | Provedores em planejamento/contratos; chaves ativas por ambiente PENDENTE — apenas nome de variável |
| Codex e Claude Code | Executores externos | Codex registrado Neon MCP, Claude histórico; cotas indisponíveis temporariamente conforme Founder |
| Remote Desktop Commander / TinyFish | Acesso remoto/navegador | Conectores disponíveis neste ChatGPT; cotas não disponíveis segundo Founder, não depender |
| Multiverso Social Agents | Produto `multiversoagents.jacobos.com.br` planejado | Front/back/DB e publicar real PENDENTE |
| Férias com Propósito | Produto independente | Domínio/repo/serviço/banco PENDENTE; não assumir jacob-family-api |
| Jacob Jobs | Repo `jasonfrancamusic/jacob-jobs`, site `jobs.jacobos.com.br` planejado | Host/DB e publicação PENDENTE |

## Neon IA — aplicações úteis ao Jacob
A documentação oficial `https://neon.com/docs/ai/ai-agents-tools` oferece MCP, agent skills, integração editor/CLI, versionamento de banco e Neon API para agentes. O benefício imediato é rastrear o DB efetivamente usado por cada serviço, ramificar um DB certo antes de publicar, diagnosticar SQL via skill e manter o catálogo atualizado. Nenhuma dessas tecnologias substitui mapear env vars por serviço nem valida automaticamente restore. **Não executar `npx neon init` indiscriminadamente**: pode criar API key/config novos quando a CLI já está autenticada; preservar contexto atual.

## Processo de atualização
1. **Descobrir:** varrer ferramentas PATH, executáveis conhecidos, roots de skills e arquivos de configuração (somente nomes, existência e hash de arquivos públicos; não conteúdo de segredos).
2. **Identificar:** associação ambiente -> app -> frontend -> backend -> tool/provider -> repo/branch -> banco -> release/restore. Ambientes separados Local, Staging, Produção e produtos independentes.
3. **Verificar:** comandos read-only e HTTP não autenticados quando fizer sentido; registrar timestamp e resposta reduzida, sem tokens.
4. **Congelar:** gravar recibos locais JSON e sincronizar docs no GitHub por caminho conhecido. Nunca dar `git reset`, limpar worktrees, sobrescrever `.env`, `pgpass.conf`, `.neon`, `.mcp.json`, config de Codex/Claude, nem mudar Home.
5. **Operar:** para PUBLICAR, usar catálogo para escolher serviço real; um restore point validado antes de deploy; verificar versão servida e registrar novo recibo.

## Missões P0
- Atualizar inventário de ferramentas mensalmente e após qualquer instalação/autenticação/deploy, com timestamp (não criar automação sem instrução específica).
- Resolver mapeamento Cloudflare Pages/Workers do frontend e origens Produção, MSA, Férias e Jobs.
- Descobrir **apenas o nome e presença** de `DATABASE_URL`, `POSTGRES_URL` e correlatas no serviço exato Render `srv-d9bh207avr4c73aluds0`, sem exportar secret.
- Criar restore point no banco realmente ligado ao Staging e identificar rollback real de frontend/backend.
