import { SiteHeader } from "@/components/site-header";
import { assessmentPrinciples } from "@/lib/platform";

export default function Home() {
  return (
    <>
      <SiteHeader />
      <main id="main">
        <section className="mx-auto grid max-w-6xl items-center gap-12 px-6 py-20 lg:grid-cols-[1.2fr_1fr] lg:py-28">
          <div>
            <p className="mb-6 text-xs font-bold tracking-[0.2em] text-brand uppercase">Clarity at every clause</p>
            <h1 className="max-w-2xl text-5xl leading-[1.08] font-semibold tracking-tight sm:text-6xl">A clearer view of<br /><span className="text-brand">contract risk.</span></h1>
            <p className="mt-7 max-w-lg text-lg leading-8 text-slate-600">Bring consistency to the first pass of contract review with transparent, rule-based assessment.</p>
            <a href="#approach" className="mt-8 inline-flex items-center gap-5 rounded-lg bg-brand px-6 py-3.5 text-sm font-semibold text-white hover:bg-teal-800">Explore the approach <span aria-hidden="true">&rarr;</span></a>
            <p className="mt-5 text-xs text-slate-500">Platform foundation · Assessment workspace coming later</p>
          </div>
          <aside aria-label="Illustrative assessment result" className="rounded-2xl border border-slate-200 bg-white p-7 shadow-lg shadow-slate-200/50">
            <div className="flex items-center justify-between border-b border-slate-100 pb-5"><span className="text-sm font-semibold">Assessment overview</span><span className="rounded-full bg-slate-100 px-3 py-1 text-xs text-slate-600">Illustrative sample</span></div>
            <div className="my-7 flex items-end justify-between"><div><p className="text-xs text-slate-500">Weighted risk score</p><p className="mt-2 text-5xl font-semibold">8 <span className="text-base font-normal text-slate-400">points</span></p></div><span className="rounded-md bg-rose-50 px-3 py-2 text-sm font-semibold text-rose-800">High Risk</span></div>
            <ul className="space-y-4 text-sm">
              {[['Termination without notice', '3'], ['Unlimited liability', '3'], ['Confidentiality', '1'], ['Arbitration', '1']].map(([clause, points]) => <li key={clause} className="flex justify-between gap-3 border-b border-slate-100 pb-3"><span className="text-slate-600">{clause}</span><span className="font-medium">+{points}</span></li>)}
            </ul>
            <p className="mt-5 text-xs leading-5 text-slate-500">Four findings from the original sample contract. This illustration is static, not a live assessment.</p>
          </aside>
        </section>
        <section id="approach" className="border-y border-slate-200 bg-white px-6 py-16">
          <div className="mx-auto max-w-6xl"><p className="text-xs font-bold tracking-widest text-brand uppercase">A considered approach</p><h2 className="mt-3 text-3xl font-semibold tracking-tight">Understand the signal behind the score.</h2>
            <div className="mt-10 grid gap-9 md:grid-cols-3">{assessmentPrinciples.map((item) => <article key={item.number}><p className="text-sm font-semibold text-brand">{item.number} /</p><h3 className="mt-4 text-lg font-semibold">{item.title}</h3><p className="mt-3 text-sm leading-7 text-slate-600">{item.description}</p></article>)}</div>
          </div>
        </section>
        <section id="roadmap" className="mx-auto max-w-6xl px-6 py-16"><p className="text-xs font-bold tracking-widest text-brand uppercase">Built with intention</p><div className="mt-4 grid gap-6 md:grid-cols-2"><h2 className="text-3xl font-semibold tracking-tight">A strong foundation.<br />A measured path forward.</h2><p className="max-w-lg text-sm leading-7 text-slate-600">The existing risk engine and API remain available. This milestone establishes the web platform. Database persistence, authentication and an interactive assessment workspace are planned for later milestones.</p></div></section>
      </main>
      <footer className="border-t border-slate-200 px-6 py-6"><div className="mx-auto flex max-w-6xl flex-wrap justify-between gap-3 text-xs text-slate-500"><span>Contract Risk Assessment Platform</span><span>Educational demonstration · Not legal advice</span></div></footer>
    </>
  );
}
