export default defineNuxtRouteMiddleware(() => {
  const auth = useAuth()

  if (!auth.user) {
    return navigateTo('/login')
  }
})