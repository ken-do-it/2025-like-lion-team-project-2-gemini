import { Link, useNavigate } from 'react-router-dom';
import { useState } from 'react';

export default function Header() {
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
    const [searchQuery, setSearchQuery] = useState('');
    const navigate = useNavigate();

    const handleSearch = (e) => {
        e.preventDefault();
        if (searchQuery.trim()) {
            navigate(`/search?q=${encodeURIComponent(searchQuery.trim())}`);
            setSearchQuery('');
        }
    };

    return (
        <header className="sticky top-0 z-50 w-full bg-[#191022]/80 backdrop-blur-sm border-b border-white/10">
            <div className="custom-container">
                <div className="flex h-16 items-center justify-between gap-4">
                    {/* Logo */}
                    <Link to="/" className="flex items-center gap-3 flex-shrink-0">
                        <span className="material-symbols-outlined text-[#8c2bee] text-2xl">
                            music_note
                        </span>
                        <h1 className="text-lg sm:text-xl font-bold tracking-tight text-white">AI Music</h1>
                    </Link>

                    {/* Search Bar - Desktop */}
                    <form onSubmit={handleSearch} className="hidden md:flex flex-1 max-w-md">
                        <div className="relative w-full">
                            <input
                                type="text"
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                placeholder="Search tracks, artists..."
                                className="w-full h-10 pr-4 pl-16 bg-white/10 border border-white/10 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#8c2bee] focus:border-transparent"
                                style={{ paddingLeft: '45px' }}
                            />
                            <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-xl pointer-events-none">
                                search
                            </span>
                        </div>
                    </form>

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
                        {/* Mobile Search */}
                        <form onSubmit={handleSearch} className="px-4 pb-2">
                            <div className="relative">
                                <input
                                    type="text"
                                    value={searchQuery}
                                    onChange={(e) => setSearchQuery(e.target.value)}
                                    placeholder="Search tracks, artists..."
                                    className="w-full h-10 pr-4 pl-16 bg-white/10 border border-white/10 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#8c2bee]"
                                    style={{ paddingLeft: '45px' }}
                                />
                                <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-xl pointer-events-none">
                                    search
                                </span>
                            </div>
                        </form>

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
