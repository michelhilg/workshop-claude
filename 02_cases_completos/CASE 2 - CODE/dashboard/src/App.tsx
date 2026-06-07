import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/layout/Layout'
import Overview from './pages/Overview'
import Funnel from './pages/Funnel'
import Campaigns from './pages/Campaigns'
import SalesReps from './pages/SalesReps'
import Objections from './pages/Objections'
import DataQuality from './pages/DataQuality'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<Overview />} />
          <Route path="funnel" element={<Funnel />} />
          <Route path="campaigns" element={<Campaigns />} />
          <Route path="reps" element={<SalesReps />} />
          <Route path="objections" element={<Objections />} />
          <Route path="quality" element={<DataQuality />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
