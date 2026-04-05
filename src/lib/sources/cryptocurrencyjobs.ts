import { Job } from '../types'

// CryptocurrencyJobs.co uses Algolia search under the hood
// The search API key is a public read-only key embedded in their JS bundle
const ALGOLIA_APP_ID = '8EHCB38Y1U'
const ALGOLIA_SEARCH_KEY = 'e3deada9c15551e6363ee91e7e7d59cc'
const ALGOLIA_INDEX = 'jobs'

interface AlgoliaHit {
  objectID: string
  title: string
  company?: { name?: string; url?: string }
  permalink?: string
  remoteLocation?: { name?: string }
  onsiteLocation?: string | Record<string, string>
  locationFilter?: string[]
  keywords?: Array<{ name: string }>
  employmentTypes?: Array<{ name: string }>
  role?: { name?: string }
  datePublished?: string
  baseSalary?: string
}

function mapHitToJob(hit: AlgoliaHit): Job {
  const tags: string[] = []

  // Role
  if (hit.role?.name) tags.push(hit.role.name)

  // Keywords → tags
  const keywordMap: Record<string, string> = {
    'Solidity': 'Solidity', 'Rust': 'Rust', 'React': 'React',
    'TypeScript': 'TypeScript', 'Python': 'Python', 'Go': 'Go',
    'DeFi': 'DeFi', 'NFT': 'NFT', 'DAO': 'DAO', 'Web3': 'Web3',
    'Ethereum': 'Ethereum', 'Solana': 'Solana', 'Polygon': 'Polygon',
    'Layer 2': 'Layer2', 'ZK': 'ZK', 'Infrastructure': 'Infrastructure',
    'Gaming': 'Gaming', 'Security': 'Security', 'Research': 'Research',
    'Marketing': 'Marketing', 'Design': 'Designer', 'Product': 'Product',
    'Engineering': 'Engineer', 'Developer': 'Developer', 'Data': 'Data',
    'Community': 'Community', 'Finance': 'Finance', 'Legal': 'Legal',
  }
  for (const kw of hit.keywords || []) {
    const mapped = keywordMap[kw.name] || kw.name
    if (mapped) tags.push(mapped)
  }

  // Employment type
  for (const et of hit.employmentTypes || []) {
    if (et.name === 'Full-Time') tags.push('Full-time')
    else if (et.name === 'Part-Time') tags.push('Part-time')
    else if (et.name === 'Contract') tags.push('Contract')
    else if (et.name === 'Internship') tags.push('Internship')
  }

  // Remote
  const isRemote = (hit.locationFilter || []).some(l => l.toLowerCase().includes('remote'))
  if (isRemote) tags.push('Remote')

  // onsiteLocation can be an object {city, country} or a string depending on the listing
  const rawOnsite = hit.onsiteLocation
  const onsiteStr = typeof rawOnsite === 'string'
    ? rawOnsite
    : rawOnsite && typeof rawOnsite === 'object'
      ? ((rawOnsite as Record<string, string>).city || (rawOnsite as Record<string, string>).name || '')
      : ''
  const location = hit.remoteLocation?.name || onsiteStr ||
    (hit.locationFilter || []).find(l => typeof l === 'string' && !l.includes('/')) ||
    'Remote'

  return {
    id: `ccj-${hit.objectID}`,
    title: String(hit.title || ''),
    company: String(hit.company?.name || 'Unknown'),
    location: String(location),
    url: hit.permalink ? `https://cryptocurrencyjobs.co${hit.permalink}` : 'https://cryptocurrencyjobs.co',
    source: 'CryptocurrencyJobs',
    tags: [...new Set(tags)],
    remote: isRemote,
    postedAt: hit.datePublished,
    salary: hit.baseSalary,
  }
}

export async function fetchCryptocurrencyJobs(): Promise<Job[]> {
  try {
    // Fetch up to 200 jobs (pages of 100)
    const pages = await Promise.allSettled([
      queryAlgolia(0, 100),
      queryAlgolia(1, 100),
    ])

    const jobs: Job[] = []
    for (const page of pages) {
      if (page.status === 'fulfilled') jobs.push(...page.value)
    }
    return jobs
  } catch {
    return []
  }
}

async function queryAlgolia(page: number, hitsPerPage: number): Promise<Job[]> {
  const res = await fetch(
    `https://${ALGOLIA_APP_ID}-dsn.algolia.net/1/indexes/${ALGOLIA_INDEX}/query`,
    {
      method: 'POST',
      next: { revalidate: 3600 },
      signal: AbortSignal.timeout(10000),
      headers: {
        'X-Algolia-API-Key': ALGOLIA_SEARCH_KEY,
        'X-Algolia-Application-Id': ALGOLIA_APP_ID,
        'Content-Type': 'application/json',
        'Referer': 'https://cryptocurrencyjobs.co/',
        'Origin': 'https://cryptocurrencyjobs.co',
      },
      body: JSON.stringify({ query: '', hitsPerPage, page }),
    }
  )

  if (!res.ok) return []
  const data = await res.json()
  return (data.hits || []).map(mapHitToJob)
}
