/**
 * Formatting utilities.
 */

import { format, parseISO } from 'date-fns'

export function formatDate(dateString: string): string {
  try {
    const date = parseISO(dateString)
    return format(date, 'MMM d, yyyy')
  } catch {
    return dateString
  }
}

export function formatPrice(price: number | undefined, currency: 'USD' | 'GBP' = 'USD'): string {
  if (!price) return 'N/A'

  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(price)
}

export function formatMonthYear(monthString: string): string {
  try {
    const [year, month] = monthString.split('-')
    const date = new Date(parseInt(year), parseInt(month) - 1, 1)
    return format(date, 'MMMM yyyy')
  } catch {
    return monthString
  }
}
