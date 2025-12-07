<template>
  <div class="p-8 max-w-md mx-auto">
    <h1 class="text-2xl mb-4">Login</h1>

    <form @submit.prevent="submit">
      <input
        v-model="username"
        placeholder="Username"
        class="border p-2 w-full mb-3"
      />
      <input
        v-model="password"
        type="password"
        placeholder="Password"
        class="border p-2 w-full mb-3"
      />

      <button class="bg-blue-600 text-white px-4 py-2 rounded">
        Login
      </button>

      <p v-if="error" class="text-red-500 mt-3">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { useAuth } from '~/stores/auth'

const auth = useAuth()

const username = ref("")
const password = ref("")
const error = ref("")

const submit = async () => {
  const success = await auth.login(username.value, password.value)

  if (success) {
    return navigateTo('/')
  }

  error.value = "Invalid username or password"
}
</script>