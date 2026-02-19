<template>
  <v-container fluid class="pa-4">
    <v-row v-if="loading">
      <v-col cols="12" class="text-center">
        <v-progress-circular indeterminate />
      </v-col>
    </v-row>

    <v-row v-else-if="error">
      <v-col cols="12">
        <v-alert type="error">{{ error }}</v-alert>
      </v-col>
    </v-row>

    <v-row v-else>
      <!-- Weather cards -->
      <v-col
        v-for="w in weatherData"
        :key="w.location"
        cols="12"
        sm="6"
        lg="4"
      >
        <WeatherCard :weather="w" />
      </v-col>

      <!-- Add more card columns here as new widgets are built -->
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import WeatherCard from '@/components/WeatherCard.vue'
import { weatherApi } from '@/services/api.js'

const weatherData = ref([])
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const res = await weatherApi.getAll()
    weatherData.value = res.data
  } catch (e) {
    error.value = 'Could not load weather data.'
  } finally {
    loading.value = false
  }
})
</script>
