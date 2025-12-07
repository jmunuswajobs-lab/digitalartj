
import React, { useState } from 'react'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

type Intensity = 'L1' | 'L2' | 'L3'

const styleFamilies = [
  { code: 'C1', label: 'C1 - Dark Near-Square (Intimate)' },
  { code: 'C2', label: 'C2 - Bright Near-Square (Playful)' },
  { code: 'C3', label: 'C3 - Dark Portrait (Cinematic)' },
  { code: 'C4', label: 'C4 - Neutral Portrait (Boudoir)' },
  { code: 'C5', label: 'C5 - Bright Portrait (Glamour)' },
  { code: 'C6', label: 'C6 - Landscape Scene (Bedroom)' },
]

export const App: React.FC = () => {
  const [file, setFile] = useState<File | null>(null)
  const [styleFamily, setStyleFamily] = useState('C3')
  const [intensity, setIntensity] = useState<Intensity>('L2')
  const [artVariant, setArtVariant] = useState('oil_painting')
  const [pose, setPose] = useState('reclining on a bed, side profile')
  const [clothing, setClothing] = useState('black lace lingerie, partially covered by bedsheet')
  const [environment, setEnvironment] = useState('dim bedroom with warm bedside lamp')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [resultUrl, setResultUrl] = useState<string | null>(null)
  const [promptUsed, setPromptUsed] = useState<string | null>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0]
    setFile(f || null)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setResultUrl(null)
    setPromptUsed(null)

    if (!file) {
      setError('Please select an image first.')
      return
    }

    const form = new FormData()
    form.append('file', file)
    form.append('style_family', styleFamily)
    form.append('intensity', intensity)
    form.append('art_style_variant', artVariant)
    form.append('pose_description', pose)
    form.append('clothing_description', clothing)
    form.append('environment_description', environment)

    try {
      setLoading(true)
      const res = await fetch(`${API_BASE}/api/generate`, {
        method: 'POST',
        body: form,
      })
      if (!res.ok) {
        const err = await res.json().catch(() => ({}))
        throw new Error(err.detail || 'Generation failed')
      }
      const data = await res.json()
      setResultUrl(`${API_BASE}${data.image_url}`)
      setPromptUsed(data.prompt_used)
    } catch (err: any) {
      setError(err.message || 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ maxWidth: 900, margin: '0 auto', padding: 24, fontFamily: 'system-ui, sans-serif' }}>
      <h1>18+ Digital Art Generator (Self-Hosted)</h1>
      <p style={{ fontSize: 14, opacity: 0.8 }}>
        Upload an image (adult 18+ only), choose a style family and intensity,
        and this app will call your Stable Diffusion server (e.g. Automatic1111)
        with safe, erotic-but-non-explicit prompts.
      </p>

      <form onSubmit={handleSubmit} style={{ marginTop: 24, display: 'grid', gap: 16 }}>
        <div>
          <label>Input Image (reference):</label><br />
          <input type="file" accept="image/*" onChange={handleFileChange} />
        </div>

        <div>
          <label>Style Family:</label><br />
          <select value={styleFamily} onChange={e => setStyleFamily(e.target.value)}>
            {styleFamilies.map(sf => (
              <option key={sf.code} value={sf.code}>{sf.label}</option>
            ))}
          </select>
        </div>

        <div>
          <label>Intensity Level:</label><br />
          <select value={intensity} onChange={e => setIntensity(e.target.value as Intensity)}>
            <option value="L1">L1 - Soft Erotic</option>
            <option value="L2">L2 - Strong Erotic</option>
            <option value="L3">L3 - Max Sensual (Non-Explicit)</option>
          </select>
        </div>

        <div>
          <label>Art Style Variant:</label><br />
          <select value={artVariant} onChange={e => setArtVariant(e.target.value)}>
            <option value="oil_painting">Oil painting</option>
            <option value="digital_illustration">Digital illustration</option>
            <option value="hyperreal_digital_art">Hyperreal digital art</option>
            <option value="watercolor_painting">Watercolor painting</option>
            <option value="anime_style_painting">Anime-style painting</option>
          </select>
        </div>

        <div>
          <label>Pose Description:</label><br />
          <input
            type="text"
            value={pose}
            onChange={e => setPose(e.target.value)}
            style={{ width: '100%' }}
          />
        </div>

        <div>
          <label>Clothing / Fabric Description:</label><br />
          <input
            type="text"
            value={clothing}
            onChange={e => setClothing(e.target.value)}
            style={{ width: '100%' }}
          />
        </div>

        <div>
          <label>Environment Description:</label><br />
          <input
            type="text"
            value={environment}
            onChange={e => setEnvironment(e.target.value)}
            style={{ width: '100%' }}
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Generating…' : 'Generate Art'}
        </button>
      </form>

      {error && (
        <div style={{ marginTop: 16, color: 'red' }}>
          Error: {error}
        </div>
      )}

      {resultUrl && (
        <div style={{ marginTop: 24 }}>
          <h2>Result</h2>
          <img src={resultUrl} alt="Generated" style={{ maxWidth: '100%', borderRadius: 8 }} />
        </div>
      )}

      {promptUsed && (
        <div style={{ marginTop: 16 }}>
          <details>
            <summary>Prompt used</summary>
            <pre style={{ whiteSpace: 'pre-wrap' }}>{promptUsed}</pre>
          </details>
        </div>
      )}

      <hr style={{ marginTop: 32, marginBottom: 16 }} />
      <p style={{ fontSize: 12, opacity: 0.7 }}>
        Note: This frontend is static and can be deployed on GitHub Pages. The backend must be self-hosted
        (FastAPI + Stable Diffusion / Automatic1111) and configured via VITE_API_BASE.
      </p>
    </div>
  )
}
