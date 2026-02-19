import axios from 'axios'

const client = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 10000,
})

export const weatherApi = {
  getAll: () => client.get('/api/weather/'),
  getByCity: (city, country = 'AU') =>
    client.get(`/api/weather/${city}`, { params: { country } }),
}

export default client
