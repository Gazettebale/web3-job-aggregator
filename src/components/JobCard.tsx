'use client'
import { Job } from '@/lib/types'
import { timeAgo } from '@/lib/utils'

interface Props {
  job: Job
}

const SOURCE_COLORS: Record<string, string> = {
  Greenhouse: '#22c55e',
  Lever: '#3b82f6',
  CryptocurrencyJobs: '#f97316',
}

export default function JobCard({ job }: Props) {
  const sourceColor = SOURCE_COLORS[job.source] || '#8b5cf6'

  return (
    <div
      className="group flex flex-col h-full rounded-xl border p-5 transition-all hover:border-violet-500/50"
      style={{ background: 'var(--bg-card)', borderColor: 'var(--border)' }}
    >
      {/* Top row: source + remote badge + time */}
      <div className="flex items-start justify-between gap-2 mb-3">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1 flex-wrap">
            <span
              className="text-xs font-medium px-2 py-0.5 rounded-full"
              style={{ background: sourceColor + '22', color: sourceColor }}
            >
              {job.source}
            </span>
            {job.remote && (
              <span
                className="text-xs px-2 py-0.5 rounded-full"
                style={{ background: '#06b6d422', color: '#06b6d4' }}
              >
                Remote
              </span>
            )}
          </div>
          <p className="text-xs font-medium truncate" style={{ color: 'var(--text-muted)' }}>
            {job.company}
          </p>
        </div>
        {job.postedAt && (
          <p className="text-xs flex-shrink-0 mt-0.5" style={{ color: 'var(--text-muted)' }}>
            {timeAgo(job.postedAt)}
          </p>
        )}
      </div>

      {/* Title */}
      <h3
        className="font-semibold text-base leading-snug mb-2 group-hover:text-violet-400 transition-colors"
        style={{ color: 'var(--text-primary)' }}
      >
        {job.title}
      </h3>

      {/* Location */}
      <p className="text-xs mb-3" style={{ color: 'var(--text-muted)' }}>
        📍 {job.location}
      </p>

      {/* Tags */}
      <div className="flex flex-wrap gap-1.5 mb-4 flex-1">
        {job.tags.slice(0, 4).map(tag => (
          <span
            key={tag}
            className="text-xs px-2 py-0.5 rounded-md"
            style={{ background: '#27272a', color: 'var(--text-muted)' }}
          >
            {tag}
          </span>
        ))}
        {job.tags.length > 4 && (
          <span
            className="text-xs px-2 py-0.5 rounded-md"
            style={{ background: '#27272a', color: 'var(--text-muted)' }}
          >
            +{job.tags.length - 4}
          </span>
        )}
      </div>

      {/* Apply button */}
      <a
        href={job.url}
        target="_blank"
        rel="noopener noreferrer"
        className="mt-auto w-full text-center text-sm font-medium py-2 rounded-lg transition-all"
        style={{
          background: '#8b5cf622',
          color: '#8b5cf6',
          border: '1px solid #8b5cf633',
        }}
        onMouseEnter={e => {
          e.currentTarget.style.background = '#8b5cf633'
        }}
        onMouseLeave={e => {
          e.currentTarget.style.background = '#8b5cf622'
        }}
      >
        Apply →
      </a>
    </div>
  )
}
