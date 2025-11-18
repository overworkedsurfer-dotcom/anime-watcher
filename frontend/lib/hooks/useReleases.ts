/**
 * React Query hooks for fetching manga releases.
 */

import { useQuery } from '@tanstack/react-query'
import { api } from '@/lib/api/client'
import type { ReleaseListResponse, UpcomingReleasesResponse, MetadataFilters } from '@/lib/types/manga'

export function useCurrentReleases(params?: {
  limit?: number
  offset?: number
  publisher?: string
  region?: string
  format?: string
  sort?: string
}) {
  return useQuery<ReleaseListResponse>({
    queryKey: ['releases', 'current', params],
    queryFn: () => api.releases.getCurrent(params),
    staleTime: 5 * 60 * 1000, // 5 minutes
  })
}

export function useUpcomingReleases(params?: {
  months?: number
  publisher?: string
  region?: string
  format?: string
}) {
  return useQuery<UpcomingReleasesResponse>({
    queryKey: ['releases', 'upcoming', params],
    queryFn: () => api.releases.getUpcoming(params),
    staleTime: 30 * 60 * 1000, // 30 minutes
  })
}

export function useSearchReleases(params: {
  q: string
  limit?: number
  offset?: number
  date_from?: string
  date_to?: string
}) {
  return useQuery<ReleaseListResponse>({
    queryKey: ['releases', 'search', params],
    queryFn: () => api.releases.search(params),
    enabled: params.q.length > 0,
    staleTime: 5 * 60 * 1000, // 5 minutes
  })
}

export function useMetadataFilters() {
  return useQuery<MetadataFilters>({
    queryKey: ['metadata', 'filters'],
    queryFn: () => api.metadata.getFilters(),
    staleTime: 60 * 60 * 1000, // 1 hour
  })
}
