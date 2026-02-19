<template>
  <v-app>
    <v-app-bar flat border="b">
      <v-app-bar-title>Life Dashboard</v-app-bar-title>
    </v-app-bar>

    <v-main>
      <Dashboard />
    </v-main>
  </v-app>
</template>

<script setup>
import Dashboard from '@/views/Dashboard.vue'
</script>
