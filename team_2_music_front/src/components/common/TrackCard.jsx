import { Link } from 'react-router-dom';
import { usePlayer } from '../../context/PlayerContext';

export default function TrackCard({ track }) {
    const { playTrack, currentTrack, isPlaying } = usePlayer();
    const isCurrentTrack = currentTrack?.id === track.id;

    const handlePlay = (e) => {
        e.preventDefault();
        playTrack(track);
    };

    return (
        <Link to={`/track/${track.id}`} className="group flex flex-col gap-3 rounded-lg p-2 transition-colors hover:bg-white/5">
            <div className="relative w-full overflow-hidden rounded-lg pt-[100%] bg-gray-800">
                {track.cover_image_url ? (
                    <img
                        className="absolute left-0 top-0 h-full w-full object-cover transition-transform duration-300 group-hover:scale-110"
                        src={track.cover_image_url}
                        alt={`Album art for ${track.title}`}
                        onError={(e) => {
                            e.target.style.display = 'none';
                            e.target.parentElement.classList.add('bg-gradient-to-br', 'from-purple-600', 'to-blue-600');
                            // Create and append fallback icon if not present
                            if (!e.target.parentElement.querySelector('.fallback-icon')) {
                                const icon = document.createElement('span');
                                icon.className = 'material-symbols-outlined text-4xl text-white opacity-50 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 fallback-icon';
                                icon.innerText = 'music_note';
                                e.target.parentElement.appendChild(icon);
                            }
                        }}
                    />
                ) : (
                    <div className="absolute left-0 top-0 h-full w-full bg-gradient-to-br from-purple-600 to-blue-600 flex items-center justify-center">
                        <span className="material-symbols-outlined text-4xl text-white opacity-50">music_note</span>
                    </div>
                )}
                <button
                    onClick={handlePlay}
                    className={`absolute bottom-2 right-2 flex h-10 w-10 items-center justify-center rounded-full shadow-lg transition-all duration-300 ${isCurrentTrack && isPlaying
                        ? 'bg-white text-[#8c2bee] opacity-100 bottom-4'
                        : 'bg-[#8c2bee] text-white opacity-0 group-hover:bottom-4 group-hover:opacity-100'
                        }`}
                >
                    <span className="material-symbols-outlined text-2xl">
                        {isCurrentTrack && isPlaying ? 'pause' : 'play_arrow'}
                    </span>
                </button>
            </div>
            <div>
                <p className="truncate text-base font-medium text-white">{track.title}</p>
                <p className="truncate text-sm text-gray-400">{track.artist_name || 'Unknown Artist'}</p>
            </div>
        </Link>
    );
}
