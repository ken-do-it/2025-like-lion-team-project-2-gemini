import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { trackAPI } from '../services/api';
import TrackCard from '../components/common/TrackCard';

export default function SearchPage() {
    const [searchParams] = useSearchParams();
    const query = searchParams.get('q') || '';
    const [tracks, setTracks] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (query) {
            searchTracks();
        }
    }, [query]);

    const searchTracks = async () => {
        setLoading(true);
        try {
            console.log('Searching for:', query);
            const response = await trackAPI.search(query);
            console.log('Search response:', response.data);
            const tracksData = Array.isArray(response.data) ? response.data : [];
            setTracks(tracksData);
        } catch (error) {
            console.error('Failed to search tracks:', error);
            setTracks([]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <main className="flex-1">
            <div className="custom-container py-6 sm:py-8">
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-white mb-2">
                        Search Results
                    </h1>
                    <p className="text-gray-400">
                        {query ? `Results for "${query}"` : 'Enter a search query'}
                    </p>
                </div>

                {loading ? (
                    <div className="flex items-center justify-center py-20">
                        <div className="text-white text-lg">Searching...</div>
                    </div>
                ) : tracks.length > 0 ? (
                    <div>
                        <p className="text-gray-400 mb-6">{tracks.length} tracks found</p>
                        <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6">
                            {tracks.map((track) => (
                                <TrackCard key={track.id} track={track} />
                            ))}
                        </div>
                    </div>
                ) : query ? (
                    <div className="flex flex-col items-center justify-center py-20">
                        <span className="material-symbols-outlined text-6xl text-gray-600 mb-4">
                            search_off
                        </span>
                        <p className="text-gray-400 text-lg">No tracks found for "{query}"</p>
                        <p className="text-gray-500 text-sm mt-2">Try different keywords</p>
                    </div>
                ) : (
                    <div className="flex flex-col items-center justify-center py-20">
                        <span className="material-symbols-outlined text-6xl text-gray-600 mb-4">
                            search
                        </span>
                        <p className="text-gray-400 text-lg">Start searching for music</p>
                    </div>
                )}
            </div>
        </main>
    );
}
