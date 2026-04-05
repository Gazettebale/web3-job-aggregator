'use client'
import { BugBounty } from '@/lib/types'

interface Props {
  bounty: BugBounty
}

const SOURCE_COLORS: Record<string, string> = {
  Immunefi: '#22c55e',
  Code4rena: '#f97316',
  Sherlock: '#8b5cf6',
}

export default function BountyCard({ bounty }: Props) {
  const sourceColor = SOURCE_COLORS[bounty.source] || '#22c55e'

  return (
    <div
      className="group flex flex-col h-full rounded-xl border p-5 transition-all hover:border-green-500/50"
      style={{ background: 'var(--bg-card)', borderColor: 'var(--border)' }}
    >
      {/* Top row: source + max reward */}
      <div className="flex items-center justify-between mb-3">
        <span
          className="text-xs font-medium px-2 py-0.5 rounded-full"
          style={{ background: sourceColor + '22', color: sourceColor }}
        >
          {bounty.source}
        </span>
        {bounty.maxReward && (
          <span className="text-sm font-bold" style={{ color: '#22c55e' }}>
            {bounty.maxReward}
          </span>
        )}
      </div>

      {/* Title */}
      <h3
        className="font-semibold text-base leading-snug mb-2 group-hover:text-green-400 transition-colors"
        style={{ color: 'var(--text-primary)' }}
      >
        {bounty.title}
      </h3>

      {/* Reward range */}
      {bounty.maxReward && (
        <p className="text-xs mb-3" style={{ color: 'var(--text-muted)' }}>
          Max reward:{' '}
          <span className="font-semibold" style={{ color: '#22c55e' }}>
            {bounty.maxReward}
          </span>
          {bounty.minReward && ` · Min: ${bounty.minReward}`}
        </p>
      )}

      {/* Asset types */}
      {bounty.assets && bounty.assets.length > 0 && (
        <div className="flex flex-wrap gap-1.5 mb-3">
          {bounty.assets.slice(0, 3).map(asset => (
            <span
              key={asset}
              className="text-xs px-2 py-0.5 rounded-md"
              style={{
                background: '#22c55e11',
                color: '#22c55e',
                border: '1px solid #22c55e22',
              }}
            >
              {asset}
            </span>
          ))}
        </div>
      )}

      {/* Ecosystem tags */}
      <div className="flex flex-wrap gap-1.5 mb-4 flex-1">
        {bounty.tags.slice(0, 4).map(tag => (
          <span
            key={tag}
            className="text-xs px-2 py-0.5 rounded-md"
            style={{ background: '#27272a', color: 'var(--text-muted)' }}
          >
            {tag}
          </span>
        ))}
        {bounty.tags.length > 4 && (
          <span
            className="text-xs px-2 py-0.5 rounded-md"
            style={{ background: '#27272a', color: 'var(--text-muted)' }}
          >
            +{bounty.tags.length - 4}
          </span>
        )}
      </div>

      {/* CTA button */}
      <a
        href={bounty.url}
        target="_blank"
        rel="noopener noreferrer"
        className="mt-auto w-full text-center text-sm font-medium py-2 rounded-lg transition-all"
        style={{
          background: '#22c55e22',
          color: '#22c55e',
          border: '1px solid #22c55e33',
        }}
        onMouseEnter={e => {
          e.currentTarget.style.background = '#22c55e33'
        }}
        onMouseLeave={e => {
          e.currentTarget.style.background = '#22c55e22'
        }}
      >
        View Bounty →
      </a>
    </div>
  )
}
