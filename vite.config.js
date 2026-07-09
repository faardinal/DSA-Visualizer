import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5000,
    allowedHosts: true,
    proxy: {
      '/api/run': 'http://localhost:8000',
      '/api/health': 'http://localhost:8000',
      '/api/config': 'http://localhost:8000',
    },
  },
})

