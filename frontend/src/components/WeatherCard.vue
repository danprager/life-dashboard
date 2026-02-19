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
        <!-- Current temperature -->
        <div class="text-h3 mb-1">{{ Math.round(weather.temperature) }}°C</div>

        <!-- Today min/max -->
        <div class="text-body-2 mb-2 text-medium-emphasis">
          Min {{ Math.round(weather.temp_min) }}° &nbsp; Max {{ Math.round(weather.temp_max) }}°
        </div>

        <!-- Description -->
        <div class="text-subtitle-1 mb-3">{{ weather.description }}</div>

        <!-- Humidity and wind -->
        <v-row dense class="mb-3">
          <v-col cols="6">
            <v-icon size="small">mdi-water-percent</v-icon>
            Humidity: {{ weather.humidity }}%
          </v-col>
          <v-col cols="6">
            <v-icon size="small">mdi-weather-windy</v-icon>
            Wind: {{ weather.wind_speed }} km/h
          </v-col>
        </v-row>

        <!-- 7-day forecast -->
        <v-row dense class="forecast-row mb-3">
          <v-col
            v-for="(day, i) in weather.forecast_7day"
            :key="i"
            class="forecast-day text-center pa-1"
          >
            <div class="text-caption font-weight-bold">{{ day.day }}</div>
            <div class="text-caption">{{ day.temp_max }}°</div>
            <div class="text-caption text-medium-emphasis">{{ day.temp_min }}°</div>
          </v-col>
        </v-row>

        <!-- BOM links -->
        <div class="d-flex align-center gap-2">
          <span class="text-caption text-medium-emphasis">BOM forecasts:</span>
          <v-btn
            :href="weather.bom_today_url"
            target="_blank"
            rel="noopener"
            variant="tonal"
            size="small"
            density="compact"
          >
            Today
          </v-btn>
          <v-btn
            :href="weather.bom_7day_url"
            target="_blank"
            rel="noopener"
            variant="tonal"
            size="small"
            density="compact"
            class="ml-1"
          >
            7-day
          </v-btn>
        </div>
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

<style scoped>
.forecast-row {
  flex-wrap: nowrap;
}
.forecast-day {
  min-width: 0;
  flex: 1;
}
</style>
