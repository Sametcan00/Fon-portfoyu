/* Fon Portföyüm — çevrimdışı çalışma.
   Uygulama dosyaları ilk açılışta iPhone'a kaydedilir; sonraki açılışlar internet olmadan da çalışır.
   Yeni sürüm yayınladığınızda aşağıdaki VERSION değerini artırın. */
const VERSION = '1.9.19';
const CACHE = 'fon-portfoyu-' + VERSION;
const FILES = [
  './',
  './index.html',
  './manifest.webmanifest',
  './icons/apple-touch-icon.png',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/icon-maskable-512.png'
];

self.addEventListener('install', (e) => {
  // cache:'reload' → tarayıcının HTTP önbelleği atlanır (GitHub Pages dosyaları 10 dk önbellekli gönderir; yoksa yeni sürüm eski sayfayla kurulabiliyordu)
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(FILES.map((u) => new Request(u, { cache: 'reload' })))).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k.startsWith('fon-portfoyu-') && k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

// Önce cihazdaki kopyayı hemen göster (hızlı açılış), arka planda internetten güncelle.
self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== self.location.origin) return;
  // Enflasyon verisi: önce internetten (yeni ay açıklanmış olabilir), internet yoksa cihazdaki kopya
  if (new URL(req.url).pathname.endsWith('/tufe.json')) {
    // Sunucu hata dönerse (502/404 gibi) de cihazdaki kopya kullanılır; önbelleğe yazma bitene kadar service worker uyumaz
    e.respondWith(
      caches.open(CACHE).then((cache) =>
        fetch(req).then((res) => {
          if (res && res.ok) { e.waitUntil(cache.put('./tufe.json', res.clone())); return res; }
          return cache.match('./tufe.json').then((c) => c || res);
        }).catch(() => cache.match('./tufe.json').then((c) => c || Response.error()))
      )
    );
    return;
  }
  const key = req.mode === 'navigate' ? './index.html' : req;
  e.respondWith(
    caches.open(CACHE).then(async (cache) => {
      const cached = await cache.match(key, { ignoreSearch: true });
      // arka plan güncellemesi her seferinde sunucuya sorar (no-cache: değişmediyse 304, ucuz)
      const fresh = fetch(req, { cache: 'no-cache' }).then((res) => {
        if (res && res.ok) cache.put(key, res.clone());
        return res;
      }).catch(() => null);
      if (cached) { e.waitUntil(fresh); return cached; }
      return (await fresh) || new Response('Çevrimdışı', { status: 503, headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
    })
  );
});
