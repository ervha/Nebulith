// Nebulith Studio Web - Complete Offline Service Worker (v2.8)
const CACHE_NAME = 'nebulith-studio-5f30be3e143768939128';
const PRECACHE_ASSETS = [
  './',
  './index.html',
  './standalone.html',
  './data.js',
  './library.html',
  './bidirectional.js',
  './incremental.js',
  './workspace.js',
  './app.js',
  './manifest.json',
  './icon.svg',
  './favicon.svg'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(PRECACHE_ASSETS);
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key.startsWith('nebulith-studio-') && key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  // Only handle GET requests
  if (event.request.method !== 'GET') return;
  if (!event.request.url.startsWith(self.registration.scope)) return;

  event.respondWith(
    caches.open(CACHE_NAME).then(async (cache) => {
      const cachedResponse = await cache.match(event.request);
      if (cachedResponse) {
        // Return cached asset immediately
        return cachedResponse;
      }
      // If not in cache, fetch from network and dynamically cache
      return fetch(event.request).then((networkResponse) => {
        if (!networkResponse || networkResponse.status !== 200 || networkResponse.type !== 'basic') {
          return networkResponse;
        }
        const responseToCache = networkResponse.clone();
        event.waitUntil(cache.put(event.request, responseToCache));
        return networkResponse;
      }).catch(async () => {
        // Offline fallback to index.html or standalone.html
        if (event.request.mode === 'navigate') {
          const fallback = await cache.match('./index.html') || await cache.match('./standalone.html');
          if (fallback) return fallback;
        }
        return new Response('Offline asset unavailable', {status: 503});
      });
    })
  );
});

