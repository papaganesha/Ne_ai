# NE‑AI V1 — Inteligência Multimodal Local

Este documento é **README + Documentação Técnica** do projeto **NE‑AI V1**.
Tudo aqui corresponde exatamente ao que foi construído passo a passo.

---

## 🎯 O QUE É O NE‑AI

NE‑AI é um **agente cognitivo local**, escrito em **Python**, capaz de:

* Perceber o mundo (tela, vídeo, texto, OCR)
* Filtrar informação irrelevante
* Avaliar confiança
* Perguntar quando não tem certeza
* Aprender incrementalmente
* Manter memória vetorial
* Tomar decisões
* Gerar intenções de ação

⚠️ Automação real **não é executada** na V1 — apenas preparada.

---

## 🧠 PRINCÍPIO FUNDAMENTAL

> **Extrair ≠ Aprender ≠ Agir**

Cada etapa é isolada, observável e controlável.

---

## 🧱 ARQUITETURA GERAL

```
Percepção → Cognição → Decisão → Intenção → (Ação futura)
```

Nada pula etapas.

---

## 📁 ESTRUTURA FINAL DO PROJETO

```
ne_ai/
│
├── main.py
│
├── core/
│   ├── orchestrator.py
│   ├── scheduler.py
│   └── config.py
│
├── inputs/
│   ├── screen_stream.py
│   ├── video_stream.py
│   ├── upload_handler.py
│   └── text_input.py
│
├── perception/
│   ├── frame_filter.py
│   ├── ocr.py
│   └── text_normalizer.py
│
├── cognition/
│   ├── relevance.py
│   ├── confidence.py
│   ├── questioner.py
│   └── learner.py
│
├── memory/
│   ├── vectorizer.py
│   ├── similarity.py
│   ├── history.py
│   └── store.py
│
├── agent/
│   ├── decision.py
│   ├── intent.py
│   ├── policy.py
│   └── executor.py
│
├── api/
│   └── web_server.py
│
├── web/
│   ├── templates/index.html
│   └── static/app.js
│
└── storage/
    ├── raw/
    ├── processed/
    └── memory.json
```

---

## ▶️ FLUXO COMPLETO DO SISTEMA

### 1️⃣ Inicialização

* `main.py` carrega tudo
* Orquestrador sobe
* Web UI inicia
* Threads ficam prontas

### 2️⃣ Entrada de Dados

Fontes possíveis (paralelas):

* Tela (stream)
* Vídeo
* Upload manual
* Texto

### 3️⃣ Percepção

* Filtro de frames
* OCR
* Normalização

### 4️⃣ Cognição

* Relevância
* Confiança
* Pergunta se necessário
* Aprendizado

### 5️⃣ Memória

* Vetores
* Similaridade
* Reforço
* Histórico

### 6️⃣ Decisão

* Geração de intenção
* Nenhuma ação executada

---

## 🧠 MODELO COGNITIVO

Cada conhecimento salvo contém:

```json
{
  "id": "uuid",
  "embedding": [...],
  "abstract": "conceito aprendido",
  "confidence": 0.87,
  "times_seen": 4,
  "history": []
}
```

---

## 🌐 INTERFACE WEB

A Web UI permite:

* Upload de dados
* Ver memória
* Ver perguntas
* Responder dúvidas
* Monitorar intenções

Tudo local.

---

## 🛡️ SEGURANÇA

* Automação desligada por padrão
* Intenções não executam ações
* Política central controla permissões

---

## 🚀 COMO RODAR

```bash
pip install fastapi uvicorn numpy opencv-python pytesseract
python main.py
```

Acesse:

```
http://127.0.0.1:8000
```

---

## 🔌 COMO EVOLUIR

### Automação

* Implementar `executor.py`
* Habilitar `policy.py`

### Inteligência

* Trocar embeddings
* Melhorar confiança

### Interface

* React / Vue
* Visualização de frames

---

## ✅ STATUS FINAL

✔ Multimodal
✔ Aprendizado incremental
✔ Memória vetorial
✔ Agente cognitivo
✔ Pronto para automação

---

## 🧠 FILOSOFIA DO PROJETO

> Não fazer rápido.
> Fazer **certo**.
> Evoluir sem quebrar.

---

FIM DA DOCUMENTAÇÃO V1
