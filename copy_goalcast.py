"""
copy_goalcast.py — пакет копирайта футбольных брендов (GoalCast / fútbolplus)
============================================================================
Режим: email-capture (открыть мини-апп → оставить email). Mundial 2026.
Персона: Diego — футбольный аналитик. Тон: по делу, на данных, без хайпа.
Языки: EN / ES.

ВАЖНО:
  • Испанский — НЕЙТРАЛЬНЫЙ LATAM (tuteo: "deja", "toca", "recibe", "suscríbete"),
    а НЕ аргентинский voseo — чтобы одинаково читалось в MX/CO/PE/CL/AR и ES.
  • COMPLIANCE: 18+, только информационный анализ, БЕЗ обещаний результата/процентов.
"""

# ── /start HOOK (email-capture) ───────────────────────────────────────────────
HOOK_CAPTION = {
    "en": (
        "⚽ *World Cup 2026 analysis, straight to your inbox*\n\n"
        "I'm Diego, football analyst. Data, form, lineups and injuries — "
        "a clear read on every matchday of the World Cup.\n\n"
        "📊 Pre-match analysis backed by data\n"
        "⏱️ Scores and news in real time\n"
        "🎯 The analysis, delivered to your email\n\n"
        "Takes 10 seconds. 👇"
    ),
    "es": (
        "⚽ *Análisis del Mundial 2026, directo a tu correo*\n\n"
        "Soy Diego, analista de fútbol. Datos, forma, alineaciones y lesiones — "
        "un análisis claro de cada jornada del Mundial.\n\n"
        "📊 Previa de cada partido con datos\n"
        "⏱️ Resultados y novedades al instante\n"
        "🎯 El análisis, directo a tu correo\n\n"
        "Toma 10 segundos. 👇"
    ),
}

# Кнопка, открывающая мини-апп
OPEN_APP_BTN = {
    "en": "⚽ Get the analysis — free",
    "es": "⚽ Recibir el análisis — gratis",
}

# Юзер написал что-то вместо того чтобы открыть апп
NUDGE = {
    "en": (
        "👆 Tap the button above — leave your email and get the World Cup analysis.\n"
        "No spam, 18+, unsubscribe whenever you want."
    ),
    "es": (
        "👆 Toca el botón de arriba — deja tu correo y recibe el análisis del Mundial.\n"
        "Sin spam, 18+, te das de baja cuando quieras."
    ),
}

# Уже подписан
ALREADY_SUBSCRIBED = {
    "en": "✅ You're already in! Check your inbox — the next analysis is on its way. ⚽",
    "es": "✅ ¡Ya estás dentro! Revisa tu correo — el próximo análisis va en camino. ⚽",
}

GENERIC_FALLBACK = {
    "en": "⚽ Tap the button to get the analysis — 10 seconds, free, unsubscribe anytime.",
    "es": "⚽ Toca el botón para recibir el análisis — 10 segundos, gratis, te das de baja cuando quieras.",
}

# ── Repeat / retention nudges (используются retention_push.py) ────────────────
REPEAT_PUSH = {
    "en": [
        "⚽ The World Cup is around the corner. Get the data-backed analysis in your inbox — free. 👇",
        "📊 Lineups, form and injuries — the full read lands in your email. One tap to set it up. 👇",
        "⏱️ Last call before the next matchday — leave your email so you don't miss the analysis. 👇",
    ],
    "es": [
        "⚽ El Mundial está por arrancar. Recibe el análisis con datos en tu correo — gratis. 👇",
        "📊 Alineaciones, forma y lesiones — el análisis completo llega a tu correo. Un toque para activarlo. 👇",
        "⏱️ Última llamada antes de la próxima jornada — deja tu correo para no perderte el análisis. 👇",
    ],
}

# ── Warmup (нейтральный LATAM, без обещаний результата) ───────────────────────
WARMUP_FOOTBALL = {
    "en": [
        "⚽ Most people follow the team they love. I follow the data — form, head-to-head, fixture congestion.",
        "📊 Home/away splits move matches more than the table suggests. Tracking them well is half the read.",
        "💡 Midweek European nights wreck weekend form. Fatigue is the most underrated factor in football.",
    ],
    "es": [
        "⚽ La mayoría sigue al equipo que ama. Yo sigo los datos — forma, historial y carga de partidos.",
        "📊 El rendimiento local/visitante mueve partidos más de lo que dice la tabla. Seguirlo bien es la mitad del análisis.",
        "💡 Las noches europeas entre semana afectan la forma del fin de semana. El cansancio es el factor más subestimado.",
    ],
}
WARMUP_ESPORTS = WARMUP_FOOTBALL

# ── Bridge / CTA (email-режим) ────────────────────────────────────────────────
BRIDGE = HOOK_CAPTION  # в email-флоу отдельный bridge не нужен

CTA_REGISTER = {
    "en": "👇 Open the app, leave your email, and the World Cup analysis lands in your inbox. Free. ⚽",
    "es": "👇 Abre la app, deja tu correo y el análisis del Mundial llega a tu bandeja. Gratis. ⚽",
}

FTD_CELEBRATION = ALREADY_SUBSCRIBED

# ── Возражения (нейтральный LATAM) ────────────────────────────────────────────
BARRIER_FALLBACK = {
    "no_trust": {
        "en": "Fair. Open the app and see what the analysis looks like first — no commitment.",
        "es": "Es válido. Abre la app y mira primero cómo es el análisis — sin compromiso.",
    },
    "not_urgent": {
        "en": "No rush. Leaving your email takes 10 seconds whenever you're ready before the next matchday.",
        "es": "Sin apuro. Dejar tu correo toma 10 segundos cuando quieras, antes de la próxima jornada.",
    },
    "thinking": {
        "en": "Take your time. The World Cup analysis is free and lands straight in your inbox.",
        "es": "Tómate tu tiempo. El análisis del Mundial es gratis y llega directo a tu correo.",
    },
}

FTD_CONFIRM_PROMPT = {
    "en": "Left your email? Check your inbox — the first analysis is on its way. ⚽",
    "es": "¿Dejaste tu correo? Revisa tu bandeja — el primer análisis va en camino. ⚽",
}

MORNING_DIGEST_HEADER = {
    "en": "📅 *Good morning — today's fixtures*\n\n",
    "es": "📅 *Buenos días — los partidos de hoy*\n\n",
}
MORNING_DIGEST_FOOTER = {
    "en": "\n\n⚽ The full analysis is delivered by email.",
    "es": "\n\n⚽ El análisis completo se envía por correo.",
}

# ── Совместимость (channel-режим; в email-флоу не показываются) ────────────────
JOIN_PROMPT = {
    "en": "📣 Open the app and leave your email to get the World Cup analysis. Free, 18+.",
    "es": "📣 Abre la app y deja tu correo para recibir el análisis del Mundial. Gratis, 18+.",
}
JOIN_CHECK_BTN = {"en": "✅ Done", "es": "✅ Listo"}
JOIN_OK = {
    "en": "🔓 You're in — the analysis will land in your inbox. ⚽",
    "es": "🔓 Ya estás dentro — el análisis llegará a tu correo. ⚽",
}
JOIN_NOT_YET = {
    "en": "Hmm — I don't see your email yet. Open the app and leave it to get the analysis. ⚽",
    "es": "Mmm — todavía no veo tu correo. Abre la app y déjalo para recibir el análisis. ⚽",
}
