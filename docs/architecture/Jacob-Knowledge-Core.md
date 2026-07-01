# Jacob Knowledge Core

## Strategic Decision

Jacob should not begin by training a large language model from zero.

Jacob should begin with a proprietary knowledge system that grows through use.

This is cheaper, safer and more aligned with the product vision.

## What We Are Building

Jacob Knowledge Core is the layer responsible for separating:

1. General knowledge learned from public sources.
2. Private partner memory owned by each user.
3. Temporary conversation context.
4. Verified summaries and reusable insights.

## Core Principle

Public knowledge can be shared across the Jacob ecosystem.

Private partner data must remain isolated.

A partner's personal memory never becomes general knowledge.

## Architecture

```text
Jacob Brain
   |
   |-- Private Memory Store
   |     - partner goals
   |     - personal preferences
   |     - projects
   |     - sensitive life data
   |
   |-- General Knowledge Store
   |     - public summaries
   |     - reusable concepts
   |     - verified facts
   |     - domain knowledge
   |
   |-- Research Engine
   |     - search
   |     - extract
   |     - summarize
   |     - verify
   |     - store
   |
   |-- Answer Engine
         - retrieve
         - reason
         - respond
```

## This Is Not Yet a Foundation Model

A foundation model predicts language from billions of examples.

Jacob Knowledge Core retrieves, organizes and reuses knowledge.

This is closer to a proprietary RAG system, knowledge graph and memory engine.

Over time, this can generate training data for future fine-tuning or a smaller local model.

## Learning Flow

1. Partner asks a question.
2. Jacob checks private memory.
3. Jacob checks general knowledge.
4. If knowledge is missing, Jacob researches.
5. Jacob summarizes the result.
6. Jacob stores reusable public learning in General Knowledge.
7. Jacob stores personal context only in Private Memory, with consent.
8. Jacob answers with sources and uncertainty when needed.

## Privacy Rule

Never mix private partner data into the general knowledge base.

Example:

- General knowledge: "Compound interest grows capital exponentially over time."
- Private memory: "Jason invests R$ 500 per month."

The first can be general.
The second belongs only to Jason.

## Cost Strategy

This approach avoids the cost of training a large model.

It still requires development time, but not millions of dollars.

The first version can be implemented with:

- local JSON or SQLite;
- simple search;
- manual or automated summarization;
- optional LLM support;
- future vector database;
- future local embedding model.

## Future Evolution

Phase 1: Local knowledge store.

Phase 2: Source-aware research engine.

Phase 3: Semantic search with embeddings.

Phase 4: Knowledge graph.

Phase 5: Fine-tuning dataset generated from verified Jacob usage.

Phase 6: Small local Jacob model for offline reasoning.

Phase 7: Hybrid Jacob model plus external LLM fallback.

## Strategic Position

Jacob's moat is not training a huge model first.

Jacob's moat is building a trusted personal operating system with memory, planning, knowledge and presence.

The model can evolve later.

The relationship, memory and knowledge architecture must start now.
