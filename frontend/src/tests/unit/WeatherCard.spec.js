/**
 * Unit tests for WeatherCard component.
 * Tests rendering in isolation with mock props.
 */
import { describe, it, expect } from 'vitest'
import { mountWithVuetify } from './test-utils.js'
import WeatherCard from '@/components/WeatherCard.vue'

const mockWeather = {
  location: 'Castlemaine',
  temperature: 17.8,
  description: 'Partly cloudy',
  humidity: 55,
  wind_speed: 12.3,
  temp_min: 11.2,
  temp_max: 24.1,
  forecast_7day: [
    { day: 'F', temp_min: 13, temp_max: 23 },
    { day: 'S', temp_min: 11, temp_max: 21 },
    { day: 'S', temp_min: 10, temp_max: 20 },
    { day: 'M', temp_min: 12, temp_max: 22 },
    { day: 'T', temp_min: 14, temp_max: 24 },
    { day: 'W', temp_min: 13, temp_max: 25 },
    { day: 'T', temp_min: 11, temp_max: 23 },
  ],
  bom_today_url: 'https://www.bom.gov.au/location/australia/victoria/north-central/bvic_pt012-castlemaine#today',
  bom_7day_url: 'https://www.bom.gov.au/location/australia/victoria/north-central/bvic_pt012-castlemaine#7-days',
  total_fire_ban: false,
  fire_danger: null,
}

const mockFireDanger = [
  { day: 'T', rating: 'Extreme', index: 87 },
  { day: 'F', rating: 'High', index: 42 },
  { day: 'S', rating: 'Very High', index: null },
  { day: 'S', rating: 'Moderate', index: 18 },
]

describe('WeatherCard', () => {
  it('displays the location name', () => {
    const wrapper = mountWithVuetify(WeatherCard, { props: { weather: mockWeather } })
    expect(wrapper.text()).toContain('Castlemaine')
  })

  it('displays temperature as rounded integer', () => {
    const wrapper = mountWithVuetify(WeatherCard, { props: { weather: mockWeather } })
    expect(wrapper.text()).toContain('18°C')
  })

  it('displays today min and max as integers', () => {
    const wrapper = mountWithVuetify(WeatherCard, { props: { weather: mockWeather } })
    expect(wrapper.text()).toContain('Min 11°')
    expect(wrapper.text()).toContain('Max 24°')
  })

  it('renders 7-day forecast row with 7 entries', () => {
    const wrapper = mountWithVuetify(WeatherCard, { props: { weather: mockWeather } })
    const days = wrapper.findAll('.forecast-day')
    expect(days).toHaveLength(7)
  })

  it('displays correct day letters in forecast', () => {
    const wrapper = mountWithVuetify(WeatherCard, { props: { weather: mockWeather } })
    expect(wrapper.text()).toContain('F')
  })

  it('renders BOM Today link targeting new tab', () => {
    const wrapper = mountWithVuetify(WeatherCard, { props: { weather: mockWeather } })
    const links = wrapper.findAll('a[target="_blank"]')
    const todayLink = links.find(l => l.text().trim() === 'Today')
    expect(todayLink).toBeTruthy()
    expect(todayLink.attributes('href')).toContain('#today')
  })

  it('renders BOM 7-day link targeting new tab', () => {
    const wrapper = mountWithVuetify(WeatherCard, { props: { weather: mockWeather } })
    const links = wrapper.findAll('a[target="_blank"]')
    const sevenDayLink = links.find(l => l.text().trim() === '7-day')
    expect(sevenDayLink).toBeTruthy()
    expect(sevenDayLink.attributes('href')).toContain('#7-days')
  })

  it('collapses when the toggle is clicked', async () => {
    const wrapper = mountWithVuetify(WeatherCard, { props: { weather: mockWeather } })
    await wrapper.find('button').trigger('click')
    expect(wrapper.find('.v-card-text').isVisible()).toBe(false)
  })
})

describe('WeatherCard — Total Fire Ban', () => {
  it('shows TFB banner when total_fire_ban is true', () => {
    const weather = { ...mockWeather, total_fire_ban: true }
    const wrapper = mountWithVuetify(WeatherCard, { props: { weather } })
    expect(wrapper.find('.tfb-banner').exists()).toBe(true)
    expect(wrapper.text()).toContain('TOTAL FIRE BAN')
  })

  it('does not show TFB banner when total_fire_ban is false', () => {
    const wrapper = mountWithVuetify(WeatherCard, { props: { weather: mockWeather } })
    expect(wrapper.find('.tfb-banner').exists()).toBe(false)
  })
})

describe('WeatherCard — Fire Danger Ratings row', () => {
  it('shows FDR row when fire_danger is non-null', () => {
    const weather = { ...mockWeather, fire_danger: mockFireDanger }
    const wrapper = mountWithVuetify(WeatherCard, { props: { weather } })
    expect(wrapper.find('.fdr-row').exists()).toBe(true)
  })

  it('does not show FDR row when fire_danger is null', () => {
    const wrapper = mountWithVuetify(WeatherCard, { props: { weather: mockWeather } })
    expect(wrapper.find('.fdr-row').exists()).toBe(false)
  })

  it('renders 4 day columns in FDR row', () => {
    const weather = { ...mockWeather, fire_danger: mockFireDanger }
    const wrapper = mountWithVuetify(WeatherCard, { props: { weather } })
    expect(wrapper.findAll('.fdr-day')).toHaveLength(4)
  })

  it('shows Today/Tomorrow/+2/+3 day labels', () => {
    const weather = { ...mockWeather, fire_danger: mockFireDanger }
    const wrapper = mountWithVuetify(WeatherCard, { props: { weather } })
    expect(wrapper.text()).toContain('Today')
    expect(wrapper.text()).toContain('Tomorrow')
    expect(wrapper.text()).toContain('+2')
    expect(wrapper.text()).toContain('+3')
  })

  it('displays FDI index inline with rating when present', () => {
    const weather = { ...mockWeather, fire_danger: mockFireDanger }
    const wrapper = mountWithVuetify(WeatherCard, { props: { weather } })
    // mockFireDanger[0] = Extreme 87, [1] = High 42
    expect(wrapper.text()).toContain('Extreme 87')
    expect(wrapper.text()).toContain('High 42')
  })

  it('omits FDI index when null', () => {
    const weather = { ...mockWeather, fire_danger: mockFireDanger }
    const wrapper = mountWithVuetify(WeatherCard, { props: { weather } })
    const fdrDays = wrapper.findAll('.fdr-day')
    // Day index 2 has index: null — badge text should be just the rating, no trailing number
    expect(fdrDays[2].find('.fdr-badge').text().trim()).toBe('Very High')
  })

  it('displays rating labels', () => {
    const weather = { ...mockWeather, fire_danger: mockFireDanger }
    const wrapper = mountWithVuetify(WeatherCard, { props: { weather } })
    expect(wrapper.text()).toContain('Extreme')
    expect(wrapper.text()).toContain('High')
  })
})

describe('WeatherCard — FDR badge colours', () => {
  function hexToRgb(hex) {
    const r = parseInt(hex.slice(1, 3), 16)
    const g = parseInt(hex.slice(3, 5), 16)
    const b = parseInt(hex.slice(5, 7), 16)
    return `rgb(${r}, ${g}, ${b})`
  }

  function badgeForRating(rating) {
    const weather = { ...mockWeather, fire_danger: [{ day: 'T', rating, index: null }] }
    const wrapper = mountWithVuetify(WeatherCard, { props: { weather } })
    return wrapper.find('.fdr-badge')
  }

  it('Moderate badge has green background', () => {
    expect(badgeForRating('Moderate').element.style.backgroundColor).toBe(hexToRgb('#6DB840'))
  })

  it('High badge has yellow background', () => {
    expect(badgeForRating('High').element.style.backgroundColor).toBe(hexToRgb('#F7D94A'))
  })

  it('Extreme badge has orange background', () => {
    expect(badgeForRating('Extreme').element.style.backgroundColor).toBe(hexToRgb('#E87820'))
  })

  it('Catastrophic badge has dark red background', () => {
    expect(badgeForRating('Catastrophic').element.style.backgroundColor).toBe(hexToRgb('#922B21'))
  })

  it('No Rating badge has white background with black text', () => {
    const badge = badgeForRating('No Rating')
    expect(badge.element.style.backgroundColor).toBe(hexToRgb('#FFFFFF'))
    expect(badge.element.style.color).toBe(hexToRgb('#000000'))
  })

  it('unknown rating falls back to grey', () => {
    expect(badgeForRating('Very High').element.style.backgroundColor).toBe(hexToRgb('#888888'))
  })
})

describe('WeatherCard — FDR help popup', () => {
  it('shows ? button when fire_danger is non-null', () => {
    const weather = { ...mockWeather, fire_danger: mockFireDanger }
    const wrapper = mountWithVuetify(WeatherCard, { props: { weather } })
    expect(wrapper.find('.fdr-help-btn').exists()).toBe(true)
  })

  it('does not show ? button when fire_danger is null', () => {
    const wrapper = mountWithVuetify(WeatherCard, { props: { weather: mockWeather } })
    expect(wrapper.find('.fdr-help-btn').exists()).toBe(false)
  })

  it('shows all five AFDRS rating labels after clicking ?', async () => {
    const weather = { ...mockWeather, fire_danger: mockFireDanger }
    const wrapper = mountWithVuetify(WeatherCard, { props: { weather } })
    await wrapper.find('.fdr-help-btn').trigger('click')
    const helpText = wrapper.find('.fdr-help-panel').text()
    expect(helpText).toContain('No Rating')
    expect(helpText).toContain('Moderate')
    expect(helpText).toContain('High')
    expect(helpText).toContain('Extreme')
    expect(helpText).toContain('Catastrophic')
  })
})

describe('WeatherCard — FDR scale panel FBI ranges', () => {
  async function openPanel() {
    const weather = { ...mockWeather, fire_danger: mockFireDanger }
    const wrapper = mountWithVuetify(WeatherCard, { props: { weather } })
    await wrapper.find('.fdr-help-btn').trigger('click')
    return wrapper.find('.fdr-help-panel')
  }

  it('No Rating band shows FBI range < 12', async () => {
    expect((await openPanel()).text()).toContain('< 12')
  })

  it('Moderate band shows FBI range 12–23', async () => {
    expect((await openPanel()).text()).toContain('12–23')
  })

  it('High band shows FBI range 24–49', async () => {
    expect((await openPanel()).text()).toContain('24–49')
  })

  it('Extreme band shows FBI range 50–99', async () => {
    expect((await openPanel()).text()).toContain('50–99')
  })

  it('Catastrophic band shows FBI range ≥ 100', async () => {
    expect((await openPanel()).text()).toContain('≥ 100')
  })
})

export { mockWeather }
