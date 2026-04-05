'use client'
import { Grant } from '@/lib/types'

interface Props {
  grant: Grant
}

const STATUS_STYLES = {
  open: { bg: '#22c55e22', color: '#22c55e', label: 'Open' },
  rolling: { bg: '#8b5cf622', color: '#8b5cf6', label: 'Rolling' },
  closed: { bg: '#27272a', color: '#71717a', label: 'Closed' },
}

export default function GrantCard({ grant }: Props) {
  const status = STATUS_STYLES[grant.status || 'rolling']

  return (
    <div
      className="group flex flex-col h-full rounded-xl border p-5 transition-all hover:border-orange-500/50"
      style={{ background: 'var(--bg-card)', borderColor: 'var(--border)' }}
    >
      {/* Top row: source + status */}
      <div className="flex items-center justify-between mb-3">
        <span
          className="text-xs font-medium px-2 py-0.5 rounded-full"
          style={{ background: '#f9731622', color: '#f97316' }}
        >
          {grant.source}
        </span>
        <span
          className="text-xs font-medium px-2 py-0.5 rounded-full"
          style={{ background: status.bg, color: status.color }}
        >
          {status.label}
        </span>
      </div>

      {/* Title */}
      <h3
        className="font-semibold text-base leading-snug mb-1 group-hover:text-orange-400 transition-colors"
        style={{ color: 'var(--text-primary)' }}
      >
        {grant.title}
      </h3>

      {/* Organization */}
      <p className="text-xs mb-2" style={{ color: 'var(--text-muted)' }}>
        by {grant.organization}
      </p>

      {/* Amount */}
      {grant.amount && (
        <p className="text-sm font-semibold mb-2" style={{ color: '#f97316' }}>
          💰 {grant.amount}
        </p>
      )}

      {/* Description */}
      {grant.description && (
        <p
          className="text-xs mt-1 mb-3 line-clamp-3"
          style={{ color: 'var(--text-muted)' }}
        >
          {grant.description}
        </p>
      )}

      {/* Tags */}
      <div className="flex flex-wrap gap-1.5 mb-4 flex-1">
        {grant.tags.slice(0, 4).map(tag => (
          <span
            key={tag}
            className="text-xs px-2 py-0.5 rounded-md"
            style={{ background: '#27272a', color: 'var(--text-muted)' }}
          >
            {tag}
          </span>
        ))}
        {grant.tags.length > 4 && (
          <span
            className="text-xs px-2 py-0.5 rounded-md"
            style={{ background: '#27272a', color: 'var(--text-muted)' }}
          >
            +{grant.tags.length - 4}
          </span>
        )}
      </div>

      {/* Deadline */}
      {grant.deadline && (
        <p className="text-xs mb-2" style={{ color: 'var(--text-muted)' }}>
          ⏰ Deadline: {grant.deadline}
        </p>
      )}

      {/* CTA button */}
      <a
        href={grant.url}
        target="_blank"
        rel="noopener noreferrer"
        className="mt-auto w-full text-center text-sm font-medium py-2 rounded-lg transition-all"
        style={{
          background: '#f9731622',
          color: '#f97316',
          border: '1px solid #f9731633',
        }}
        onMouseEnter={e => {
          e.currentTarget.style.background = '#f9731633'
        }}
        onMouseLeave={e => {
          e.currentTarget.style.background = '#f9731622'
        }}
      >
        Apply →
      </a>
    </div>
  )
}
