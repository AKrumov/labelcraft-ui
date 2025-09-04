import { render } from '@testing-library/vue'
import Home from '../views/Home.vue'

it('renders home text', () => {
  const { getByText } = render(Home)
  getByText('LabelCraft')
})
