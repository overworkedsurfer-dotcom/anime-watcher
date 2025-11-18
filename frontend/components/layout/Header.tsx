/**
 * Main header component with navigation.
 */

'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { cn } from '@/lib/utils/cn'
import { BookOpen } from 'lucide-react'

export function Header() {
  const pathname = usePathname()

  const navItems = [
    { href: '/', label: 'Current' },
    { href: '/upcoming', label: 'Upcoming' },
    { href: '/search', label: 'Search' },
  ]

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto px-4">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 font-bold text-xl">
            <div className="bg-gradient-to-br from-primary-500 to-primary-700 p-2 rounded-lg">
              <BookOpen className="w-6 h-6 text-white" />
            </div>
            <span className="hidden sm:inline bg-gradient-to-r from-primary-600 to-primary-800 bg-clip-text text-transparent">
              Manga Release Radar
            </span>
            <span className="sm:hidden bg-gradient-to-r from-primary-600 to-primary-800 bg-clip-text text-transparent">
              MRR
            </span>
          </Link>

          {/* Navigation */}
          <nav className="flex items-center gap-1">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  'px-4 py-2 rounded-md font-medium text-sm transition-colors',
                  pathname === item.href
                    ? 'bg-primary text-primary-foreground'
                    : 'text-muted-foreground hover:text-foreground hover:bg-muted'
                )}
              >
                {item.label}
              </Link>
            ))}
          </nav>
        </div>
      </div>
    </header>
  )
}
