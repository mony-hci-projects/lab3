<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
</script>

<template>
  <header>
    <h1>Image Search Engine Demo</h1>
    <img
      alt="logo"
      class="logo"
      src="@/assets/tju.ico"
      width="32"
      height="32"
    />
    <nav>
      <RouterLink to="/">搜索</RouterLink>
      <RouterLink to="/favorite">收藏</RouterLink>
    </nav>
  </header>

  <RouterView />
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
  margin-top: 1rem;
}

.logo {
  display: block;
  margin: 1rem auto 1rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
  margin-bottom: 3rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}
</style>
