# Manga Release Radar - UI/UX Design Guide

**Version:** 1.0
**Design Philosophy:** Cute, Cozy, and Approachable

---

## 1. Visual Design Principles

### 1.1 Color Palette

```css
/* Pastel Primary Colors */
--pastel-pink: #ffc4dd;
--pastel-purple: #d4a5ff;
--pastel-blue: #a8d8ff;
--pastel-green: #b8f0d0;
--pastel-yellow: #fff3b8;
--pastel-orange: #ffd4a3;

/* Accent Colors */
--primary-500: #e750f4;    /* Vibrant purple for CTAs */
--primary-600: #c729d6;
--secondary-500: #a8d8ff;  /* Soft blue for info */

/* Neutrals (Warm) */
--neutral-50: #fafafa;     /* Background */
--neutral-100: #f5f5f5;    /* Card background */
--neutral-200: #e5e5e5;    /* Borders */
--neutral-700: #404040;    /* Body text */
--neutral-900: #171717;    /* Headings */

/* Semantic Colors */
--success: #86efac;        /* Green */
--warning: #fcd34d;        /* Yellow */
--error: #fca5a5;          /* Red */
--info: #a8d8ff;           /* Blue */
```

### 1.2 Typography

```css
/* Font Stack */
font-family:
  'Inter',
  -apple-system,
  BlinkMacSystemFont,
  'Segoe UI',
  Roboto,
  'Helvetica Neue',
  sans-serif;

/* Headings (Rounded) */
font-family-headings:
  'Nunito',
  'Poppins',
  'Quicksand',
  sans-serif;

/* Type Scale */
--text-xs: 0.75rem;     /* 12px */
--text-sm: 0.875rem;    /* 14px */
--text-base: 1rem;      /* 16px */
--text-lg: 1.125rem;    /* 18px */
--text-xl: 1.25rem;     /* 20px */
--text-2xl: 1.5rem;     /* 24px */
--text-3xl: 1.875rem;   /* 30px */
--text-4xl: 2.25rem;    /* 36px */

/* Line Heights */
--leading-tight: 1.25;
--leading-normal: 1.5;
--leading-relaxed: 1.75;
```

### 1.3 Spacing System

```css
/* 4px base unit */
--space-1: 0.25rem;    /* 4px */
--space-2: 0.5rem;     /* 8px */
--space-3: 0.75rem;    /* 12px */
--space-4: 1rem;       /* 16px */
--space-6: 1.5rem;     /* 24px */
--space-8: 2rem;       /* 32px */
--space-12: 3rem;      /* 48px */
--space-16: 4rem;      /* 64px */
```

### 1.4 Border Radius

```css
/* Rounded corners everywhere! */
--radius-sm: 0.5rem;    /* 8px - Badges, tags */
--radius-md: 0.75rem;   /* 12px - Buttons, inputs */
--radius-lg: 1rem;      /* 16px - Cards */
--radius-xl: 1.5rem;    /* 24px - Containers */
--radius-2xl: 2rem;     /* 32px - Hero sections */
--radius-full: 9999px;  /* Pills */
```

### 1.5 Shadows

```css
/* Soft, layered shadows */
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow-md:
  0 4px 6px -1px rgba(0, 0, 0, 0.1),
  0 2px 4px -1px rgba(0, 0, 0, 0.06);
--shadow-lg:
  0 10px 15px -3px rgba(0, 0, 0, 0.1),
  0 4px 6px -2px rgba(0, 0, 0, 0.05);
--shadow-xl:
  0 20px 25px -5px rgba(0, 0, 0, 0.1),
  0 10px 10px -5px rgba(0, 0, 0, 0.04);

/* Colored shadows for hover states */
--shadow-primary: 0 8px 20px rgba(231, 80, 244, 0.25);
--shadow-pastel: 0 8px 20px rgba(255, 196, 221, 0.3);
```

---

## 2. Component Library

### 2.1 ReleaseCard

**Visual Description:**
```
┌─────────────────────────────────┐
│  ┌─────────────────────┐        │
│  │                     │        │
│  │   [Cover Image]     │        │
│  │    160x240px        │        │
│  │                     │        │
│  └─────────────────────┘        │
│                                  │
│  Chainsaw Man, Vol. 15          │ <- Title (bold)
│  🏷️ VIZ Media                    │ <- Publisher (badge)
│  📅 Nov 5, 2025                  │ <- Date
│  💵 $11.99                       │ <- Price
│                                  │
│  [Action] [Horror] [Shonen]     │ <- Genre tags
└─────────────────────────────────┘
   ↑
   Hover: Scale 1.02, lift shadow
```

**Styling:**
- Background: `--neutral-100` (warm white)
- Border: 1px solid `--neutral-200`
- Border radius: `--radius-lg` (1rem)
- Padding: `--space-4` (1rem)
- Shadow: `--shadow-md`
- Hover shadow: `--shadow-xl` + `--shadow-pastel`
- Transition: all 200ms ease-in-out

**Responsive:**
- Mobile: Full width, smaller image (120x180px)
- Tablet: 2-column grid
- Desktop: 3-4 column grid

### 2.2 FilterBar

**Visual Description:**
```
┌─────────────────────────────────────────────────────────┐
│  🔍 [Search manga titles...]                             │
│                                                          │
│  Publisher: [All ▼]  Region: [US] [UK] [CA] [AU]      │
│  Format: [All ▼]     Sort: [Date ▼]                    │
│                                                          │
│  Active Filters: [VIZ Media ✕] [Paperback ✕]  Clear   │
└─────────────────────────────────────────────────────────┘
```

**Styling:**
- Background: `--pastel-purple` (very light, 10% opacity)
- Border radius: `--radius-xl`
- Padding: `--space-6`
- Sticky position on scroll
- Collapse to accordion on mobile

**Interactive Elements:**
- Dropdowns: shadcn/ui Select component
- Toggle buttons: Active state with `--primary-500` background
- Tags: Removable with ✕ icon, `--radius-full`

### 2.3 MonthSection

**Visual Description:**
```
┌─────────────────────────────────────────────────────────┐
│  ┌─────────────────────────────────────────────────┐   │
│  │  📅 November 2025 · 87 releases                  │   │
│  └─────────────────────────────────────────────────┘   │
│                                                          │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐          │
│  │ Release 1 │  │ Release 2 │  │ Release 3 │   ...    │
│  └───────────┘  └───────────┘  └───────────┘          │
│                                                          │
│  [Load More] or infinite scroll                         │
└─────────────────────────────────────────────────────────┘
```

**Styling:**
- Month header: Gradient background `--pastel-pink` to `--pastel-purple`
- Header text: `--text-2xl`, bold
- Count: `--text-lg`, lighter weight
- Grid gap: `--space-6`

### 2.4 Navigation Header

**Visual Description:**
```
┌─────────────────────────────────────────────────────────┐
│  📚 Manga Release Radar    [Current] [Upcoming] [Search]│
└─────────────────────────────────────────────────────────┘
   ↑ Logo + Title              ↑ Navigation links
```

**Mobile Navigation:**
```
┌─────────────────────────────────────────────────────────┐
│  📚 MRR                                     ☰           │
└─────────────────────────────────────────────────────────┘
   ↑ Logo                                    ↑ Hamburger

[When hamburger clicked]
┌─────────────────────────────────────────────────────────┐
│  ✕                                                      │
│                                                          │
│  Current Releases                                       │
│  Upcoming Releases                                      │
│  Search                                                 │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

**Styling:**
- Background: `--neutral-50` with subtle shadow
- Height: 64px (desktop), 56px (mobile)
- Logo: Custom icon or emoji 📚
- Links: Underline animation on hover
- Active link: `--primary-500` color + bottom border

### 2.5 Buttons

**Primary Button:**
```css
background: linear-gradient(135deg, #e750f4, #c729d6);
color: white;
padding: 0.75rem 1.5rem;
border-radius: var(--radius-md);
font-weight: 600;
box-shadow: var(--shadow-primary);
transition: all 200ms;

&:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-primary-lg);
}

&:active {
  transform: translateY(0);
}
```

**Secondary Button:**
```css
background: white;
color: var(--primary-600);
border: 2px solid var(--primary-500);
/* Same padding, radius, transitions */
```

**Ghost Button:**
```css
background: transparent;
color: var(--neutral-700);
&:hover {
  background: var(--neutral-100);
}
```

### 2.6 Tags/Badges

**Genre Tag:**
```css
background: var(--pastel-purple);
color: var(--neutral-900);
padding: 0.25rem 0.75rem;
border-radius: var(--radius-full);
font-size: var(--text-sm);
font-weight: 500;
```

**Publisher Badge:**
```css
background: var(--pastel-pink);
/* Same styling as genre tag */
display: inline-flex;
align-items: center;
gap: 0.25rem;
```

**Status Badge (New Release):**
```css
background: var(--success);
color: var(--neutral-900);
/* Animated pulse effect */
animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
```

---

## 3. Page Layouts

### 3.1 Home Page (`/`)

**Desktop Layout:**
```
┌─────────────────────────────────────────────────────────┐
│                    [Header/Nav]                          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │  🎉 November 2025 Releases                      │   │
│  │  Discover the latest manga hitting shelves!     │   │
│  └─────────────────────────────────────────────────┘   │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  [Filter Bar with search & filters]             │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐          │
│  │ Release 1 │  │ Release 2 │  │ Release 3 │   ...    │
│  └───────────┘  └───────────┘  └───────────┘          │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐          │
│  │ Release 4 │  │ Release 5 │  │ Release 6 │   ...    │
│  └───────────┘  └───────────┘  └───────────┘          │
│                                                          │
│  [Load More] or [Infinite Scroll]                      │
│                                                          │
└─────────────────────────────────────────────────────────┘
│                    [Footer]                              │
└─────────────────────────────────────────────────────────┘
```

**Mobile Layout:**
```
┌─────────────────┐
│   [Header/Nav]   │
├─────────────────┤
│                  │
│  November 2025  │
│  Releases 🎉     │
│                  │
│  [Search 🔍]     │
│  [Filters ▼]     │
│                  │
│  ┌────────────┐ │
│  │ Release 1  │ │
│  └────────────┘ │
│  ┌────────────┐ │
│  │ Release 2  │ │
│  └────────────┘ │
│  ┌────────────┐ │
│  │ Release 3  │ │
│  └────────────┘ │
│       ...        │
│                  │
│   [Load More]    │
│                  │
│    [Footer]      │
└─────────────────┘
```

### 3.2 Upcoming Page (`/upcoming`)

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│                    [Header/Nav]                          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  🔮 Upcoming Releases                                   │
│  Plan your manga purchases for the next few months      │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  [Filter Bar]                                   │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │  📅 December 2025 · 94 releases      [Expand ▼] │   │
│  ├─────────────────────────────────────────────────┤   │
│  │  ┌───────┐  ┌───────┐  ┌───────┐               │   │
│  │  │ Rel 1 │  │ Rel 2 │  │ Rel 3 │  ...          │   │
│  │  └───────┘  └───────┘  └───────┘               │   │
│  └─────────────────────────────────────────────────┘   │
│                                                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │  📅 January 2026 · 78 releases      [Expand ▼]  │   │
│  │  [Collapsed - click to expand]                  │   │
│  └─────────────────────────────────────────────────┘   │
│                                                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │  📅 February 2026 · 82 releases     [Expand ▼]  │   │
│  │  [Collapsed - click to expand]                  │   │
│  └─────────────────────────────────────────────────┘   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

**Interaction:**
- Month sections start expanded for first month, collapsed for others
- Smooth accordion animation (300ms)
- Retain scroll position on expand/collapse

### 3.3 Search Page (`/search`)

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│                    [Header/Nav]                          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  🔍 Search Manga Releases                               │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  🔍 Search by title, series, or author...        │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
│  Date Range: [From: ___] [To: ___]                     │
│  Publisher: [All ▼]  Region: [All ▼]                   │
│                                                          │
│  Showing 12 results for "chainsaw man"                  │
│                                                          │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐          │
│  │ Result 1  │  │ Result 2  │  │ Result 3  │   ...    │
│  └───────────┘  └───────────┘  └───────────┘          │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

**Search Features:**
- Debounced input (300ms)
- Search-as-you-type
- Highlight matching terms in results
- No results state with illustration

---

## 4. Micro-Interactions & Animations

### 4.1 Card Hover
```css
.release-card {
  transition: all 200ms cubic-bezier(0.4, 0, 0.2, 1);
}

.release-card:hover {
  transform: translateY(-4px) scale(1.02);
  box-shadow: var(--shadow-xl), var(--shadow-pastel);
  border-color: var(--primary-400);
}
```

### 4.2 Filter Application
- Fade out current results (200ms)
- Show loading skeleton
- Fade in new results (300ms)
- Subtle "pop" animation on each card (stagger 50ms)

### 4.3 Page Transitions
```tsx
// Framer Motion example
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  exit={{ opacity: 0, y: -20 }}
  transition={{ duration: 0.3 }}
>
  {children}
</motion.div>
```

### 4.4 Loading States
- Skeleton screens matching card layout
- Shimmer effect (gradient animation)
- Smooth transition to real content

### 4.5 Error States
- Shake animation for form errors
- Bounce animation for "retry" buttons
- Toast notifications with slide-in from top

### 4.6 Success States
- Checkmark animation (draw path)
- Confetti effect for milestones
- Toast notifications with slide-in

---

## 5. Responsive Breakpoints

```css
/* Mobile-first approach */

/* Extra small devices (phones, 320px and up) */
@media (min-width: 320px) {
  /* Base styles - single column */
}

/* Small devices (landscape phones, 576px and up) */
@media (min-width: 576px) {
  /* Slightly larger cards, 2-column where appropriate */
}

/* Medium devices (tablets, 768px and up) */
@media (min-width: 768px) {
  /* 2-3 column grids, side-by-side filters */
}

/* Large devices (desktops, 1024px and up) */
@media (min-width: 1024px) {
  /* 3-4 column grids, sticky filters */
}

/* Extra large devices (large desktops, 1280px and up) */
@media (min-width: 1280px) {
  /* Max-width container, centered */
  max-width: 1280px;
  margin: 0 auto;
}
```

---

## 6. Accessibility

### 6.1 Keyboard Navigation
- All interactive elements focusable
- Visible focus indicators (ring with `--primary-500`)
- Skip to content link
- Arrow keys for carousels/accordions

### 6.2 Screen Readers
- Semantic HTML (`<main>`, `<nav>`, `<article>`)
- ARIA labels for interactive elements
- Alt text for all images
- Live regions for dynamic content

### 6.3 Color Contrast
- All text meets WCAG AA standards (4.5:1 for normal, 3:1 for large)
- Focus indicators visible (3:1 contrast minimum)
- Don't rely solely on color for information

### 6.4 Motion Preferences
```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 7. Empty & Error States

### 7.1 No Results (Search)
```
┌─────────────────────────────────────┐
│                                      │
│         🔍                           │
│    No results found                  │
│                                      │
│    Try adjusting your filters or    │
│    search terms                      │
│                                      │
│    [Clear Filters]                   │
│                                      │
└─────────────────────────────────────┘
```

### 7.2 No Releases This Month
```
┌─────────────────────────────────────┐
│                                      │
│         📚                           │
│    No releases this month            │
│                                      │
│    Check upcoming releases to see   │
│    what's coming soon!               │
│                                      │
│    [View Upcoming]                   │
│                                      │
└─────────────────────────────────────┘
```

### 7.3 Error Loading Data
```
┌─────────────────────────────────────┐
│                                      │
│         ⚠️                            │
│    Oops! Something went wrong        │
│                                      │
│    We couldn't load the releases.   │
│    Please try again.                 │
│                                      │
│    [Retry]                           │
│                                      │
└─────────────────────────────────────┘
```

---

## 8. Dark Mode (Optional Feature)

### 8.1 Dark Mode Palette
```css
/* Dark mode overrides */
@media (prefers-color-scheme: dark) {
  :root {
    --neutral-50: #18181b;     /* Background */
    --neutral-100: #27272a;    /* Card background */
    --neutral-200: #3f3f46;    /* Borders */
    --neutral-700: #d4d4d8;    /* Body text */
    --neutral-900: #fafafa;    /* Headings */

    /* Adjust pastel colors for dark mode */
    --pastel-pink: #c084fc;
    --pastel-purple: #a78bfa;
    --pastel-blue: #60a5fa;
    /* ... etc */
  }
}
```

### 8.2 Toggle Switch
- Moon/sun icon
- Smooth transition between modes (200ms)
- Persist preference in localStorage

---

## 9. Performance Guidelines

### 9.1 Images
- Use WebP with JPEG fallback
- Lazy load below the fold
- Blur placeholder while loading
- Responsive images with `srcset`

### 9.2 Fonts
- System font stack for body
- Preload custom fonts for headings
- Font-display: swap

### 9.3 Code Splitting
- Route-based code splitting
- Dynamic imports for heavy components
- Tree-shaking unused code

---

## 10. Component Examples (React/TSX)

### 10.1 ReleaseCard Component

```tsx
interface ReleaseCardProps {
  release: MangaRelease;
  variant?: 'default' | 'compact';
}

export function ReleaseCard({ release, variant = 'default' }: ReleaseCardProps) {
  return (
    <Card className="group hover:shadow-xl hover:-translate-y-1 transition-all duration-200">
      <CardContent className="p-4">
        <div className="aspect-[2/3] relative rounded-lg overflow-hidden mb-3">
          <Image
            src={release.cover_image_url}
            alt={release.title}
            fill
            className="object-cover"
            sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
          />
        </div>

        <h3 className="font-bold text-lg line-clamp-2 mb-2">
          {release.title}
        </h3>

        <div className="flex items-center gap-2 mb-2">
          <Badge variant="secondary" className="rounded-full">
            {release.publisher.name}
          </Badge>
        </div>

        <div className="flex items-center justify-between text-sm text-neutral-600">
          <span>📅 {formatDate(release.release_date)}</span>
          <span className="font-semibold">💵 ${release.price_usd}</span>
        </div>

        <div className="flex flex-wrap gap-1 mt-3">
          {release.genres.slice(0, 3).map((genre) => (
            <Badge key={genre} variant="outline" className="text-xs">
              {genre}
            </Badge>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
```

### 10.2 FilterBar Component

```tsx
export function FilterBar() {
  const { data: filters } = useFilters();
  const [searchQuery, setSearchQuery] = useState('');

  return (
    <div className="bg-pastel-purple/10 rounded-xl p-6 sticky top-4 z-10">
      <div className="space-y-4">
        {/* Search */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-neutral-400" />
          <Input
            placeholder="Search manga titles..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10 rounded-md"
          />
        </div>

        {/* Filters */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Select>
            <SelectTrigger>
              <SelectValue placeholder="All Publishers" />
            </SelectTrigger>
            <SelectContent>
              {filters?.publishers.map((pub) => (
                <SelectItem key={pub.id} value={pub.slug}>
                  {pub.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>

          {/* More filters... */}
        </div>

        {/* Active filters */}
        {activeFilters.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {activeFilters.map((filter) => (
              <Badge key={filter.key} className="rounded-full">
                {filter.label}
                <X className="ml-1 w-3 h-3 cursor-pointer" />
              </Badge>
            ))}
            <Button variant="ghost" size="sm">
              Clear all
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}
```

---

## 11. Animation Library Recommendations

- **Framer Motion:** Page transitions, complex animations
- **React Spring:** Physics-based animations
- **Auto-animate:** Simple, zero-config animations
- **GSAP:** Heavy-duty animations (if needed)

---

## 12. Icon System

Use **Lucide React** for consistent, customizable icons:

```tsx
import {
  Calendar,
  Search,
  Filter,
  BookOpen,
  Heart,
  Star,
  TrendingUp,
  Bell,
  X,
  ChevronDown,
  ChevronRight
} from 'lucide-react';

// Usage
<Calendar className="w-5 h-5 text-neutral-600" />
```

---

**End of UI/UX Guide**
