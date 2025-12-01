import { useState, useEffect } from 'react';
import { trackAPI } from '../services/api';
import TrackCard from '../components/common/TrackCard';

export default function HomePage() {
    const [tracks, setTracks] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState('');

    useEffect(() => {
        fetchTracks();
    }, []);

    const fetchTracks = async () => {
        try {
            const response = await trackAPI.getAll({ limit: 12 });
            const tracksData = Array.isArray(response.data) ? response.data : [];
            setTracks(tracksData);
        } catch (error) {
            console.error('Failed to fetch tracks:', error);
            setTracks([]);
        } finally {
            setLoading(false);
        }
    };

    const handleSearch = (e) => {
        e.preventDefault();
        console.log('Search for:', searchQuery);
        // TODO: Implement search
    };

    return (
        <main className="flex-1">
            <div className="custom-container py-6 sm:py-8">
                {/* Hero Section - Reduced height */}
                <section
                    className="relative mb-8 sm:mb-12 flex min-h-[280px] sm:min-h-[320px] flex-col items-center justify-center overflow-hidden rounded-xl bg-cover bg-center p-6 sm:p-8 text-center"
                    style={{
                        backgroundImage:
                            "linear-gradient(rgba(25, 16, 34, 0.7) 0%, rgba(25, 16, 34, 0.9) 100%), url('https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=1200')",
                    }}
                >
                    <div className="z-10 flex flex-col items-center gap-3 sm:gap-4 max-w-4xl w-full">
                        <h2 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-black leading-tight tracking-tighter text-white">
                            AI 음악의 세계를 탐험하세요
                        </h2>
                        <p className="max-w-2xl text-sm sm:text-base md:text-lg text-gray-300 px-4">
                            AI가 만든 새로운 음악을 발견하고, 듣고, 공유하세요.
                        </p>

                        {/* Improved Search */}
                        <form onSubmit={handleSearch} className="relative z-10 mt-4 sm:mt-6 w-full max-w-2xl px-4">
                            <div className="flex h-12 sm:h-14 w-full items-stretch rounded-lg bg-[#191022]/50 shadow-lg backdrop-blur-sm border border-white/10">
                                <div className="flex items-center justify-center pl-3 sm:pl-4 text-gray-400">
                                    <span className="material-symbols-outlined text-xl sm:text-2xl">search</span>
                                </div>
                                <input
                                    type="text"
                                    value={searchQuery}
                                    onChange={(e) => setSearchQuery(e.target.value)}
                                    className="h-full w-full flex-1 border-0 bg-transparent px-3 sm:px-4 text-sm sm:text-base text-white placeholder-gray-400 focus:outline-none focus:ring-0"
                                    placeholder="아티스트, 트랙, 장르 검색"
                                />
                                <div className="flex items-center p-1 sm:p-1.5">
                                    <button
                                        type="submit"
                                        className="flex h-full min-w-[70px] sm:min-w-[84px] cursor-pointer items-center justify-center rounded-md bg-[#8c2bee] px-4 sm:px-5 text-sm font-bold text-white transition-all hover:bg-[#9c3bfe] active:scale-95"
                                    >
                                        검색
                                    </button>
                                </div>
                            </div>
                        </form>
                    </div>
                </section>

                {/* Track Grid with improved spacing */}
                <section className="mb-8 sm:mb-12">
                    <div className="mb-4 sm:mb-6 flex items-center justify-between px-1 sm:px-2">
                        <h3 className="text-xl sm:text-2xl font-bold leading-tight tracking-tight text-white">
                            인기 트랙
                        </h3>
                        <a className="text-xs sm:text-sm font-medium text-gray-400 hover:text-white transition-colors" href="#">
                            더 보기
                        </a>
                    </div>

                    {loading ? (
                        <div className="flex justify-center py-16 sm:py-20">
                            <div className="flex flex-col items-center gap-3">
                                <div className="h-8 w-8 animate-spin rounded-full border-4 border-gray-600 border-t-[#8c2bee]"></div>
                                <p className="text-gray-400 text-sm">로딩 중...</p>
                            </div>
                        </div>
                    ) : tracks.length === 0 ? (
                        <div className="flex justify-center py-16 sm:py-20">
                            <div className="text-center">
                                <span className="material-symbols-outlined text-6xl text-gray-600 mb-4">
                                    music_note
                                </span>
                                <p className="text-gray-400 text-base sm:text-lg">아직 트랙이 없습니다</p>
                                <p className="text-gray-500 text-sm mt-2">첫 번째 음악을 업로드해보세요!</p>
                            </div>
                        </div>
                    ) : (
                        <div className="grid grid-cols-2 gap-3 sm:gap-4 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6">
                            {tracks.map((track) => (
                                <TrackCard key={track.id} track={track} />
                            ))}
                        </div>
                    )}
                </section>
            </div>
        </main>
    );
}
