import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { userAPI, trackAPI } from '../services/api';
import EditTrackModal from '../components/EditTrackModal';

export default function ProfilePage() {
    const navigate = useNavigate();
    const [user, setUser] = useState(null);
    const [tracks, setTracks] = useState([]);
    const [loading, setLoading] = useState(true);
    const [activeTab, setActiveTab] = useState('my-music');
    const [openMenuId, setOpenMenuId] = useState(null);
    const [editingTrack, setEditingTrack] = useState(null);

    useEffect(() => {
        fetchUserData();
        fetchUserTracks();
    }, []);

    useEffect(() => {
        // Close menu when clicking outside
        const handleClickOutside = () => setOpenMenuId(null);
        if (openMenuId) {
            document.addEventListener('click', handleClickOutside);
            return () => document.removeEventListener('click', handleClickOutside);
        }
    }, [openMenuId]);

    const fetchUserData = async () => {
        try {
            const response = await userAPI.me();
            setUser(response.data);
        } catch (error) {
            console.error('Failed to fetch user:', error);
        }
    };

    const fetchUserTracks = async () => {
        try {
            const response = await trackAPI.getAll();
            const tracksData = Array.isArray(response.data) ? response.data : [];
            setTracks(tracksData);
        } catch (error) {
            console.error('Failed to fetch tracks:', error);
            setTracks([]);
        } finally {
            setLoading(false);
        }
    };

    const handleEdit = (track) => {
        setEditingTrack(track);
        setOpenMenuId(null);
    };

    const handleEditSuccess = () => {
        fetchUserTracks();
    };

    return (
        <main className="flex-1">
            <div className="custom-container py-6 sm:py-8">
                <div className="flex flex-col lg:flex-row gap-6 lg:gap-8">
                    {/* Sidebar - Desktop */}
                    <aside className="hidden lg:block lg:w-1/4 xl:w-1/5">
                        <div className="sticky top-24 bg-[#1a1a1a] rounded-xl p-6">
                            <div className="flex flex-col items-center text-center gap-4">
                                <div
                                    className="w-24 h-24 rounded-full bg-cover bg-center border-2 border-[#8c2bee]"
                                    style={{
                                        backgroundImage: user?.profile_image_url
                                            ? `url(${user.profile_image_url})`
                                            : "url('https://api.dicebear.com/7.x/avataaars/svg?seed=user')",
                                    }}
                                />
                                <div>
                                    <h1 className="text-xl font-bold text-white">
                                        {user?.nickname || 'User'}
                                    </h1>
                                    <p className="text-sm text-gray-400">
                                        {tracks.length} Tracks
                                    </p>
                                </div>
                                <button className="w-full px-4 py-2 bg-[#2a2a2a] hover:bg-[#3a3a3a] text-white text-sm font-bold rounded-lg transition-colors">
                                    Edit Profile
                                </button>
                            </div>

                            <nav className="mt-6 space-y-2">
                                <button
                                    onClick={() => setActiveTab('my-music')}
                                    className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${activeTab === 'my-music'
                                        ? 'bg-[#8c2bee]/20 text-[#8c2bee]'
                                        : 'text-gray-300 hover:bg-white/10 hover:text-white'
                                        }`}
                                >
                                    <span className="material-symbols-outlined">queue_music</span>
                                    <p className="text-sm font-medium">My Music</p>
                                </button>
                                <button
                                    onClick={() => setActiveTab('statistics')}
                                    className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${activeTab === 'statistics'
                                        ? 'bg-[#8c2bee]/20 text-[#8c2bee]'
                                        : 'text-gray-300 hover:bg-white/10 hover:text-white'
                                        }`}
                                >
                                    <span className="material-symbols-outlined">bar_chart</span>
                                    <p className="text-sm font-medium">Statistics</p>
                                </button>
                            </nav>
                        </div>
                    </aside>

                    {/* Main Content */}
                    <div className="flex-1">
                        {/* Mobile Profile Header */}
                        <div className="lg:hidden bg-[#1a1a1a] rounded-xl p-4 mb-6">
                            <div className="flex items-center gap-4">
                                <div
                                    className="w-16 h-16 rounded-full bg-cover bg-center border-2 border-[#8c2bee]"
                                    style={{
                                        backgroundImage: user?.profile_image_url
                                            ? `url(${user.profile_image_url})`
                                            : "url('https://api.dicebear.com/7.x/avataaars/svg?seed=user')",
                                    }}
                                />
                                <div className="flex-1">
                                    <h1 className="text-lg font-bold text-white">
                                        {user?.nickname || 'User'}
                                    </h1>
                                    <p className="text-sm text-gray-400">{tracks.length} Tracks</p>
                                </div>
                            </div>
                        </div>

                        {/* Tabs */}
                        <div className="border-b border-white/10 mb-6">
                            <div className="flex gap-8 px-4">
                                <button
                                    onClick={() => setActiveTab('my-music')}
                                    className={`flex flex-col items-center justify-center border-b-[3px] pb-3 pt-2 ${activeTab === 'my-music'
                                        ? 'border-[#8c2bee] text-white'
                                        : 'border-transparent text-gray-400 hover:text-white'
                                        }`}
                                >
                                    <p className="text-sm font-bold">My Music</p>
                                </button>
                                <button
                                    onClick={() => setActiveTab('statistics')}
                                    className={`flex flex-col items-center justify-center border-b-[3px] pb-3 pt-2 ${activeTab === 'statistics'
                                        ? 'border-[#8c2bee] text-white'
                                        : 'border-transparent text-gray-400 hover:text-white'
                                        }`}
                                >
                                    <p className="text-sm font-bold">Statistics</p>
                                </button>
                            </div>
                        </div>

                        {/* Content */}
                        {activeTab === 'my-music' && (
                            <div>
                                {loading ? (
                                    <div className="flex justify-center py-12">
                                        <div className="text-white">Loading...</div>
                                    </div>
                                ) : tracks.length === 0 ? (
                                    <div className="flex flex-col items-center justify-center py-16 text-center">
                                        <span className="material-symbols-outlined text-6xl text-gray-600 mb-4">
                                            music_note
                                        </span>
                                        <p className="text-gray-400 text-lg">아직 업로드한 트랙이 없습니다</p>
                                        <p className="text-gray-500 text-sm mt-2">첫 번째 음악을 업로드해보세요!</p>
                                    </div>
                                ) : (
                                    <div className="bg-[#1a1a1a] rounded-xl overflow-hidden">
                                        <div className="overflow-x-auto">
                                            <table className="w-full text-sm text-left text-gray-300">
                                                <thead className="text-xs text-gray-400 uppercase bg-white/5">
                                                    <tr>
                                                        <th className="px-4 sm:px-6 py-3 min-w-[200px]">Track</th>
                                                        <th className="px-4 sm:px-6 py-3 hidden sm:table-cell">Plays</th>
                                                        <th className="px-4 sm:px-6 py-3 hidden md:table-cell">Date Added</th>
                                                        <th className="px-4 sm:px-6 py-3">
                                                            <span className="sr-only">Actions</span>
                                                        </th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    {tracks.map((track) => (
                                                        <tr
                                                            key={track.id}
                                                            onClick={() => navigate(`/track/${track.id}`)}
                                                            className="border-b border-white/10 hover:bg-white/5 transition-colors cursor-pointer"
                                                        >
                                                            <td className="px-4 sm:px-6 py-4 font-medium text-white">
                                                                <div className="flex items-center gap-3">
                                                                    <div
                                                                        className="w-12 h-12 rounded bg-cover bg-center flex-shrink-0"
                                                                        style={{
                                                                            backgroundImage: track.cover_image_url
                                                                                ? `url(${track.cover_image_url})`
                                                                                : "linear-gradient(to bottom right, #7c3aed, #2563eb)",
                                                                        }}
                                                                    />
                                                                    <div className="min-w-0">
                                                                        <p className="font-bold truncate">{track.title}</p>
                                                                        <p className="text-xs text-gray-400 truncate">{track.genre || 'Unknown'}</p>
                                                                    </div>
                                                                </div>
                                                            </td>
                                                            <td className="px-4 sm:px-6 py-4 hidden sm:table-cell">
                                                                {track.play_count || 0}
                                                            </td>
                                                            <td className="px-4 sm:px-6 py-4 hidden md:table-cell">
                                                                {new Date(track.created_at).toLocaleDateString()}
                                                            </td>
                                                            <td className="px-4 sm:px-6 py-4 text-right relative">
                                                                <button
                                                                    onClick={(e) => {
                                                                        e.stopPropagation();
                                                                        setOpenMenuId(openMenuId === track.id ? null : track.id);
                                                                    }}
                                                                    className="text-gray-400 hover:text-white transition-colors"
                                                                >
                                                                    <span className="material-symbols-outlined text-xl">
                                                                        more_vert
                                                                    </span>
                                                                </button>

                                                                {/* Dropdown Menu */}
                                                                {openMenuId === track.id && (
                                                                    <div className="absolute right-0 top-full mt-1 w-48 bg-[#2a2a2a] rounded-lg shadow-xl border border-white/10 z-10">
                                                                        <button
                                                                            onClick={(e) => {
                                                                                e.stopPropagation();
                                                                                window.open(`http://localhost:8002/api/v1/tracks/${track.id}/stream`, '_blank');
                                                                                setOpenMenuId(null);
                                                                            }}
                                                                            className="w-full flex items-center gap-3 px-4 py-3 text-sm text-white hover:bg-white/10 transition-colors rounded-t-lg"
                                                                        >
                                                                            <span className="material-symbols-outlined text-lg">download</span>
                                                                            Download
                                                                        </button>
                                                                        <button
                                                                            onClick={(e) => {
                                                                                e.stopPropagation();
                                                                                alert('Edit functionality coming soon!');
                                                                                setOpenMenuId(null);
                                                                            }}
                                                                            className="w-full flex items-center gap-3 px-4 py-3 text-sm text-white hover:bg-white/10 transition-colors"
                                                                        >
                                                                            <span className="material-symbols-outlined text-lg">edit</span>
                                                                            Edit
                                                                        </button>
                                                                        <button
                                                                            onClick={(e) => {
                                                                                e.stopPropagation();
                                                                                if (confirm(`Delete "${track.title}"?`)) {
                                                                                    alert('Delete functionality coming soon!');
                                                                                }
                                                                                setOpenMenuId(null);
                                                                            }}
                                                                            className="w-full flex items-center gap-3 px-4 py-3 text-sm text-red-400 hover:bg-white/10 transition-colors rounded-b-lg"
                                                                        >
                                                                            <span className="material-symbols-outlined text-lg">delete</span>
                                                                            Delete
                                                                        </button>
                                                                    </div>
                                                                )}
                                                            </td>
                                                        </tr>
                                                    ))}
                                                </tbody>
                                            </table>
                                        </div>
                                    </div>
                                )}
                            </div>
                        )}

                        {activeTab === 'statistics' && (
                            <div className="bg-[#1a1a1a] rounded-xl p-6 sm:p-8">
                                <h2 className="text-xl font-bold text-white mb-6">Statistics</h2>
                                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                    <div className="bg-[#2a2a2a] rounded-lg p-4">
                                        <p className="text-sm text-gray-400">Total Plays</p>
                                        <p className="text-2xl font-bold text-white mt-1">
                                            {tracks.reduce((sum, t) => sum + (t.play_count || 0), 0)}
                                        </p>
                                    </div>
                                    <div className="bg-[#2a2a2a] rounded-lg p-4">
                                        <p className="text-sm text-gray-400">Total Tracks</p>
                                        <p className="text-2xl font-bold text-white mt-1">{tracks.length}</p>
                                    </div>
                                    <div className="bg-[#2a2a2a] rounded-lg p-4">
                                        <p className="text-sm text-gray-400">Total Likes</p>
                                        <p className="text-2xl font-bold text-white mt-1">
                                            {tracks.reduce((sum, t) => sum + (t.like_count || 0), 0)}
                                        </p>
                                    </div>
                                    <div className="bg-[#2a2a2a] rounded-lg p-4">
                                        <p className="text-sm text-gray-400">Followers</p>
                                        <p className="text-2xl font-bold text-white mt-1">0</p>
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </main>
    );
}
