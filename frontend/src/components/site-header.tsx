export function SiteHeader() {
  return (
    <header className="border-b border-slate-200 bg-white">
      <a href="#main" className="sr-only focus:not-sr-only focus:absolute focus:bg-white focus:p-4">Skip to content</a>
      <nav aria-label="Main navigation" className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-4 px-6 py-5">
        <a href="/" className="flex items-center gap-3 font-bold tracking-tight">
          <span aria-hidden="true" className="grid h-9 w-9 place-items-center rounded-lg bg-brand text-sm text-white">CR</span>
          Contract Risk<span className="hidden font-normal text-slate-500 sm:inline"> / Platform</span>
        </a>
        <div className="flex gap-6 text-sm font-medium text-slate-600">
          <a href="#approach" className="hover:text-brand">Our approach</a>
          <a href="#roadmap" className="hover:text-brand">Roadmap</a>
        </div>
      </nav>
    </header>
  );
}
