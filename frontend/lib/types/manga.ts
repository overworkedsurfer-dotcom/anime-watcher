/**
 * Type definitions for manga releases and related entities.
 */

export interface Publisher {
  id: number
  name: string
  slug: string
  country?: string
}

export interface MangaRelease {
  id: number
  title: string
  series_name?: string
  volume_number?: string
  isbn_13?: string
  isbn_10?: string
  release_date: string
  publisher: Publisher
  format?: string
  page_count?: number
  price_usd?: number
  price_gbp?: number
  cover_image_url?: string
  description?: string
  demographic?: string
  genres: string[]
  regions: string[]
  authors: string[]
  illustrators: string[]
}

export interface PaginationMeta {
  total: number
  limit: number
  offset: number
  month?: string
  query?: string
}

export interface ReleaseListResponse {
  data: MangaRelease[]
  meta: PaginationMeta
}

export interface UpcomingReleasesResponse {
  data: Record<string, MangaRelease[]>
  meta: {
    total: number
    months_covered: string[]
  }
}

export interface PublisherFilter {
  id: number
  name: string
  slug: string
  release_count: number
}

export interface MetadataFilters {
  publishers: PublisherFilter[]
  regions: string[]
  formats: string[]
  demographics: string[]
  genres: string[]
}
