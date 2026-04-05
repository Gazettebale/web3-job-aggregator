import { Job } from '../types'

// Only confirmed working slugs (verified against Lever API)
const LEVER_COMPANIES = [
  'binance',   // Binance
  'zerion',    // Zerion
  'immutable', // Immutable
  '1inch',     // 1inch Network
]

const ONE_YEAR_MS = 365 * 24 * 60 * 60 * 1000

interface LeverPosting {
  id: string
  text: string
  company?: string
  hostedUrl?: string
  applyUrl?: string
  createdAt?: number
  categories?: {
    team?: string
    department?: string
    location?: string
    commitment?: string
  }
  workplaceType?: string
}

function extractTags(posting: LeverPosting): string[] {
  const tags: string[] = []
  const text = `${posting.text || ''} ${posting.categories?.team || ''} ${posting.categories?.department || ''}`.toLowerCase()

  if (['engineer', 'developer', 'dev ', 'development'].some(k => text.includes(k))) tags.push('Engineer')
  if (['design', 'designer', 'ux', 'ui '].some(k => text.includes(k))) tags.push('Designer')
  if (['marketing', 'growth'].some(k => text.includes(k))) tags.push('Marketing')
  if (['product manager', 'product lead', ' pm '].some(k => text.includes(k))) tags.push('Product')
  if (['research', 'researcher'].some(k => text.includes(k))) tags.push('Research')
  if (['security', 'audit'].some(k => text.includes(k))) tags.push('Security')
  if (['data analyst', 'data scientist', 'data engineer'].some(k => text.includes(k))) tags.push('Data')
  if (['community', 'social media'].some(k => text.includes(k))) tags.push('Community')
  if (['business development', 'partnerships', 'sales'].some(k => text.includes(k))) tags.push('Sales')

  if (['ethereum', 'solidity', 'evm'].some(k => text.includes(k))) tags.push('Ethereum')
  if (['solana', ' sol ', 'rust'].some(k => text.includes(k))) tags.push('Solana')
  if (['polygon', 'matic'].some(k => text.includes(k))) tags.push('Polygon')
  if (['zk', 'zero-knowledge'].some(k => text.includes(k))) tags.push('ZK')
  if (['arbitrum'].some(k => text.includes(k))) tags.push('Arbitrum')
  if (['cosmos', 'ibc'].some(k => text.includes(k))) tags.push('Cosmos')

  const location = (posting.categories?.location || '').toLowerCase()
  const commitment = (posting.categories?.commitment || '').toLowerCase()
  if (location.includes('remote') || location === 'anywhere') tags.push('Remote')
  if (commitment.includes('full') || commitment === '') tags.push('Full-time')
  if (commitment.includes('part')) tags.push('Part-time')
  if (commitment.includes('contract')) tags.push('Contract')
  if (commitment.includes('intern')) tags.push('Internship')

  if (['senior', 'staff ', 'principal', 'lead '].some(k => text.includes(k))) tags.push('Senior')
  if (['junior', 'entry level', 'associate'].some(k => text.includes(k))) tags.push('Junior')

  return [...new Set(tags)]
}

export async function fetchLeverJobs(): Promise<Job[]> {
  const jobs: Job[] = []

  const results = await Promise.allSettled(
    LEVER_COMPANIES.map(async (slug) => {
      const res = await fetch(
        `https://api.lever.co/v0/postings/${slug}?mode=json`,
        { next: { revalidate: 3600 }, signal: AbortSignal.timeout(8000) }
      )
      if (!res.ok) return []
      const data = await res.json() as LeverPosting[]
      const cutoff = Date.now() - ONE_YEAR_MS
      return (Array.isArray(data) ? data : [])
        .filter(p => !p.createdAt || p.createdAt > cutoff)
        .slice(0, 30)
        .map((posting) => ({
        id: `lv-${posting.id}`,
        title: posting.text || '',
        company: posting.company || slug.replace(/-/g, ' '),
        location: posting.categories?.location || posting.workplaceType || 'Remote',
        url: posting.hostedUrl || posting.applyUrl || '',
        source: 'Lever',
        tags: extractTags(posting),
        remote: ['remote', 'anywhere', 'distributed'].includes((posting.categories?.location || '').toLowerCase()),
        postedAt: posting.createdAt ? new Date(posting.createdAt).toISOString() : undefined,
      } as Job))
    })
  )

  for (const result of results) {
    if (result.status === 'fulfilled') jobs.push(...result.value)
  }

  return jobs
}
