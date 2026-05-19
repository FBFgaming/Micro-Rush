# Research Report: RES-002 — Framework Analysis

**Date**: 2024-05-19
**Analyst**: AGENT-RESEARCHER
**Status**: COMPLETE

---

## Executive Summary

Evaluated vector databases for the Archival Memory layer. **LanceDB** is recommended for Micro Rush due to its embedded design, Python-native API, and zero-config deployment. SQLite remains the best choice for Recall (SQL) memory.

---

## Vector Database Comparison

| Criteria | LanceDB | Pinecone | Chroma | Qdrant | Weaviate |
|----------|---------|---------|--------|--------|---------|
| **Deployment** | Embedded | Managed | Embedded | Server | Server |
| **Setup** | Zero-config | API key needed | Simple | Docker | Docker |
| **Language** | Python | Any | Python | Any | Any |
| **Scalability** | Single-node | Unlimited | Single-node | Distributed | Distributed |
| **Cost** | Free (local) | $70+/mo managed | Free | Self-hosted | Self-hosted |
| **License** | Apache 2.0 | Proprietary | Apache 2.0 | Apache 2.0 | BSD |

---

## Detailed Analysis

### LanceDB ✅ RECOMMENDED

**Pros:**
- Embedded (no server needed)
- Zero-config, just `pip install`
- Apache 2.0 license
- Excellent for single-user local apps
- Direct Python integration
- Active development

**Cons:**
- Single-node only (fine for personal use)
- Ecosystem still maturing

**Verdict:** Perfect for Micro Rush. Local, free, simple.

### Pinecone ❌

**Pros:**
- Production-grade, highly scalable
- Managed (no ops)

**Cons:**
- Cloud-only, defeats privacy purpose
- $70+/month minimum
- API key required

**Verdict:** Good for enterprise, wrong for us.

### Chroma ⚠️

**Pros:**
- Simple setup
- Python-native
- Good for development

**Cons:**
- Performance concerns at scale
- Limited querying capabilities
- Project velocity slowed

**Verdict:** Alternative if LanceDB has issues.

### Qdrant ✅

**Pros:**
- Self-hosted option
- Distributed architecture
- Strong filtering

**Cons:**
- Requires Docker/server
- More ops overhead

**Verdict:** Good for multi-user deployment later.

---

## SQL Database for Recall

| Database | Verdict | Notes |
|----------|---------|-------|
| **SQLite** | ✅ Use this | Zero-config, sufficient for single user |
| PostgreSQL | For later | If multi-user needed |

---

## Framework Architecture Decision

```
┌─────────────────────────────────────────────────────────┐
│                    Recall Memory                        │
│                    (SQLite)                              │
│                                                         │
│  • Hard facts & preferences                             │
│  • Exact key-value lookups                              │
│  • Categorized search                                   │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                   Archival Memory                       │
│                   (LanceDB)                             │
│                                                         │
│  • Vector embeddings for semantic search               │
│  • Conversation summaries                              │
│  • Conceptual history                                  │
└─────────────────────────────────────────────────────────┘
```

---

## Recommendations

1. **Use SQLite for Recall** — Simple, sufficient, zero-config
2. **Use LanceDB for Archival** — Embedded, fast, perfect for local
3. **Defer PostgreSQL decision** — Only if multi-user is needed

---

## Sources
- LanceDB documentation (https://lancedb.github.io/lancedb/)
- Pinecone pricing page
- Chroma GitHub repository
- Qdrant documentation