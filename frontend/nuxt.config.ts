export default defineNuxtConfig({
    compatibilityDate: '2025-07-15',
    devtools: { enabled: true },
    modules: ['@pinia/nuxt', '@nuxt/fonts'],
    css: [
        '~/assets/css/main.css'
    ],
    fonts: {
        families: [
            {
                name: 'Roboto',
                provider: 'google',
            }
        ]
    },
})
