/**
 * Home page - Current month releases.
 */

'use client'

import { useState } from 'react'
import { useCurrentReleases } from '@/lib/hooks/useReleases'
import { ReleaseGrid } from '@/components/releases/ReleaseGrid'
import { SearchBar } from '@/components/filters/SearchBar'
import { formatMonthYear } from '@/lib/utils/format'

export default function HomePage() {
  const [searchQuery, setSearchQuery] = useState('')
  const { data, isLoading, error } = useCurrentReleases()

  // Filter releases based on search query
  const filteredReleases = data?.data.filter((release) => {
    if (!searchQuery) return true
    const query = searchQuery.toLowerCase()
    return (
      release.title.toLowerCase().includes(query) ||
      release.series_name?.toLowerCase().includes(query) ||
      release.publisher.name.toLowerCase().includes(query)
    )
  }) || []

  const currentMonth = data?.meta.month ? formatMonthYear(data.meta.month) : ''

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-6xl mb-4">⚠️</div>
        <h3 className="text-xl font-semibold mb-2">Oops! Something went wrong</h3>
        <p className="text-muted-foreground">
          We couldn&apos;t load the releases. Please try again later.
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="bg-gradient-to-r from-pastel-pink/30 via-pastel-purple/30 to-pastel-blue/30 rounded-2xl p-8 text-center">
        <h1 className="text-4xl font-bold mb-2">
          {currentMonth || 'Current Month'} Releases
        </h1>
        <p className="text-lg text-muted-foreground">
          Discover the latest manga hitting shelves this month!
        </p>
      </div>

      {/* Search */}
      <div className="max-w-2xl mx-auto">
        <SearchBar
          value={searchQuery}
          onChange={setSearchQuery}
          placeholder="Search by title, series, or publisher..."
        />
      </div>

      {/* Release Count */}
      {!isLoading && (
        <div className="flex items-center justify-between">
          <p className="text-sm text-muted-foreground">
            Showing {filteredReleases.length} of {data?.meta.total || 0} releases
          </p>
        </div>
      )}

      {/* Releases Grid */}
      <ReleaseGrid releases={filteredReleases} isLoading={isLoading} />
    </div>
  )
}
