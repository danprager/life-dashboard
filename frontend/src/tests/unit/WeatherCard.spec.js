/**
 * Unit tests for WeatherCard component.
 * Tests rendering in isolation with mock props.
 */
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
// import WeatherCard from '@/components/WeatherCard.vue'

const mockWeather = {
  location: 'Sydney, AU',
  temperature: 22.4,
  description: 'Partly cloudy',
  humidity: 65,
  wind_speed: 15.2,
}

// TODO: implement tests as part of TDD workflow
// Vuetify requires a plugin wrapper — set that up before enabling tests.

// describe('WeatherCard', () => {
//   it('displays the location name', () => {
//     const wrapper = mount(WeatherCard, { props: { weather: mockWeather } })
//     expect(wrapper.text()).toContain('Sydney, AU')
//   })
//
//   it('displays temperature', () => {
//     const wrapper = mount(WeatherCard, { props: { weather: mockWeather } })
//     expect(wrapper.text()).toContain('22.4')
//   })
//
//   it('collapses when the toggle is clicked', async () => {
//     const wrapper = mount(WeatherCard, { props: { weather: mockWeather } })
//     await wrapper.find('button').trigger('click')
//     expect(wrapper.find('.v-card-text').isVisible()).toBe(false)
//   })
// })

export { mockWeather }
