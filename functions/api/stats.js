// PocketSage — compteur ANONYME d'erreurs par question (Cloudflare Pages Function)
// Reçoit seulement : identifiant de question, nb de réponses, nb d'erreurs, et quelle
// mauvaise réponse (son numéro). Aucune donnée sur l'enfant, aucun identifiant d'appareil.
// Stockage : base D1 liée au projet Pages sous le nom STATS (sinon : rien n'est stocké).
// Lecture (pour analyse) : GET /api/stats?t=<STATS_TOKEN>[&min=20][&format=csv]
const ID = /^[A-Z]{2,4}-[A-Za-z0-9]{1,6}-\d{1,4}$/;
const TABLES = [
  "CREATE TABLE IF NOT EXISTS qstats (id TEXT PRIMARY KEY, n INTEGER NOT NULL DEFAULT 0, k INTEGER NOT NULL DEFAULT 0)",
  "CREATE TABLE IF NOT EXISTS qchoix (id TEXT NOT NULL, i INTEGER NOT NULL, c INTEGER NOT NULL DEFAULT 0, PRIMARY KEY (id, i))",
  "CREATE TABLE IF NOT EXISTS qavis (id TEXT NOT NULL, a TEXT NOT NULL, c INTEGER NOT NULL DEFAULT 0, PRIMARY KEY (id, a))",
];
const ok = (body = null, status = 204, type = "application/json") =>
  new Response(body, { status, headers: { "content-type": type, "cache-control": "no-store" } });

async function init(db) { await db.batch(TABLES.map((s) => db.prepare(s))); }

export async function onRequestPost({ request, env }) {
  const db = env.STATS;
  if (!db) return ok();
  let data;
  try {
    const txt = await request.text();
    if (txt.length > 20000) return ok(null, 413);
    data = JSON.parse(txt);
  } catch { return ok(null, 400); }
  const q = data && data.q;
  if (!q || typeof q !== "object") return ok(null, 400);
  const st = [];
  for (const [id, v] of Object.entries(q).slice(0, 80)) {
    if (!ID.test(id) || !Array.isArray(v)) continue;
    const n = Math.min(20, Math.max(0, v[0] | 0)), k = Math.min(n, Math.max(0, v[1] | 0));
    const av = v[3] && typeof v[3] === "object" ? v[3] : {};
    for (const a of ["f", "d", "p"]) {
      const c = Math.min(5, Math.max(0, av[a] | 0));
      if (c) st.push(db.prepare("INSERT INTO qavis (id,a,c) VALUES (?1,?2,?3) ON CONFLICT(id,a) DO UPDATE SET c=c+?3").bind(id, a, c));
    }
    if (!n) continue;
    st.push(db.prepare("INSERT INTO qstats (id,n,k) VALUES (?1,?2,?3) ON CONFLICT(id) DO UPDATE SET n=n+?2, k=k+?3").bind(id, n, k));
    const w = v[2] && typeof v[2] === "object" ? v[2] : {};
    for (const [i, c] of Object.entries(w).slice(0, 8)) {
      const ii = i | 0, cc = Math.min(20, Math.max(0, c | 0));
      if (ii < 0 || ii > 9 || !cc) continue;
      st.push(db.prepare("INSERT INTO qchoix (id,i,c) VALUES (?1,?2,?3) ON CONFLICT(id,i) DO UPDATE SET c=c+?3").bind(id, ii, cc));
    }
  }
  if (!st.length) return ok();
  try { await db.batch(st); }
  catch { await init(db); await db.batch(st); }
  return ok();
}

export async function onRequestGet({ request, env }) {
  const db = env.STATS;
  if (!db) return ok(JSON.stringify({ actif: false, info: "Base STATS non liée au projet Pages" }), 200);
  const u = new URL(request.url);
  if (!env.STATS_TOKEN || u.searchParams.get("t") !== env.STATS_TOKEN) return ok(null, 403);
  const min = Math.max(1, parseInt(u.searchParams.get("min") || "1", 10));
  await init(db);
  const { results: qs } = await db.prepare("SELECT id,n,k FROM qstats WHERE n>=?1 ORDER BY (k*1.0/n) DESC, n DESC LIMIT 5000").bind(min).all();
  const { results: ch } = await db.prepare("SELECT id,i,c FROM qchoix").all();
  const { results: av } = await db.prepare("SELECT id,a,c FROM qavis").all();
  const w = {}, A = {};
  for (const r of ch) (w[r.id] = w[r.id] || {})[r.i] = r.c;
  for (const r of av) (A[r.id] = A[r.id] || { f: 0, d: 0, p: 0 })[r.a] = r.c;
  if (u.searchParams.get("format") === "csv") {
    const lines = ["id,reponses,erreurs,taux_erreur,mauvaises_reponses(numero:nb),avis_trop_facile,avis_trop_dure,avis_pas_claire"];
    for (const r of qs) { const a = A[r.id] || { f: 0, d: 0, p: 0 };
      lines.push(`${r.id},${r.n},${r.k},${(r.k / r.n).toFixed(2)},"${Object.entries(w[r.id] || {}).map(([i, c]) => i + ":" + c).join(" ")}",${a.f},${a.d},${a.p}`); }
    return ok(lines.join("\n"), 200, "text/csv; charset=utf-8");
  }
  return ok(JSON.stringify({ actif: true, questions: qs.map((r) => ({ ...r, taux: +(r.k / r.n).toFixed(3), mauvaises: w[r.id] || {}, avis: A[r.id] || { f: 0, d: 0, p: 0 } })) }), 200);
}
