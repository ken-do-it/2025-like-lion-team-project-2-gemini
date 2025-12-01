import { useState, useEffect } from 'react';
import { trackAPI } from '../services/api';

export default function EditTrackModal({ track, onClose, onSuccess }) {
    const [formData, setFormData] = useState({
        title: '',
        description: '',
        genre: '',
        tags: '',
        aiPlatform: 'suno',
        aiPlatformOther: '',
        aiModel: '',
    });
    const [saving, setSaving] = useState(false);

    useEffect(() => {
        if (track) {
            // Parse description to extract AI metadata
            const desc = track.description || '';
            const metadataMatch = desc.match(/---\nAI Platform: (.+)\nAI Model: (.+)\nGenre: (.+)\nTags: (.+)/);

            let userDescription = desc;
            let aiPlatform = 'suno';
            let aiPlatformOther = '';
            let aiModel = '';
            let genre = '';
            let tags = '';

            if (metadataMatch) {
                userDescription = desc.substring(0, desc.indexOf('\n\n---')).trim();
                const platform = metadataMatch[1];
                aiModel = metadataMatch[2];
                genre = metadataMatch[3];
                tags = metadataMatch[4];

                // Check if platform is one of the predefined options
                if (['suno', 'mureka', 'soundraw'].includes(platform.toLowerCase())) {
                    aiPlatform = platform.toLowerCase();
                } else {
                    aiPlatform = 'other';
                    aiPlatformOther = platform;
                }
            }

            setFormData({
                title: track.title || '',
                description: userDescription,
                genre,
                tags,
                aiPlatform,
                aiPlatformOther,
                aiModel,
            });
        }
    }, [track]);

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!formData.title) {
            alert('제목을 입력해주세요.');
            return;
        }

        if (!formData.aiModel || (formData.aiPlatform === 'other' && !formData.aiPlatformOther)) {
            alert('AI 정보를 모두 입력해주세요.');
            return;
        }

        setSaving(true);

        try {
            // Prepare description with AI metadata
            const aiPlatformFinal = formData.aiPlatform === 'other' ? formData.aiPlatformOther : formData.aiPlatform;
            const aiMetadata = `\n\n---\nAI Platform: ${aiPlatformFinal}\nAI Model: ${formData.aiModel}\nGenre: ${formData.genre}\nTags: ${formData.tags}`;
            const finalDescription = (formData.description || '') + aiMetadata;

            await trackAPI.update(track.id, {
                title: formData.title,
                description: finalDescription,
            });

            alert('트랙 정보가 수정되었습니다!');
            onSuccess();
            onClose();
        } catch (error) {
            console.error('Update failed:', error);
            const errorDetail = error.response?.data?.detail;
            const errorMessage = typeof errorDetail === 'object' ? JSON.stringify(errorDetail) : (errorDetail || error.message);
            alert('수정 실패: ' + errorMessage);
        } finally {
            setSaving(false);
        }
    };

    if (!track) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
            <div className="bg-[#191022] border border-white/10 rounded-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto m-4">
                <div className="p-6">
                    <div className="flex justify-between items-center mb-6">
                        <h2 className="text-2xl font-bold text-white">트랙 수정</h2>
                        <button
                            onClick={onClose}
                            className="text-gray-400 hover:text-white transition-colors"
                        >
                            <span className="material-symbols-outlined text-2xl">close</span>
                        </button>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-6">
                        {/* Title */}
                        <label className="flex flex-col w-full">
                            <p className="text-white text-base font-medium mb-2">제목 *</p>
                            <input
                                type="text"
                                value={formData.title}
                                onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
                                className="form-input flex w-full rounded-lg text-white focus:outline-0 focus:ring-2 focus:ring-[#8c2bee]/50 border border-[#4d3267] bg-[#261933] focus:border-[#8c2bee] h-12 placeholder:text-[#ad92c9] p-3 text-sm"
                                placeholder="음악의 제목을 입력하세요"
                                required
                            />
                        </label>

                        {/* Description */}
                        <label className="flex flex-col w-full">
                            <p className="text-white text-base font-medium mb-2">음악에 대한 설명</p>
                            <textarea
                                value={formData.description}
                                onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                                className="form-textarea flex w-full rounded-lg text-white focus:outline-0 focus:ring-2 focus:ring-[#8c2bee]/50 border border-[#4d3267] bg-[#261933] focus:border-[#8c2bee] h-24 placeholder:text-[#ad92c9] p-3 text-sm resize-none"
                                placeholder="음악에 대한 설명을 입력하세요"
                            />
                        </label>

                        {/* AI Platform */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <label className="flex flex-col w-full">
                                <p className="text-white text-base font-medium mb-2">어떤 AI를 사용했나요? (필수)</p>
                                <select
                                    value={formData.aiPlatform}
                                    onChange={(e) => setFormData(prev => ({ ...prev, aiPlatform: e.target.value }))}
                                    className="form-select flex w-full rounded-lg text-white focus:outline-0 focus:ring-2 focus:ring-[#8c2bee]/50 border border-[#4d3267] bg-[#261933] focus:border-[#8c2bee] h-12 p-3 text-sm"
                                    required
                                >
                                    <option value="suno">Suno</option>
                                    <option value="mureka">Mureka</option>
                                    <option value="soundraw">Soundraw</option>
                                    <option value="other">기타 (직접 입력)</option>
                                </select>
                                {formData.aiPlatform === 'other' && (
                                    <input
                                        type="text"
                                        value={formData.aiPlatformOther}
                                        onChange={(e) => setFormData(prev => ({ ...prev, aiPlatformOther: e.target.value }))}
                                        className="mt-2 form-input flex w-full rounded-lg text-white focus:outline-0 focus:ring-2 focus:ring-[#8c2bee]/50 border border-[#4d3267] bg-[#261933] focus:border-[#8c2bee] h-12 placeholder:text-[#ad92c9] p-3 text-sm"
                                        placeholder="사용하신 AI 플랫폼 이름을 입력하세요"
                                        required
                                    />
                                )}
                            </label>

                            {/* AI Model */}
                            <label className="flex flex-col w-full">
                                <p className="text-white text-base font-medium mb-2">사용한 모델 (필수)</p>
                                <input
                                    type="text"
                                    value={formData.aiModel}
                                    onChange={(e) => setFormData(prev => ({ ...prev, aiModel: e.target.value }))}
                                    className="form-input flex w-full rounded-lg text-white focus:outline-0 focus:ring-2 focus:ring-[#8c2bee]/50 border border-[#4d3267] bg-[#261933] focus:border-[#8c2bee] h-12 placeholder:text-[#ad92c9] p-3 text-sm"
                                    placeholder="예: v3, v3.5, Udio beta"
                                    required
                                />
                            </label>
                        </div>

                        {/* Genre and Tags */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <label className="flex flex-col w-full">
                                <p className="text-white text-base font-medium mb-2">장르</p>
                                <input
                                    type="text"
                                    value={formData.genre}
                                    onChange={(e) => setFormData(prev => ({ ...prev, genre: e.target.value }))}
                                    className="form-input flex w-full rounded-lg text-white focus:outline-0 focus:ring-2 focus:ring-[#8c2bee]/50 border border-[#4d3267] bg-[#261933] focus:border-[#8c2bee] h-12 placeholder:text-[#ad92c9] p-3 text-sm"
                                    placeholder="예: Electronic, Lo-fi, Ambient"
                                />
                            </label>

                            <label className="flex flex-col w-full">
                                <p className="text-white text-base font-medium mb-2">분위기 / 태그</p>
                                <input
                                    type="text"
                                    value={formData.tags}
                                    onChange={(e) => setFormData(prev => ({ ...prev, tags: e.target.value }))}
                                    className="form-input flex w-full rounded-lg text-white focus:outline-0 focus:ring-2 focus:ring-[#8c2bee]/50 border border-[#4d3267] bg-[#261933] focus:border-[#8c2bee] h-12 placeholder:text-[#ad92c9] p-3 text-sm"
                                    placeholder="예: chill, focus, relaxing (쉼표로 구분)"
                                />
                            </label>
                        </div>

                        {/* Action Buttons */}
                        <div className="flex justify-end gap-3 pt-4">
                            <button
                                type="button"
                                onClick={onClose}
                                disabled={saving}
                                className="px-6 py-2 rounded-lg bg-[#362348] text-white font-bold hover:bg-[#4d3267] transition-colors disabled:opacity-50"
                            >
                                취소
                            </button>
                            <button
                                type="submit"
                                disabled={saving}
                                className="px-6 py-2 rounded-lg bg-[#8c2bee] text-white font-bold hover:bg-[#9c3bfe] transition-colors disabled:opacity-50"
                            >
                                {saving ? '저장 중...' : '저장'}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
}
