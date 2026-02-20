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
        <div class="d-flex align-center mb-3">
          <span class="text-caption text-medium-emphasis mr-3">BOM forecasts:</span>
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

        <!-- Total Fire Ban banner -->
        <div v-if="weather.total_fire_ban" class="tfb-banner mb-3">
          TOTAL FIRE BAN
        </div>

        <!-- Fire Danger Ratings row (Castlemaine only) -->
        <div v-if="weather.fire_danger" class="mb-2">
          <div class="d-flex align-center mb-1">
            <span class="text-subtitle-1">🔥 Fire danger rating 🔥</span>
            <v-btn
              class="fdr-help-btn ml-1"
              variant="tonal"
              size="small"
              density="compact"
              @click="helpOpen = !helpOpen"
            >Scale</v-btn>
          </div>
          <div v-if="helpOpen" class="fdr-help-panel mb-2">
            <div
              v-for="[rating, colours] in Object.entries(FDR_COLOURS)"
              :key="rating"
              class="fdr-help-band text-caption font-weight-bold px-2 py-1"
              :style="{ backgroundColor: colours.bg, color: colours.text }"
            >
              {{ rating }} ({{ colours.fbi }})
            </div>
          </div>
          <div class="fdr-row">
            <div
              v-for="(day, i) in weather.fire_danger"
              :key="i"
              class="fdr-day text-center"
            >
              <div class="text-caption font-weight-bold mb-1">{{ fdrDayLabel(i) }}</div>
              <div
                class="fdr-badge text-caption font-weight-bold"
                :style="{ backgroundColor: fdrColour(day.rating), color: fdrText(day.rating) }"
              >
                {{ day.rating }}{{ day.index !== null ? ' ' + day.index : '' }}
              </div>
            </div>
          </div>
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
const helpOpen = ref(false)

const FDR_COLOURS = {
  'Catastrophic':{ bg: '#922B21', text: '#ffffff', fbi: '≥ 100' },
  'Extreme':     { bg: '#E87820', text: '#000000', fbi: '50–99' },
  'High':        { bg: '#F7D94A', text: '#000000', fbi: '24–49' },
  'Moderate':    { bg: '#6DB840', text: '#000000', fbi: '12–23' },
  'No Rating':   { bg: '#FFFFFF', text: '#000000', fbi: '< 12'  },
}

const FDR_FALLBACK = { bg: '#888888', text: '#ffffff' }

function fdrColour(rating) {
  return (FDR_COLOURS[rating] ?? FDR_FALLBACK).bg
}

function fdrText(rating) {
  return (FDR_COLOURS[rating] ?? FDR_FALLBACK).text
}

// CFA feed does not include numeric FDI values; index is always null from this feed.
// Labels based on position in the 4-day array, not the day-of-week letter.
const FDR_DAY_LABELS = ['Today', 'Tomorrow', '+2', '+3']
function fdrDayLabel(i) {
  return FDR_DAY_LABELS[i] ?? `+${i}`
}
</script>

<style scoped>
.forecast-row {
  flex-wrap: nowrap;
}
.forecast-day {
  min-width: 0;
  flex: 1;
}
.tfb-banner {
  background-color: #e8260b;
  color: #fff;
  font-weight: bold;
  text-align: center;
  padding: 6px 12px;
  border-radius: 4px;
  letter-spacing: 0.05em;
}
.fdr-row {
  display: flex;
  gap: 4px;
}
.fdr-day {
  flex: 1;
  min-width: 0;
}
.fdr-badge {
  padding: 2px 4px;
  border-radius: 3px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.fdr-help-panel {
  border: 1px solid #eee;
  border-radius: 4px;
  overflow: hidden;
}
</style>
