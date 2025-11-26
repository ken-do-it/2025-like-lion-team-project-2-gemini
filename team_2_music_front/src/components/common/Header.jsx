import { Link } from 'react-router-dom';
import { useState } from 'react';

export default function Header() {
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

    return (
        <header className="sticky top-0 z-50 w-full bg-[#191022]/80 backdrop-blur-sm border-b border-white/10">
            <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex h-16 items-center justify-between">
                    {/* Logo */}
                    <Link to="/" className="flex items-center gap-3">
                        <span className="material-symbols-outlined text-[#8c2bee] text-2xl">
                            music_note
                        </span>
                        <h1 className="text-lg sm:text-xl font-bold tracking-tight text-white">AI Music</h1>
                    </Link>

                    {/* Desktop Navigation */}
                    <nav className="hidden items-center gap-6 md:flex">
                        <Link
                            to="/"
                            className="text-sm font-medium text-gray-300 transition-colors hover:text-white"
                        >
                            탐색
                        </Link>
                        <Link
                            to="/upload"
                            className="text-sm font-medium text-gray-300 transition-colors hover:text-white"
                        >
                            업로드
                        </Link>
                        <Link
                            to="/profile"
                            className="text-sm font-medium text-gray-300 transition-colors hover:text-white"
                        >
                            내 라이브러리
                        </Link>
                    </nav>

                    {/* Right side */}
                    <div className="flex items-center gap-2 sm:gap-3">
                        <button className="flex h-9 w-9 sm:h-10 sm:w-10 cursor-pointer items-center justify-center rounded-full bg-white/10 text-gray-300 transition-colors hover:bg-white/20 hover:text-white">
                            <span className="material-symbols-outlined text-xl">notifications</span>
                        </button>
                        <Link to="/profile">
                            <div
                                className="h-9 w-9 sm:h-10 sm:w-10 rounded-full bg-cover bg-center"
                                style={{
                                    backgroundImage:
                                        "url('https://api.dicebear.com/7.x/avataaars/svg?seed=user')",
                                }}
                            />
                        </Link>

                        {/* Mobile menu button */}
                        <button
                            className="md:hidden flex h-9 w-9 items-center justify-center rounded-lg bg-white/10 text-gray-300"
                            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                        >
                            <span className="material-symbols-outlined text-xl">
                                {mobileMenuOpen ? 'close' : 'menu'}
                            </span>
                        </button>
                    </div>
                </div>

                {/* Mobile Navigation */}
                {mobileMenuOpen && (
                    <nav className="md:hidden border-t border-white/10 py-4 space-y-2">
                        <Link
                            to="/"
                            className="block px-4 py-2 text-sm font-medium text-gray-300 hover:text-white hover:bg-white/5 rounded-lg"
                            onClick={() => setMobileMenuOpen(false)}
                        >
                            탐색
                        </Link>
                        <Link
                            to="/upload"
                            className="block px-4 py-2 text-sm font-medium text-gray-300 hover:text-white hover:bg-white/5 rounded-lg"
                            onClick={() => setMobileMenuOpen(false)}
                        >
                            업로드
                        </Link>
                        <Link
                            to="/profile"
                            className="block px-4 py-2 text-sm font-medium text-gray-300 hover:text-white hover:bg-white/5 rounded-lg"
                            onClick={() => setMobileMenuOpen(false)}
                        >
                            내 라이브러리
                        </Link>
                    </nav>
                )}
            </div>
        </header>
    );
}
