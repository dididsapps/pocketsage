// Cloudflare Pages — blocage géographique (lu automatiquement par Cloudflare Pages)
// PocketSage n'est pas proposé dans les pays dont la réglementation impose de stocker
// les données sur place (Chine continentale, Russie). Le blocage se fait selon le pays
// de CONNEXION : les russophones / sinophones vivant ailleurs gardent l'accès normal.
// Pour modifier la liste : codes pays ISO à 2 lettres ci-dessous.
const BLOCKED = new Set(["CN", "RU"]);

const PAGE = `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>PocketSage</title><style>body{font-family:system-ui,sans-serif;background:#F6F8FC;color:#1B2333;display:flex;min-height:100vh;align-items:center;justify-content:center;margin:0;padding:16px}
.c{max-width:420px;background:#fff;border-radius:18px;padding:28px 24px;box-shadow:0 6px 24px rgba(0,0,0,.08);text-align:center;line-height:1.5}
p{margin:.6em 0}small{color:#777}</style></head><body><div class="c"><div style="font-size:40px">🎓</div><h1 style="font-size:20px">PocketSage Academy</h1>
<p>PocketSage n'est pas disponible dans votre pays.</p>
<p>PocketSage is not available in your country.</p>
<p>PocketSage недоступен в вашей стране.</p>
<p>PocketSage 在您所在的国家/地区不可用。</p>
<small>contact@pocketsage.org</small></div></body></html>`;

export async function onRequest(context) {
  const country = context.request.cf && context.request.cf.country;
  if (country && BLOCKED.has(country)) {
    return new Response(PAGE, {
      status: 451,
      headers: { "content-type": "text/html; charset=utf-8", "cache-control": "no-store" },
    });
  }
  return context.next();
}
