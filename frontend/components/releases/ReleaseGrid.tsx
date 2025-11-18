/**
 * Grid layout for displaying manga releases.
 */

import type { MangaRelease } from '@/lib/types/manga'
import { ReleaseCard } from './ReleaseCard'

interface ReleaseGridProps {
  releases: MangaRelease[]
  isLoading?: boolean
}

export function ReleaseGrid({ releases, isLoading }: ReleaseGridProps) {
  if (isLoading) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {Array.from({ length: 8 }).map((_, i) => (
          <div key={i} className="animate-pulse">
            <div className="bg-muted rounded-lg h-[400px]" />
          </div>
        ))}
      </div>
    )
  }

  if (releases.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-6xl mb-4">📚</div>
        <h3 className="text-xl font-semibold mb-2">No releases found</h3>
        <p className="text-muted-foreground">
          Try adjusting your filters or check back later for new releases.
        </p>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      {releases.map((release) => (
        <ReleaseCard key={release.id} release={release} />
      ))}
    </div>
  )
}
