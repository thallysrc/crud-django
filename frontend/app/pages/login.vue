<template>
  <div class="login-container">
    <div class="">

      <h1 class="">Bem vindo</h1>

      <form @submit.prevent="submit">
        <input
          v-model="username"
          placeholder="Usuário"
          class=""
        />
        <input
          v-model="password"
          type="password"
          placeholder="Senha"
          class=""
        />

        <button class="">
          Login
        </button>

        <p v-if="error" class="">{{ error }}</p>
      </form>
        
    </div>
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

<style scoped>
 body {
    min-height: 100vh; 
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0;
    padding: 0;
    background-color: #f4f7f6;
} 
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
  height: 100vh;
  background-color: #f5f5f5;
}
</style>