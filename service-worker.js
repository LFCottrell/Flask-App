const cacheName = 'your-app-cache-v1';
const filesToCache = [
  '/',
  '/static/styles.css',  // Update with your actual stylesheet path
  '/static/icon.jpg'    // Update with your actual icon path
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(cacheName).then((cache) => {
      return cache.addAll(filesToCache);
    })
  );
});

self.addEventListener('fetch', (e) => {
  e.respondWith(
    caches.match(e.request).then((response) => {
      return response || fetch(e.request);
    })
  );
});
