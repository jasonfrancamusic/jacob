# Contrato transversal — PUBLICAR / RESTAURAR (Founder)
Data: 2026-10-17
Escopo: Jacob OS 2 local e cloud, Jacob Staging, Jacob Produção, Multiverso Social Agents, Férias com Propósito, Jacob Jobs, demais ferramentas próprias. Backend, frontend, serviços e agentes.

## Regra operacional
Uma ordem inequívoca "publicar [projeto] [ambiente]" ou um botão PUBLICAR executa o deploy solicitado. O usuário não faz pré-flight, checklist, aprovação recorrente, seleção de executor, conferência de log ou rollback manual. O Jacob resolve isso autonomamente por trás da interface.
Fluxo: (1) registrar um ponto de restauração efetivamente recuperável da versão anterior, (2) publicar release desejada, (3) confirmar versão/serving, (4) oferecer RESTAURAR com uma ação quando necessário.
Não criar burocracia de UI. Informar bloqueio técnico real resumidamente e prosseguir com tarefas independentes.

## Alcance e sincronização
Tratar este arquivo como contrato-espelho de governança de cada repositório. O canônico central fica em jacob-os2-sovereign. Sincronizar por Git e pelas rotas operacionais válidas, sem presumir que repositórios representam estados locais ainda não commitados ou contratos guardados fora deles.
Render, GCP, Cloudflare, Neon/PostgreSQL e outros provedores não são repositórios documentais por padrão. Aplicar política ao código/configuração de deploy dos produtos, e não executar comandos SQL indiscriminados nos bancos.
Executores permitidos pela ordem do Founder: ChatGPT, Codex e Claude integrados aos agentes internos Jacob; identidades técnicas e autorização por ambiente se resolvem nos bastidores, sem perguntas repetidas.
Preservar Home aprovada, dados e worktrees. Publicação em Produção somente quando o destino Produção foi ordenado; nenhum bypass de identidade da plataforma, credencial inexistente ou integridade dos arquivos.
Não depender de Remote Desktop Commander ou TinyFish.

## Evidência obrigatória automatizada
Ponto de restauração identificador, ambiente correto, SHA candidato, resultado do deploy, SHA servido, endereço e instrução automática RESTAURAR. Não chamar sucesso se falhar.
Ponto de referência local 2026-10-17: RP-8787-8803-20261017T171841Z; manifesto 372/372 SHA válido conforme execução encaminhada, teste independente ainda pendente.
Render conectado: workspace tea-d95g75vaqgkc73f375k0, serviços existentes do legado jacob-os; Cloud Lanes deploy histórico live, mas JACOB_CLEANROOM_READY=false registrado em 15/10; não redeployar commit antigo cegamente.
Status: CONTRATO REGISTRADO. Implementação funcional de botão único e publicação em nuvem NÃO certificada pela criação deste arquivo.
