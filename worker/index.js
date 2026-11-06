// PocketSage — proxy ElevenLabs (Cloudflare Worker)
// La clé ElevenLabs reste ICI (secret Cloudflare), jamais dans la page publique.
// Protections : origine autorisée, texte limité, voix/modèle fixés côté serveur,
// limite d'appels par adresse IP.

const ALLOWED_ORIGINS = [
  "https://pocketsage.org",
  "https://www.pocketsage.org",
];
const MAX_CHARS = 3000; // un morceau de l'onglet Nuit fait ~350 mots max

function corsHeaders(origin) {
  return {
    "Access-Control-Allow-Origin": origin,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400",
    "Vary": "Origin",
  };
}

function reply(status, message, origin) {
  return new Response(JSON.stringify({ error: message }), {
    status,
    headers: { "Content-Type": "application/json", ...(origin ? corsHeaders(origin) : {}) },
  });
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";
    if (!ALLOWED_ORIGINS.includes(origin)) return reply(403, "origine refusée", null);

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: corsHeaders(origin) });
    }
    if (request.method !== "POST") return reply(405, "méthode refusée", origin);

    // Limite d'appels par IP (voir wrangler.toml)
    if (env.RATE_LIMITER) {
      const ip = request.headers.get("CF-Connecting-IP") || "inconnue";
      const { success } = await env.RATE_LIMITER.limit({ key: ip });
      if (!success) return reply(429, "trop de requêtes, réessaie dans une minute", origin);
    }

    let text;
    try {
      ({ text } = await request.json());
    } catch (e) {
      return reply(400, "requête invalide", origin);
    }
    if (typeof text !== "string" || !text.trim()) return reply(400, "texte manquant", origin);
    if (text.length > MAX_CHARS) return reply(413, "texte trop long", origin);

    const upstream = await fetch(
      `https://api.elevenlabs.io/v1/text-to-speech/${env.VOICE_ID}`,
      {
        method: "POST",
        headers: { "xi-api-key": env.ELEVEN_API_KEY, "Content-Type": "application/json" },
        body: JSON.stringify({
          text,
          model_id: env.MODEL_ID,
          voice_settings: { stability: 0.45, similarity_boost: 0.75, style: 0.25, use_speaker_boost: true },
        }),
      }
    );

    if (!upstream.ok) return reply(502, "service voix indisponible", origin);

    return new Response(upstream.body, {
      status: 200,
      headers: { "Content-Type": "audio/mpeg", "Cache-Control": "no-store", ...corsHeaders(origin) },
    });
  },
};
