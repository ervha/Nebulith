// Nebulith Studio Web - Complete Offline Service Worker (v2.8)
const CACHE_NAME = 'nebulith-studio-valnes-1';
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
          if (key !== CACHE_NAME) {
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

  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
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
        caches.open(CACHE_NAME).then((cache) => {
          cache.put(event.request, responseToCache);
        });
        return networkResponse;
      }).catch(() => {
        // Offline fallback to index.html or standalone.html
        if (event.request.mode === 'navigate') {
          return caches.match('./index.html') || caches.match('./standalone.html');
        }
      });
    })
  );
});
