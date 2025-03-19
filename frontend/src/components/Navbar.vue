<template>
  <nav class="navbar">
    <router-link to="/">Notes</router-link>
    <router-link to="/create">Create Note</router-link>
    <router-link to="/analytics">Analytics</router-link>
  </nav>
</template>

<style>
.navbar {
  background: #222;
  padding: 20px 0;
  text-align: center;
}

.navbar a {
  color: cyan;
  margin: 0 20px;
  text-decoration: none;
  font-size: 20px;
}

.navbar a:hover {
  text-decoration: underline;
}
</style>
