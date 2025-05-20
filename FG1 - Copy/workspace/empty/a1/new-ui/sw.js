// Service Worker for Banking App
const CACHE_NAME = 'banking-app-v1';
const OFFLINE_URL = '/offline.html';
const ASSETS_TO_CACHE = [
  '/',
  '/index.html',
  '/login.html',
  '/account.html',
  '/services.html',
  '/css/bootstrap.min.css',
  '/css/style.css',
  '/css/responsive.css',
  '/js/jquery.min.js',
  '/js/popper.min.js',
  '/js/bootstrap.bundle.min.js',
  '/js/jquery-3.0.0.min.js',
  '/js/plugin.js',
  '/js/custom.js',
  '/js/molecule.js',
  '/js/auth.js',
  '/js/account.js',
  '/images/logo.png',
  '/offline.html',
  '/manifest.json'
];

// Install Event - Cache Assets
self.addEventListener('install', (event) => {
  console.log('[Service Worker] Installing Service Worker...');
  
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[Service Worker] Caching app shell and content...');
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
});

// Activate Event - Clean Up Old Caches
self.addEventListener('activate', (event) => {
  console.log('[Service Worker] Activating Service Worker...');
  
  event.waitUntil(
    caches.keys().then((keyList) => {
      return Promise.all(keyList.map((key) => {
        if (key !== CACHE_NAME) {
          console.log('[Service Worker] Removing old cache', key);
          return caches.delete(key);
        }
      }));
    })
  );
  
  return self.clients.claim();
});

// Fetch Event - Serve Cached Content When Offline
self.addEventListener('fetch', (event) => {
  const request = event.request;
  
  // Skip cross-origin requests
  if (!request.url.startsWith(self.location.origin)) {
    return;
  }
  
  // HTML navigation - Network first with offline fallback
  if (request.headers.get('Accept').includes('text/html')) {
    event.respondWith(
      fetch(request)
        .then((response) => {
          // Cache the new version
          const responseClone = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(request, responseClone);
          });
          return response;
        })
        .catch(() => {
          return caches.match(request)
            .then((response) => {
              // Return cached HTML or offline page
              return response || caches.match(OFFLINE_URL);
            });
        })
    );
    return;
  }
  
  // Other assets - Cache first with network fallback
  event.respondWith(
    caches.match(request)
      .then((response) => {
        // Return from cache if found
        if (response) {
          return response;
        }
        
        // Otherwise fetch from network
        return fetch(request)
          .then((networkResponse) => {
            // Cache new assets
            if (networkResponse && networkResponse.status === 200) {
              const responseToCache = networkResponse.clone();
              caches.open(CACHE_NAME).then((cache) => {
                cache.put(request, responseToCache);
              });
            }
            return networkResponse;
          });
      })
  );
});

// Handle online/offline events
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'ONLINE_STATUS') {
    // We could update UI or sync data based on online status
    console.log('[Service Worker] Online status changed:', event.data.online);
  }
});
