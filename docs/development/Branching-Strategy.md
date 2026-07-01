# Branching Strategy — Jacob OS

## Branches

- `main`: versão estável e testável.
- `develop`: integração das próximas entregas.
- `feature/<nome>`: novas funcionalidades.
- `fix/<nome>`: correções específicas.
- `docs/<nome>`: documentação.

## Fluxo recomendado

1. Criar branch a partir de `develop`.
2. Implementar mudanças pequenas e coerentes.
3. Rodar testes e abrir revisão.
4. Integrar em `develop`.
5. Promover para `main` quando a sprint estiver estável.

## Regra de segurança

Nunca trabalhar diretamente na `main` quando o Codex estiver executando tarefas maiores.
