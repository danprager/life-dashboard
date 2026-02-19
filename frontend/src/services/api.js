import axios from 'axios'

const client = axios.create({
  baseURL: '',
  timeout: 10000,
})

export const weatherApi = {
  getAll: () => client.get('/api/weather/'),
  getByCity: (city, country = 'AU') =>
    client.get(`/api/weather/${city}`, { params: { country } }),
}

export default client
