/**
 * Search page.
 */

'use client'

import { useState } from 'react'
import { useSearchReleases } from '@/lib/hooks/useReleases'
import { ReleaseGrid } from '@/components/releases/ReleaseGrid'
import { SearchBar } from '@/components/filters/SearchBar'

export default function SearchPage() {
  const [query, setQuery] = useState('')
  const { data, isLoading } = useSearchReleases({ q: query })

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="bg-gradient-to-r from-pastel-blue/30 to-pastel-green/30 rounded-2xl p-8 text-center">
        <h1 className="text-4xl font-bold mb-2">🔍 Search Manga Releases</h1>
        <p className="text-lg text-muted-foreground">
          Find manga by title, series, or author
        </p>
      </div>

      {/* Search */}
      <div className="max-w-2xl mx-auto">
        <SearchBar
          value={query}
          onChange={setQuery}
          placeholder="Search by title, series, or author..."
        />
      </div>

      {/* Results */}
      {query.length > 0 && !isLoading && (
        <div className="flex items-center justify-between">
          <p className="text-sm text-muted-foreground">
            {data?.meta.total || 0} results for &quot;{query}&quot;
          </p>
        </div>
      )}

      {query.length === 0 ? (
        <div className="text-center py-12">
          <div className="text-6xl mb-4">🔍</div>
          <h3 className="text-xl font-semibold mb-2">Start searching</h3>
          <p className="text-muted-foreground">
            Enter a manga title, series name, or author to find releases
          </p>
        </div>
      ) : (
        <ReleaseGrid releases={data?.data || []} isLoading={isLoading} />
      )}
    </div>
  )
}
