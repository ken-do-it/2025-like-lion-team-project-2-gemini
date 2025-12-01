import { usePlayer } from '../../context/PlayerContext';

export default function MusicPlayer() {
    const { currentTrack, isPlaying, currentTime, duration, volume, togglePlay, seek, setVolume } = usePlayer();

    if (!currentTrack) return null;

    const formatTime = (seconds) => {
        if (!seconds || isNaN(seconds)) return '0:00';
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    };

    const handleSeek = (e) => {
        const rect = e.currentTarget.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const percentage = x / rect.width;
        seek(percentage * duration);
    };

    return (
        <footer className="fixed bottom-0 left-0 right-0 z-50 w-full bg-black/90 backdrop-blur-lg border-t border-white/10">
            <div className="custom-container">
                <div className="grid h-20 grid-cols-3 items-center gap-4">
                    {/* Track Info */}
                    <div className="flex items-center gap-3 min-w-0">
                        <div
                            className="h-12 w-12 flex-shrink-0 rounded bg-cover bg-center"
                            style={{
                                backgroundImage: currentTrack.cover_image_url
                                    ? `url(${currentTrack.cover_image_url})`
                                    : "linear-gradient(to bottom right, #7c3aed, #2563eb)",
                            }}
                        />
                        <div className="hidden sm:block min-w-0">
                            <p className="truncate text-sm font-bold text-white">{currentTrack.title}</p>
                            <p className="truncate text-xs text-gray-400">{currentTrack.artist_name || 'Unknown'}</p>
                        </div>
                    </div>

                    {/* Player Controls */}
                    <div className="flex flex-col items-center justify-center gap-2">
                        <div className="flex items-center gap-4 text-gray-300">
                            <button className="transition-colors hover:text-white">
                                <span className="material-symbols-outlined text-2xl">skip_previous</span>
                            </button>
                            <button
                                onClick={togglePlay}
                                className="flex h-10 w-10 items-center justify-center rounded-full bg-white text-black transition-transform hover:scale-110"
                            >
                                <span className="material-symbols-outlined text-3xl">
                                    {isPlaying ? 'pause' : 'play_arrow'}
                                </span>
                            </button>
                            <button className="transition-colors hover:text-white">
                                <span className="material-symbols-outlined text-2xl">skip_next</span>
                            </button>
                        </div>

                        {/* Progress Bar */}
                        <div className="hidden w-full max-w-xs items-center gap-2 text-xs md:flex">
                            <span className="text-gray-400">{formatTime(currentTime)}</span>
                            <div
                                className="h-1 w-full flex-1 rounded-full bg-gray-600 cursor-pointer"
                                onClick={handleSeek}
                            >
                                <div
                                    className="h-full rounded-full bg-white transition-all"
                                    style={{ width: `${(currentTime / duration) * 100}%` }}
                                />
                            </div>
                            <span className="text-gray-400">{formatTime(duration)}</span>
                        </div>
                    </div>

                    {/* Volume & Actions */}
                    <div className="flex items-center justify-end gap-3 text-gray-300">
                        <button className="transition-colors hover:text-white">
                            <span className="material-symbols-outlined text-xl">favorite_border</span>
                        </button>
                        <button className="hidden sm:block transition-colors hover:text-white">
                            <span className="material-symbols-outlined text-xl">download</span>
                        </button>
                        <div className="hidden items-center gap-2 md:flex">
                            <button className="transition-colors hover:text-white">
                                <span className="material-symbols-outlined text-xl">volume_up</span>
                            </button>
                            <input
                                type="range"
                                min="0"
                                max="1"
                                step="0.01"
                                value={volume}
                                onChange={(e) => setVolume(parseFloat(e.target.value))}
                                className="w-20 h-1 bg-gray-600 rounded-full appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-3 [&::-webkit-slider-thumb]:h-3 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-white"
                            />
                        </div>
                    </div>
                </div>
            </div>
        </footer>
    );
}
