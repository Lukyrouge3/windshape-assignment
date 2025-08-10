import { defineNuxtConfig } from 'nuxt/config'

// Nuxt configuration
export default defineNuxtConfig({
  ssr: false,
  modules: [
    '@nuxt/ui'
  ],
  app: {
    head: {
      title: 'Assignment Nuxt.JS / Flask ',
      meta: [
        { name: 'description', content: 'Application Nuxt/Three.js' }
      ]
    }
  }
})