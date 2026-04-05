import { NextResponse } from 'next/server'
import { fetchGreenhouseJobs } from '@/lib/sources/greenhouse'
import { fetchLeverJobs } from '@/lib/sources/lever'
import { fetchCryptocurrencyJobs } from '@/lib/sources/cryptocurrencyjobs'

export async function GET() {
  const [greenhouse, lever, ccj] = await Promise.allSettled([
    fetchGreenhouseJobs(),
    fetchLeverJobs(),
    fetchCryptocurrencyJobs(),
  ])

  const jobs = [
    ...(greenhouse.status === 'fulfilled' ? greenhouse.value : []),
    ...(lever.status === 'fulfilled' ? lever.value : []),
    ...(ccj.status === 'fulfilled' ? ccj.value : []),
  ]

  // Deduplicate by title + company
  const seen = new Set<string>()
  const deduped = jobs.filter(job => {
    const key = `${job.title.toLowerCase()}|${job.company.toLowerCase()}`
    if (seen.has(key)) return false
    seen.add(key)
    return job.title && job.url
  })

  return NextResponse.json({
    jobs: deduped,
    sources: {
      greenhouse: greenhouse.status === 'fulfilled' ? greenhouse.value.length : 0,
      lever: lever.status === 'fulfilled' ? lever.value.length : 0,
      cryptocurrencyjobs: ccj.status === 'fulfilled' ? ccj.value.length : 0,
    },
    total: deduped.length,
  })
}
