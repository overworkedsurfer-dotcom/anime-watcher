/**
 * Card component for displaying a manga release.
 */

import Image from 'next/image'
import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import type { MangaRelease } from '@/lib/types/manga'
import { formatDate, formatPrice } from '@/lib/utils/format'
import { Calendar, DollarSign } from 'lucide-react'

interface ReleaseCardProps {
  release: MangaRelease
}

export function ReleaseCard({ release }: ReleaseCardProps) {
  return (
    <Card className="group overflow-hidden transition-all duration-200 hover:shadow-xl hover:-translate-y-1 hover:border-primary-300">
      <CardContent className="p-4">
        {/* Cover Image */}
        <div className="relative aspect-[2/3] mb-3 rounded-lg overflow-hidden bg-muted">
          {release.cover_image_url ? (
            <Image
              src={release.cover_image_url}
              alt={release.title}
              fill
              className="object-cover transition-transform duration-200 group-hover:scale-105"
              sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-muted-foreground">
              No Image
            </div>
          )}
        </div>

        {/* Title */}
        <h3 className="font-bold text-lg line-clamp-2 mb-2 min-h-[3.5rem]">
          {release.title}
        </h3>

        {/* Publisher */}
        <div className="flex items-center gap-2 mb-2">
          <Badge variant="pastel" className="rounded-full text-xs">
            {release.publisher.name}
          </Badge>
        </div>

        {/* Release Date & Price */}
        <div className="flex items-center justify-between text-sm text-muted-foreground mb-3">
          <div className="flex items-center gap-1">
            <Calendar className="w-4 h-4" />
            <span>{formatDate(release.release_date)}</span>
          </div>
          {release.price_usd && (
            <div className="flex items-center gap-1 font-semibold text-foreground">
              <DollarSign className="w-4 h-4" />
              <span>{formatPrice(release.price_usd)}</span>
            </div>
          )}
        </div>

        {/* Genres */}
        {release.genres && release.genres.length > 0 && (
          <div className="flex flex-wrap gap-1">
            {release.genres.slice(0, 3).map((genre) => (
              <Badge key={genre} variant="outline" className="text-xs">
                {genre}
              </Badge>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  )
}
