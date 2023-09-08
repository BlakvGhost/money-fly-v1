const CACHE_NAME = 'BQ_CACHE';

const urlsToCache = [
  '/',
  '/static/css/style.css',
  '/static/vendor/vue/axios.min.js',
  '/static/js/service-worker.js',
  '/static/android-chrome-512x512.png',
  '/static/favicon.ico'
];

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.filter(function(cacheName) {
          return cacheName.startsWith(CACHE_NAME) && cacheName !== CACHE_NAME;
        }).map(function(cacheName) {
          return caches.delete(cacheName);
        })
      );
    })
  );
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        return response || fetch(event.request);
      })
      .catch(function() {
        return caches.match('/offline.html');
      })
  );
});
