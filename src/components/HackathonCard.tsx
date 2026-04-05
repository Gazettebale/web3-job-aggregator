'use client'
import { Hackathon } from '@/lib/types'
import { formatDate } from '@/lib/utils'

interface Props {
  hackathon: Hackathon
}

const STATUS_STYLES = {
  live: { bg: '#22c55e22', color: '#22c55e', label: '● LIVE' },
  upcoming: { bg: '#06b6d422', color: '#06b6d4', label: 'UPCOMING' },
  ended: { bg: '#27272a', color: '#71717a', label: 'ENDED' },
}

export default function HackathonCard({ hackathon }: Props) {
  const status = STATUS_STYLES[hackathon.status]

  return (
    <div
      className="group flex flex-col h-full rounded-xl border p-5 transition-all hover:border-cyan-500/50"
      style={{ background: 'var(--bg-card)', borderColor: 'var(--border)' }}
    >
      {/* Top row: status + source */}
      <div className="flex items-start justify-between gap-2 mb-3">
        <span
          className="text-xs font-bold px-2 py-0.5 rounded-full"
          style={{ background: status.bg, color: status.color }}
        >
          {status.label}
        </span>
        <span className="text-xs" style={{ color: 'var(--text-muted)' }}>
          {hackathon.source}
        </span>
      </div>

      {/* Title */}
      <h3
        className="font-semibold text-base leading-snug mb-1 group-hover:text-cyan-400 transition-colors"
        style={{ color: 'var(--text-primary)' }}
      >
        {hackathon.title}
      </h3>

      {/* Organizer */}
      <p className="text-xs mb-2" style={{ color: 'var(--text-muted)' }}>
        by {hackathon.organizer}
      </p>

      {/* Description */}
      {hackathon.description && (
        <p
          className="text-xs mt-1 mb-3 line-clamp-2"
          style={{ color: 'var(--text-muted)' }}
        >
          {hackathon.description}
        </p>
      )}

      {/* Details */}
      <div className="space-y-1 mb-3 flex-1">
        {hackathon.prize && (
          <p className="text-sm font-semibold" style={{ color: '#22c55e' }}>
            🏆 {hackathon.prize}
          </p>
        )}
        {hackathon.location && (
          <p className="text-xs" style={{ color: 'var(--text-muted)' }}>
            📍 {hackathon.location}
          </p>
        )}
        {(hackathon.startDate || hackathon.endDate) && (
          <p className="text-xs" style={{ color: 'var(--text-muted)' }}>
            🗓{' '}
            {hackathon.startDate ? formatDate(hackathon.startDate) : '?'}
            {hackathon.endDate ? ` → ${formatDate(hackathon.endDate)}` : ''}
          </p>
        )}
      </div>

      {/* Tags */}
      <div className="flex flex-wrap gap-1.5 mb-4">
        {hackathon.tags.slice(0, 3).map(tag => (
          <span
            key={tag}
            className="text-xs px-2 py-0.5 rounded-md"
            style={{ background: '#27272a', color: 'var(--text-muted)' }}
          >
            {tag}
          </span>
        ))}
      </div>

      {/* CTA button */}
      <a
        href={hackathon.url}
        target="_blank"
        rel="noopener noreferrer"
        className="mt-auto w-full text-center text-sm font-medium py-2 rounded-lg transition-all"
        style={{
          background: '#06b6d422',
          color: '#06b6d4',
          border: '1px solid #06b6d433',
        }}
        onMouseEnter={e => {
          e.currentTarget.style.background = '#06b6d433'
        }}
        onMouseLeave={e => {
          e.currentTarget.style.background = '#06b6d422'
        }}
      >
        View Hackathon →
      </a>
    </div>
  )
}
