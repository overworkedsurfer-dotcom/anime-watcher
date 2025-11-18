/**
 * API client for the Manga Release Radar backend.
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export class APIError extends Error {
  constructor(public status: number, message: string) {
    super(message)
    this.name = 'APIError'
  }
}

async function fetchAPI<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`

  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    })

    if (!response.ok) {
      throw new APIError(response.status, `API request failed: ${response.statusText}`)
    }

    return response.json()
  } catch (error) {
    if (error instanceof APIError) {
      throw error
    }
    throw new Error(`Network error: ${error}`)
  }
}

export const api = {
  releases: {
    getCurrent: (params?: {
      limit?: number
      offset?: number
      publisher?: string
      region?: string
      format?: string
      sort?: string
    }) => {
      const queryParams = new URLSearchParams()
      if (params) {
        Object.entries(params).forEach(([key, value]) => {
          if (value !== undefined) {
            queryParams.append(key, String(value))
          }
        })
      }
      return fetchAPI(`/api/v1/releases/current?${queryParams}`)
    },

    getUpcoming: (params?: {
      months?: number
      publisher?: string
      region?: string
      format?: string
    }) => {
      const queryParams = new URLSearchParams()
      if (params) {
        Object.entries(params).forEach(([key, value]) => {
          if (value !== undefined) {
            queryParams.append(key, String(value))
          }
        })
      }
      return fetchAPI(`/api/v1/releases/upcoming?${queryParams}`)
    },

    search: (params: {
      q: string
      limit?: number
      offset?: number
      date_from?: string
      date_to?: string
    }) => {
      const queryParams = new URLSearchParams()
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          queryParams.append(key, String(value))
        }
      })
      return fetchAPI(`/api/v1/releases/search?${queryParams}`)
    },
  },

  publishers: {
    getAll: () => fetchAPI('/api/v1/publishers'),
  },

  metadata: {
    getFilters: () => fetchAPI('/api/v1/metadata/filters'),
  },

  health: () => fetchAPI('/health'),
}
