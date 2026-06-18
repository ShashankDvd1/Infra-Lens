"use client";

import Link from "next/link";
import { ArrowRight, Map, Bot, Building2, TrendingUp } from "lucide-react";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-white">
      {/* Navbar */}
      <header className="absolute inset-x-0 top-0 z-50">
        <nav className="flex items-center justify-between p-6 lg:px-8" aria-label="Global">
          <div className="flex lg:flex-1">
            <a href="#" className="-m-1.5 p-1.5 flex items-center gap-2">
              <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center text-white font-bold text-xl">L</div>
              <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-blue-600">LandScope AI</span>
            </a>
          </div>
          <div className="flex flex-1 justify-end">
            <Link href="/map" className="text-sm font-semibold leading-6 text-gray-900 hover:text-indigo-600 transition-colors">
              Enter Platform <span aria-hidden="true">&rarr;</span>
            </Link>
          </div>
        </nav>
      </header>

      <main className="isolate">
        {/* Hero section */}
        <div className="relative pt-14">
          <div className="absolute inset-x-0 -top-40 -z-10 transform-gpu overflow-hidden blur-3xl sm:-top-80" aria-hidden="true">
            <div className="relative left-[calc(50%-11rem)] aspect-[1155/678] w-[36.125rem] -translate-x-1/2 rotate-[30deg] bg-gradient-to-tr from-[#ff80b5] to-[#9089fc] opacity-30 sm:left-[calc(50%-30rem)] sm:w-[72.1875rem]" style={{ clipPath: "polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)" }}></div>
          </div>
          
          <div className="py-24 sm:py-32 lg:pb-40">
            <div className="mx-auto max-w-7xl px-6 lg:px-8">
              <div className="mx-auto max-w-2xl text-center">
                <div className="mb-8 flex justify-center">
                  <div className="relative rounded-full px-3 py-1 text-sm leading-6 text-gray-600 ring-1 ring-gray-900/10 hover:ring-gray-900/20">
                    Currently tracking Lucknow MVP. <a href="#" className="font-semibold text-indigo-600"><span className="absolute inset-0" aria-hidden="true"></span>Read more <span aria-hidden="true">&rarr;</span></a>
                  </div>
                </div>
                <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
                  Know where the city is growing, before prices move.
                </h1>
                <p className="mt-6 text-lg leading-8 text-gray-600">
                  LandScope AI aggregates government notifications, master plans, and tenders to build a predictive map of infrastructure growth. Stop guessing where to invest.
                </p>
                <div className="mt-10 flex items-center justify-center gap-x-6">
                  <Link href="/map" className="rounded-md bg-indigo-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 flex items-center gap-2">
                    Open Infrastructure Map <ArrowRight className="w-4 h-4" />
                  </Link>
                  <Link href="/ask-ai" className="text-sm font-semibold leading-6 text-gray-900 hover:text-indigo-600">
                    Try Ask AI <span aria-hidden="true">→</span>
                  </Link>
                </div>
              </div>
              
              {/* Feature grid */}
              <div className="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-none">
                <dl className="grid max-w-xl grid-cols-1 gap-x-8 gap-y-16 lg:max-w-none lg:grid-cols-3">
                  <div className="flex flex-col">
                    <dt className="flex items-center gap-x-3 text-base font-semibold leading-7 text-gray-900">
                      <Map className="h-5 w-5 flex-none text-indigo-600" aria-hidden="true" />
                      Geospatial Mapping
                    </dt>
                    <dd className="mt-4 flex flex-auto flex-col text-base leading-7 text-gray-600">
                      <p className="flex-auto">Visualize upcoming expressways, metro lines, and IT parks on an interactive map. See the 5km impact radius of major developments.</p>
                    </dd>
                  </div>
                  <div className="flex flex-col">
                    <dt className="flex items-center gap-x-3 text-base font-semibold leading-7 text-gray-900">
                      <Bot className="h-5 w-5 flex-none text-indigo-600" aria-hidden="true" />
                      RAG-Powered Intelligence
                    </dt>
                    <dd className="mt-4 flex flex-auto flex-col text-base leading-7 text-gray-600">
                      <p className="flex-auto">Ask complex questions about real estate growth. Our AI parses hundreds of government PDFs to give you verified, cited answers.</p>
                    </dd>
                  </div>
                  <div className="flex flex-col">
                    <dt className="flex items-center gap-x-3 text-base font-semibold leading-7 text-gray-900">
                      <TrendingUp className="h-5 w-5 flex-none text-indigo-600" aria-hidden="true" />
                      Predictive Growth
                    </dt>
                    <dd className="mt-4 flex flex-auto flex-col text-base leading-7 text-gray-600">
                      <p className="flex-auto">Identify undervalued localities by tracking early-stage infrastructure announcements before construction begins.</p>
                    </dd>
                  </div>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
