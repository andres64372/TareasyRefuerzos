;
//asignar un nombre y versión al cache
const CACHE_NAME = 'v1.8_cache_tareas_refuerzos',
  urlsToCache = [
    "/",
    "/trabajos",
    "/examenes",
    "/clases",
    "/static/icon-192x192.png",
    "/static/icon-256x256.png",
    "/static/icon-384x384.png",
    "/static/icon-512x512.png",
    "/static/icon.png",
    "/static/logo1.png",
    "/static/logo2.png",
    "/static/logo3.png",
    "/static/facebook.png",
    "/static/instagram.png",
    "/static/youtube.png",
    "/static/qr.jpeg"
  ]

//durante la fase de instalación, generalmente se almacena en caché los activos estáticos
self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache)
          .then(() => self.skipWaiting())
      })
      .catch(err => console.log('Falló registro de cache', err))
  )
})

//una vez que se instala el SW, se activa y busca los recursos para hacer que funcione sin conexión
self.addEventListener('activate', e => {
  const cacheWhitelist = [CACHE_NAME]

  e.waitUntil(
    caches.keys()
      .then(cacheNames => {
        return Promise.all(
          cacheNames.map(cacheName => {
            //Eliminamos lo que ya no se necesita en cache
            if (cacheWhitelist.indexOf(cacheName) === -1) {
              return caches.delete(cacheName)
            }
          })
        )
      })
      // Le indica al SW activar el cache actual
      .then(() => self.clients.claim())
  )
})

//cuando el navegador recupera una url
self.addEventListener('fetch', e => {
  //Responder ya sea con el objeto en caché o continuar y buscar la url real
  e.respondWith(
    caches.match(e.request)
      .then(res => {
        if (res) {
          //recuperar del cache
          return res
        }
        //recuperar de la petición a la url
        return fetch(e.request)
      })
  )
})