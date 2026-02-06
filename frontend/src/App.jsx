import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [apiStatus, setApiStatus] = useState('checking...')

  useEffect(() => {
    fetch('/api')
      .then(res => res.json())
      .then(data => setApiStatus(data.message))
      .catch(() => setApiStatus('API not available'))
  }, [])

  return (
    <div className="App">
      <header className="App-header">
        <h1>Rating Workbench</h1>
        <p>API Status: {apiStatus}</p>
      </header>
    </div>
  )
}

export default App
