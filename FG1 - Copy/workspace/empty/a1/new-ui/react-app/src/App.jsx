import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import AccountsList from './AccountsList'
import LoginForm from './LoginForm'
import RegisterForm from './RegisterForm'

function App() {
  const [count, setCount] = useState(0)
  const [user, setUser] = useState(null)
  const [showRegister, setShowRegister] = useState(false)

  const handleLogin = (data) => {
    setUser(data)
    localStorage.setItem('authToken', data.token || data.access_token || '')
  }
  const handleRegister = (data) => {
    setShowRegister(false)
    alert('Registration successful! Please log in.')
  }

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <button onClick={() => setShowRegister(r => !r)} style={{marginLeft:8}}>
          {showRegister ? 'Show Login' : 'Show Register'}
        </button>
      </div>
      {!user && !showRegister && <LoginForm onLogin={handleLogin} />}
      {!user && showRegister && <RegisterForm onRegister={handleRegister} />}
      {user && <AccountsList />}
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App
