import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { trackAPI, likeAPI, commentAPI } from '../services/api';
import TrackCard from '../components/common/TrackCard';
import { usePlayer } from '../context/PlayerContext';

export default function DetailPage() {
    const { id } = useParams();
    const { playTrack, isPlaying, currentTrack, togglePlay } = usePlayer();
    const [track, setTrack] = useState(null);
    const [relatedTracks, setRelatedTracks] = useState([]);
    const [comments, setComments] = useState([]);
    const [newComment, setNewComment] = useState('');
    const [loading, setLoading] = useState(true);
    const [isLiked, setIsLiked] = useState(false);

    const isCurrentTrack = currentTrack?.id === track?.id;

    useEffect(() => {
        if (id) {
            fetchTrackDetails();
            fetchRelatedTracks();
            fetchComments();
        }
    }, [id]);

    const fetchTrackDetails = async () => {
        try {
            const response = await trackAPI.getById(id);
            setTrack(response.data);
        } catch (error) {
            console.error('Failed to fetch track:', error);
        } finally {
            setLoading(false);
        }
    };

    const fetchRelatedTracks = async () => {
        try {
            const response = await trackAPI.getAll({ limit: 6 });
            const tracksData = Array.isArray(response.data) ? response.data : [];
            setRelatedTracks(tracksData.filter(t => t.id !== parseInt(id)));
        } catch (error) {
            console.error('Failed to fetch related tracks:', error);
        }
    };

    const fetchComments = async () => {
        try {
            const response = await commentAPI.getByTrack(id);
            // Backend returns { comments: [], total: 0 }
            const commentsData = response.data.comments || [];
            setComments(commentsData);
        } catch (error) {
            console.error('Failed to fetch comments:', error);
        }
    };

    const handleLike = async () => {
        try {
            await likeAPI.toggle(id);
            setIsLiked(!isLiked);
            // Refresh track to get updated like count
            fetchTrackDetails();
        } catch (error) {
            console.error('Failed to toggle like:', error);
        }
    };

    const handleCommentSubmit = async (e) => {
        e.preventDefault();
        if (!newComment.trim()) return;

        try {
            await commentAPI.create({
                track_id: parseInt(id),
                content: newComment,
            });
            setNewComment('');
            fetchComments();
        } catch (error) {
            console.error('Failed to post comment:', error);
            alert('댓글 작성 실패');
        }
    };

    const handlePlay = () => {
        if (isCurrentTrack) {
            togglePlay();
        } else {
            playTrack(track);
        }
    };

    if (loading) {
        return (
            <main className="flex-1 flex items-center justify-center">
                <div className="text-white">Loading...</div>
            </main>
        );
    }

    if (!track) {
        return (
            <main className="flex-1 flex items-center justify-center">
                <div className="text-center">
                    <p className="text-white text-lg">Track not found</p>
                    <Link to="/" className="text-[#8c2bee] hover:underline mt-2 inline-block">
                        Go back home
                    </Link>
                </div>
            </main>
        );
    }

    return (
        <main className="flex-1">
            <div className="custom-container py-6 sm:py-8">
                <div className="flex flex-col lg:flex-row gap-8 lg:gap-12">
                    {/* Left: Album Art & Player */}
                    <div className="flex-1 lg:max-w-md">
                        <div className="flex flex-col gap-6 bg-transparent text-white sticky top-24">
                            {/* Album Art */}
                            <div className="flex items-center justify-center">
                                <div
                                    className="w-full max-w-sm aspect-square rounded-xl shadow-2xl shadow-[#8c2bee]/20 bg-cover bg-center"
                                    style={{
                                        backgroundImage: track.cover_image_url
                                            ? `url(${track.cover_image_url})`
                                            : "linear-gradient(to bottom right, #7c3aed, #2563eb)",
                                    }}
                                />
                            </div>

                            {/* Track Info */}
                            <div className="text-center">
                                <h1 className="text-2xl sm:text-3xl font-bold truncate">{track.title}</h1>
                                <p className="text-gray-400 text-base mt-1">By {track.artist || 'Unknown Artist'}</p>
                            </div>

                            {/* Player Controls */}
                            <div className="space-y-4">
                                <div className="flex items-center justify-center gap-4 sm:gap-6">
                                    <button className="flex items-center justify-center w-10 h-10 text-[#8c2bee] hover:scale-110 transition-transform">
                                        <span className="material-symbols-outlined text-3xl">skip_previous</span>
                                    </button>
                                    <button
                                        onClick={handlePlay}
                                        className="flex items-center justify-center w-14 h-14 sm:w-16 sm:h-16 bg-[#8c2bee] text-white rounded-full hover:scale-110 transition-transform"
                                    >
                                        <span className="material-symbols-outlined text-4xl sm:text-5xl">
                                            {isCurrentTrack && isPlaying ? 'pause' : 'play_arrow'}
                                        </span>
                                    </button>
                                    <button className="flex items-center justify-center w-10 h-10 text-[#8c2bee] hover:scale-110 transition-transform">
                                        <span className="material-symbols-outlined text-3xl">skip_next</span>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Right: Details & Interactions */}
                    <div className="flex-1 space-y-8">
                        {/* Action Buttons */}
                        <div className="flex flex-wrap gap-3 items-center pb-6 border-b border-white/10">
                            <button className="flex-1 sm:flex-none flex items-center justify-center gap-2 h-11 sm:h-12 px-5 sm:px-6 bg-[#8c2bee] text-white rounded-lg font-bold text-sm sm:text-base hover:bg-[#9c3bfe] transition-colors">
                                <span className="material-symbols-outlined text-xl">download</span>
                                Download
                            </button>
                            <button className="flex-1 sm:flex-none flex items-center justify-center gap-2 h-11 sm:h-12 px-5 sm:px-6 bg-white/10 text-white rounded-lg font-medium text-sm sm:text-base hover:bg-white/20 transition-colors">
                                <span className="material-symbols-outlined text-xl">share</span>
                                Share
                            </button>
                            <button
                                onClick={handleLike}
                                className={`flex-1 sm:flex-none flex items-center justify-center gap-2 h-11 sm:h-12 px-5 sm:px-6 rounded-lg font-medium text-sm sm:text-base transition-colors ${isLiked
                                    ? 'bg-[#8c2bee]/20 text-[#8c2bee]'
                                    : 'bg-white/10 text-white hover:bg-white/20'
                                    }`}
                            >
                                <span className={`material-symbols-outlined text-xl ${isLiked ? 'filled' : ''}`}>
                                    favorite
                                </span>
                                Like
                            </button>

                            <div className="w-full sm:w-auto flex flex-1 sm:flex-none items-center justify-end gap-4 sm:gap-6 text-center mt-3 sm:mt-0">
                                <div>
                                    <p className="font-bold text-base sm:text-lg text-white">
                                        {track.play_count || 0}
                                    </p>
                                    <p className="text-xs text-gray-400">Plays</p>
                                </div>
                                <div>
                                    <p className="font-bold text-base sm:text-lg text-white">
                                        {track.like_count || 0}
                                    </p>
                                    <p className="text-xs text-gray-400">Likes</p>
                                </div>
                            </div>
                        </div>

                        {/* About */}
                        <div className="space-y-4">
                            <h3 className="text-xl font-bold text-white">About This Track</h3>
                            <p className="text-gray-300 leading-relaxed">
                                {track.description || 'No description available.'}
                            </p>
                            {track.genre && (
                                <div className="flex flex-wrap gap-2 pt-2">
                                    <span className="px-3 py-1 text-sm rounded-full bg-[#8c2bee]/20 text-[#8c2bee] font-medium">
                                        #{track.genre}
                                    </span>
                                </div>
                            )}
                        </div>

                        {/* Comments */}
                        <div className="space-y-6">
                            <h3 className="text-xl font-bold text-white">
                                Comments ({comments.length})
                            </h3>

                            {/* Comment Input */}
                            <form onSubmit={handleCommentSubmit} className="flex items-start gap-4">
                                <div
                                    className="w-10 h-10 rounded-full bg-cover bg-center flex-shrink-0"
                                    style={{
                                        backgroundImage: "linear-gradient(to bottom right, #7c3aed, #2563eb)",
                                    }}
                                />
                                <div className="flex-1">
                                    <textarea
                                        value={newComment}
                                        onChange={(e) => setNewComment(e.target.value)}
                                        className="w-full rounded-lg bg-[#1a1a1a] border border-white/10 focus:ring-2 focus:ring-[#8c2bee] text-white placeholder-gray-400 p-3 text-sm resize-none"
                                        placeholder="Add a comment..."
                                        rows="2"
                                    />
                                    <button
                                        type="submit"
                                        disabled={!newComment.trim()}
                                        className="mt-2 px-4 py-2 bg-[#8c2bee] text-white rounded-lg text-sm font-bold hover:bg-[#9c3bfe] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                                    >
                                        Post Comment
                                    </button>
                                </div>
                            </form>

                            {/* Comments List */}
                            <div className="space-y-6">
                                {comments.length === 0 ? (
                                    <p className="text-gray-400 text-center py-8">No comments yet. Be the first!</p>
                                ) : (
                                    comments.map((comment) => (
                                        <div key={comment.id} className="flex items-start gap-4">
                                            <div
                                                className="w-10 h-10 rounded-full bg-cover bg-center flex-shrink-0"
                                                style={{
                                                    backgroundImage: "linear-gradient(to bottom right, #7c3aed, #2563eb)",
                                                }}
                                            />
                                            <div className="flex-1">
                                                <p className="font-bold text-white">User</p>
                                                <p className="text-gray-300 mt-1">{comment.content}</p>
                                                <p className="text-xs text-gray-500 mt-2">
                                                    {new Date(comment.created_at).toLocaleDateString()}
                                                </p>
                                            </div>
                                        </div>
                                    ))
                                )}
                            </div>
                        </div>
                    </div>
                </div>

                {/* Related Tracks */}
                {relatedTracks.length > 0 && (
                    <div className="mt-12 sm:mt-16">
                        <h2 className="text-2xl font-bold text-white mb-6">Related Tracks</h2>
                        <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6">
                            {relatedTracks.map((track) => (
                                <TrackCard key={track.id} track={track} />
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </main>
    );
}
