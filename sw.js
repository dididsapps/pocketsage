// PocketSage Academy — Service Worker v2
const CACHE = 'pocketsage-v9';
const ASSETS = [
  '/',
  '/index.html',
  '/js/jeux.js',
  '/css/jeux.css',
  '/js/jeux-cerveau.js',
  '/manifest.json'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  // Audio files: network first, cache fallback
  if (e.request.url.includes('/audio/') || e.request.url.includes('/data/')) {
    // Network first ; les fichiers data/ (ex. data/flash/*.json) sont gardés en cache
    // pour fonctionner hors-ligne après la première ouverture.
    e.respondWith(
      fetch(e.request).then(res => {
        if (res && res.status === 200 && e.request.url.includes('/data/') && e.request.method === 'GET') {
          const clone = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone));
        }
        return res;
      }).catch(() => caches.match(e.request))
    );
    return;
  }
  // Everything else: cache first
  e.respondWith(
    caches.match(e.request).then(cached => {
      if (cached) return cached;
      return fetch(e.request).then(res => {
        if (!res || res.status !== 200 || res.type === 'opaque') return res;
        const clone = res.clone();
        caches.open(CACHE).then(c => c.put(e.request, clone));
        return res;
      });
    })
  );
});
