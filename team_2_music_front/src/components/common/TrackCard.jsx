import { Link } from 'react-router-dom';

export default function TrackCard({ track }) {
    const handlePlay = (e) => {
        e.preventDefault();
        // TODO: Implement play functionality
        console.log('Play track:', track.id);
    };

    return (
        <Link to={`/track/${track.id}`} className="group flex flex-col gap-3 rounded-lg p-2 transition-colors hover:bg-white/5">
            <div className="relative w-full overflow-hidden rounded-lg pt-[100%]">
                <img
                    className="absolute left-0 top-0 h-full w-full object-cover transition-transform duration-300 group-hover:scale-110"
                    src={track.cover_image_url || 'https://via.placeholder.com/300?text=No+Cover'}
                    alt={`Album art for ${track.title}`}
                />
                <button
                    onClick={handlePlay}
                    className="absolute bottom-2 right-2 flex h-10 w-10 items-center justify-center rounded-full bg-[#8c2bee] text-white opacity-0 shadow-lg transition-all duration-300 group-hover:bottom-4 group-hover:opacity-100"
                >
                    <span className="material-symbols-outlined text-2xl">play_arrow</span>
                </button>
            </div>
            <div>
                <p className="truncate text-base font-medium text-white">{track.title}</p>
                <p className="truncate text-sm text-gray-400">{track.artist || 'Unknown Artist'}</p>
            </div>
        </Link>
    );
}
