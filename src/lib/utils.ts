export function generateId(str: string): string {
  return str.toLowerCase().replace(/[^a-z0-9]/g, '-').substring(0, 50)
}

export function normalizeText(str: string | null | undefined): string {
  if (!str) return ''
  return str.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '')
}

// Smart word-boundary filtering (no false positives)
export function matchesFilter(text: string, keyword: string): boolean {
  const normalized = normalizeText(text)
  const kw = normalizeText(keyword)
  // Word boundary check using regex
  const regex = new RegExp(`(^|[^a-z0-9])${kw.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}([^a-z0-9]|$)`)
  return regex.test(normalized)
}

export function filterItems<T extends { title: string; tags: string[] }>(
  items: T[],
  search: string,
  tags: string[]
): T[] {
  if (!Array.isArray(items)) return []
  return items.filter(item => {
    if (!item) return false
    const itemTags = Array.isArray(item.tags) ? item.tags.filter(Boolean) : []
    const searchMatch = !search ||
      normalizeText(item.title).includes(normalizeText(search)) ||
      itemTags.some(tag => normalizeText(tag).includes(normalizeText(search)))

    const tagMatch = tags.length === 0 ||
      tags.every(tag => itemTags.some(t => matchesFilter(t, tag)))

    return searchMatch && tagMatch
  })
}

export function timeAgo(date: string): string {
  const now = new Date()
  const then = new Date(date)
  const seconds = Math.floor((now.getTime() - then.getTime()) / 1000)
  if (seconds < 60) return 'just now'
  const minutes = Math.floor(seconds / 60)
  if (minutes < 60) return `${minutes}m ago`
  const hours = Math.floor(minutes / 60)
  if (hours < 24) return `${hours}h ago`
  const days = Math.floor(hours / 24)
  if (days < 30) return `${days}d ago`
  return then.toLocaleDateString()
}

export function formatDate(date: string): string {
  return new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}
