import { render, screen } from '@testing-library/react';
import App from '../App';

test('renders banking app main UI', () => {
  render(<App />);
  expect(screen.getByText(/login/i)).toBeInTheDocument();
});
