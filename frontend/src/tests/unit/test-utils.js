import { mount } from '@vue/test-utils'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({ components, directives })

export function mountWithVuetify(component, options = {}) {
  return mount(component, {
    ...options,
    global: {
      plugins: [vuetify],
      ...options.global,
    },
  })
}
