import { useEffect, useState } from 'react'
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import axios from 'axios'

const getColor = (jenis) => {
  const colors = {
    'Sekolah': '#3498db',
    'Apotek': '#e74c3c',
    'Puskesmas': '#2ecc71',
    'Pasar': '#f39c12',
    'Rumah Sakit': '#9b59b6',
    'Masjid': '#1abc9c',
  }
  return colors[jenis] || '#95a5a6'
}

const MapComponent = () => {
  const [features, setFeatures] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    axios.get('http://localhost:8000/api/fasilitas/geojson/all')
      .then(res => {
        const valid = res.data.features.filter(f => {
          const [lng, lat] = f.geometry.coordinates
          return lng !== -180 && lat !== -90
        })
        setFeatures(valid)
        setLoading(false)
      })
      .catch(err => {
        setError('Gagal mengambil data dari API')
        setLoading(false)
      })
  }, [])

  if (loading) return <div style={{padding:'20px', fontSize:'18px'}}>⏳ Memuat data peta...</div>
  if (error) return <div style={{padding:'20px', color:'red'}}>❌ {error}</div>

  return (
    <div style={{ position: 'relative', height: '100vh' }}>
      <MapContainer
        center={[-5.43, 105.26]}
        zoom={13}
        style={{ height: '100vh', width: '100%' }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; OpenStreetMap contributors'
        />

        {features.map((f, i) => {
          const [lng, lat] = f.geometry.coordinates
          const p = f.properties
          const color = getColor(p.jenis)

          return (
            <CircleMarker
              key={i}
              center={[lat, lng]}
              radius={10}
              pathOptions={{
                fillColor: color,
                color: '#fff',
                weight: 2,
                fillOpacity: 0.85
              }}
              eventHandlers={{
                mouseover: (e) => {
                  e.target.setStyle({ fillOpacity: 1, weight: 4, color: '#222' })
                  e.target.openPopup()
                },
                mouseout: (e) => {
                  e.target.setStyle({ fillOpacity: 0.85, weight: 2, color: '#fff' })
                  e.target.closePopup()
                }
              }}
            >
              <Popup>
                <div style={{fontFamily:'Arial', minWidth:'160px'}}>
                  <h3 style={{margin:'0 0 6px 0', color:'#2c3e50'}}>{p.nama || '-'}</h3>
                  <hr style={{marginBottom:'6px'}}/>
                  <b>Jenis:</b> {p.jenis || '-'}<br/>
                  <b>Alamat:</b> {p.alamat || '-'}
                </div>
              </Popup>
            </CircleMarker>
          )
        })}
      </MapContainer>

      {/* Legend */}
      <div style={{
        position:'absolute', bottom:30, right:10, zIndex:1000,
        background:'white', padding:'10px 15px', borderRadius:8,
        boxShadow:'0 2px 8px rgba(0,0,0,0.3)', fontFamily:'Arial', fontSize:13
      }}>
        <b style={{display:'block', marginBottom:6}}>Jenis Fasilitas</b>
        {[
          ['Sekolah','#3498db'],
          ['Apotek','#e74c3c'],
          ['Puskesmas','#2ecc71'],
          ['Pasar','#f39c12'],
          ['Rumah Sakit','#9b59b6'],
          ['Masjid','#1abc9c'],
          ['Lainnya','#95a5a6'],
        ].map(([label, color]) => (
          <div key={label} style={{display:'flex', alignItems:'center', marginBottom:4}}>
            <span style={{
              width:12, height:12, borderRadius:'50%',
              background:color, display:'inline-block', marginRight:8
            }}/>
            {label}
          </div>
        ))}
      </div>
    </div>
  )
}

export default MapComponent