/**
 * Upcoming releases page.
 */

'use client'

import { useState } from 'react'
import { useUpcomingReleases } from '@/lib/hooks/useReleases'
import { ReleaseGrid } from '@/components/releases/ReleaseGrid'
import { formatMonthYear } from '@/lib/utils/format'
import { Button } from '@/components/ui/button'
import { ChevronDown, ChevronUp } from 'lucide-react'

export default function UpcomingPage() {
  const { data, isLoading, error } = useUpcomingReleases({ months: 3 })
  const [expandedMonths, setExpandedMonths] = useState<Record<string, boolean>>({})

  const toggleMonth = (month: string) => {
    setExpandedMonths((prev) => ({
      ...prev,
      [month]: !prev[month],
    }))
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-6xl mb-4">⚠️</div>
        <h3 className="text-xl font-semibold mb-2">Oops! Something went wrong</h3>
        <p className="text-muted-foreground">
          We couldn&apos;t load the upcoming releases. Please try again later.
        </p>
      </div>
    )
  }

  if (isLoading) {
    return (
      <div className="space-y-8">
        <div className="bg-gradient-to-r from-pastel-purple/30 to-pastel-blue/30 rounded-2xl p-8 text-center">
          <h1 className="text-4xl font-bold mb-2">Upcoming Releases</h1>
          <p className="text-lg text-muted-foreground">Loading...</p>
        </div>
        <ReleaseGrid releases={[]} isLoading={true} />
      </div>
    )
  }

  const months = Object.keys(data?.data || {})

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="bg-gradient-to-r from-pastel-purple/30 to-pastel-blue/30 rounded-2xl p-8 text-center">
        <h1 className="text-4xl font-bold mb-2">🔮 Upcoming Releases</h1>
        <p className="text-lg text-muted-foreground">
          Plan your manga purchases for the next few months
        </p>
      </div>

      {/* Monthly Sections */}
      {months.map((month, index) => {
        const releases = data?.data[month] || []
        const isExpanded = expandedMonths[month] !== false // Default to expanded for first month

        return (
          <div key={month} className="space-y-4">
            {/* Month Header */}
            <div
              className="flex items-center justify-between p-4 bg-gradient-to-r from-pastel-pink/20 to-pastel-purple/20 rounded-xl cursor-pointer hover:from-pastel-pink/30 hover:to-pastel-purple/30 transition-colors"
              onClick={() => toggleMonth(month)}
            >
              <div>
                <h2 className="text-2xl font-bold">{formatMonthYear(month)}</h2>
                <p className="text-sm text-muted-foreground">{releases.length} releases</p>
              </div>
              <Button variant="ghost" size="sm">
                {isExpanded ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
              </Button>
            </div>

            {/* Releases */}
            {isExpanded && <ReleaseGrid releases={releases} />}
          </div>
        )
      })}
    </div>
  )
}
