import { describe, it, expect } from 'vitest'

import { mount } from '@vue/test-utils'
import App from '../App.vue'

describe('App', () => {
  it('renders main layout', () => {
    const wrapper = mount(App)
    expect(wrapper.text()).toContain('AI Testing Standard Platform')
  })
})
