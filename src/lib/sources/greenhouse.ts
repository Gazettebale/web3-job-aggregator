import { Job } from '../types'

// Only confirmed working slugs (verified against Greenhouse API)
const GREENHOUSE_COMPANIES = [
  'coinbase',       // Coinbase
  'gemini',         // Gemini
  'bitgo',          // BitGo
  'fireblocks',     // Fireblocks
  'consensys',      // ConsenSys
  'paradigm',       // Paradigm
  'aptoslabs',      // Aptos Labs
  'robinhood',      // Robinhood
  'figment',        // Figment
  'blockchain-com', // Blockchain.com
]

const ONE_YEAR_MS = 365 * 24 * 60 * 60 * 1000

function extractTags(job: Record<string, unknown>): string[] {
  const tags: string[] = []
  const departments = (job.departments as Array<{ name: string }> | undefined) || []
  const location = job.location as { name?: string } | undefined
  const text = `${job.title || ''} ${departments.map((d) => d.name).join(' ')}`.toLowerCase()

  const roleMap: Record<string, string[]> = {
    'Engineer': ['engineer', 'engineering'],
    'Developer': ['developer', 'development'],
    'Designer': ['designer', 'design', 'ux', 'ui'],
    'Marketing': ['marketing', 'growth', 'brand'],
    'Product': ['product', 'pm', 'product manager'],
    'Research': ['research', 'researcher'],
    'Security': ['security', 'audit'],
    'Data': ['data', 'analytics', 'analyst'],
    'Community': ['community', 'social'],
    'Sales': ['sales', 'business development', 'bd'],
    'Finance': ['finance', 'accounting', 'legal', 'compliance'],
    'Operations': ['operations', 'ops'],
  }

  const chainMap: Record<string, string[]> = {
    'Ethereum': ['ethereum', 'evm', 'solidity'],
    'Solana': ['solana', 'rust'],
    'Polygon': ['polygon', 'matic'],
    'Arbitrum': ['arbitrum'],
    'Optimism': ['optimism', 'op stack'],
    'Base': ['base'],
    'Cosmos': ['cosmos', 'ibc'],
    'ZK': ['zk', 'zero-knowledge', 'zkp', 'zkevm'],
    'Bitcoin': ['bitcoin', 'btc'],
  }

  for (const [tag, keywords] of Object.entries(roleMap)) {
    if (keywords.some(k => text.includes(k))) tags.push(tag)
  }
  for (const [tag, keywords] of Object.entries(chainMap)) {
    if (keywords.some(k => text.includes(k))) tags.push(tag)
  }

  const locationName = (location?.name || '').toLowerCase()
  if (locationName.includes('remote') || locationName === '') tags.push('Remote')
  if (text.includes('senior') || text.includes('staff') || text.includes('principal')) tags.push('Senior')
  if (text.includes('junior') || text.includes('entry')) tags.push('Junior')
  if (text.includes('intern')) tags.push('Internship')

  return [...new Set(tags)]
}

export async function fetchGreenhouseJobs(): Promise<Job[]> {
  const jobs: Job[] = []

  const results = await Promise.allSettled(
    GREENHOUSE_COMPANIES.map(async (slug) => {
      const res = await fetch(
        `https://boards-api.greenhouse.io/v1/boards/${slug}/jobs`,
        { next: { revalidate: 3600 }, signal: AbortSignal.timeout(8000) }
      )
      if (!res.ok) return []
      const data = await res.json() as { jobs?: Record<string, unknown>[]; meta?: { name?: string } }
      const cutoff = Date.now() - ONE_YEAR_MS
      return (data.jobs || [])
        .filter((job) => {
          const updated = job.updated_at as string | undefined
          return !updated || new Date(updated).getTime() > cutoff
        })
        .slice(0, 30)
        .map((job) => {
        const location = job.location as { name?: string } | undefined
        return {
          id: `gh-${job.id}`,
          title: (job.title as string) || '',
          company: data.meta?.name || slug.replace(/-/g, ' '),
          location: location?.name || 'Remote',
          url: (job.absolute_url as string) || '',
          source: 'Greenhouse',
          tags: extractTags(job),
          remote: (location?.name || '').toLowerCase().includes('remote'),
          postedAt: job.updated_at as string | undefined,
        } as Job
      })
    })
  )

  for (const result of results) {
    if (result.status === 'fulfilled') jobs.push(...result.value)
  }

  return jobs
}
