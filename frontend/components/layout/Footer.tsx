/**
 * Footer component.
 */

export function Footer() {
  return (
    <footer className="mt-auto border-t bg-muted/50">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center text-sm text-muted-foreground">
          <p className="mb-2">
            Built with ❤️ by manga fans, for manga fans
          </p>
          <p>
            Manga Release Radar © {new Date().getFullYear()}
          </p>
        </div>
      </div>
    </footer>
  )
}
