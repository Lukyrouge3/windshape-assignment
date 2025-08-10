import { defineNuxtConfig } from 'nuxt/config'

// Nuxt configuration
export default defineNuxtConfig({
  // Activer le rendu côté client uniquement
  ssr: false,
  modules: [
    '@nuxt/ui'
  ],
  app: {
    head: {
      title: 'Assignment Nuxt.JS / Flask ',
      meta: [
        { name: 'description', content: 'Application Nuxt/Three.js pour ajouter des objets 3D et synchroniser la scène via WebSocket.' }
      ]
    }
  }
})