<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
</script>

<template>
  <el-container>
    <el-header>
      <img
        alt="logo"
        class="logo"
        src="@/assets/tju.ico"
        width="32"
        height="32"
      />
      <h1>A Simple Image Search System</h1>
      <nav>
        <RouterLink to="/">简单搜索</RouterLink>
        <RouterLink to="/advance">高级搜索</RouterLink>
        <RouterLink to="/collection">收藏</RouterLink>
        <RouterLink to="/history">历史记录</RouterLink>
      </nav>
    </el-header>

    <el-main>
      <RouterView />
    </el-main>
  </el-container>
</template>

<style scoped>
header {
  width: 100%;
  height: auto;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  line-height: 1.5;
  max-height: 100vh;
  margin-top: 1rem;
  margin-bottom: 1rem;
}

.logo {
  /*display: block;*/
  margin: auto 1rem;
}

nav {
  width: 100%;
  font-size: 12px;
  margin-top: 1rem;
  margin-left: 3rem;
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

@media (min-width: 1024px) {
  main {
    margin: 2rem 2rem;
    width: 80%;
  }
}
</style>
