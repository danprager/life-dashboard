<template>
  <v-card class="weather-card" elevation="2">
    <v-card-title class="d-flex align-center justify-space-between">
      <span>{{ weather.location }}</span>
      <v-btn
        :icon="collapsed ? 'mdi-chevron-down' : 'mdi-chevron-up'"
        variant="text"
        size="small"
        @click="collapsed = !collapsed"
      />
    </v-card-title>

    <v-expand-transition>
      <v-card-text v-show="!collapsed">
        <div class="text-h3 mb-2">{{ weather.temperature }}°C</div>
        <div class="text-subtitle-1 mb-4">{{ weather.description }}</div>

        <v-row dense>
          <v-col cols="6">
            <v-icon size="small">mdi-water-percent</v-icon>
            Humidity: {{ weather.humidity }}%
          </v-col>
          <v-col cols="6">
            <v-icon size="small">mdi-weather-windy</v-icon>
            Wind: {{ weather.wind_speed }} km/h
          </v-col>
        </v-row>
      </v-card-text>
    </v-expand-transition>
  </v-card>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  weather: {
    type: Object,
    required: true,
  },
})

const collapsed = ref(false)
</script>
