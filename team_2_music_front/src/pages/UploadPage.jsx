import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { trackAPI } from '../services/api';

export default function UploadPage() {
    const navigate = useNavigate();
    const [uploading, setUploading] = useState(false);
    const [uploadProgress, setUploadProgress] = useState(0);
    const [dragActive, setDragActive] = useState(false);

    const [formData, setFormData] = useState({
        file: null,
        title: '',
        description: '',
        genre: '',
        tags: '',
        coverImage: null,
        aiPlatform: 'suno', // Default
        aiPlatformOther: '',
        aiModel: '',
    });

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFileChange(e.dataTransfer.files[0]);
        }
    };

    const handleFileChange = (file) => {
        if (file && (file.type === 'audio/mpeg' || file.type === 'audio/wav' || file.type === 'audio/flac')) {
            setFormData(prev => ({ ...prev, file }));
            // Auto-fill title from filename
            if (!formData.title) {
                const filename = file.name.replace(/\.[^/.]+$/, "");
                setFormData(prev => ({ ...prev, title: filename }));
            }
        } else {
            alert('지원되는 형식: MP3, WAV, FLAC만 업로드 가능합니다.');
        }
    };

    const handleCoverImageChange = (file) => {
        if (file && file.type.startsWith('image/')) {
            setFormData(prev => ({ ...prev, coverImage: file }));
        } else {
            alert('이미지 파일만 업로드 가능합니다.');
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!formData.file) {
            alert('음악 파일을 선택해주세요.');
            return;
        }

        if (!formData.title) {
            alert('제목을 입력해주세요.');
            return;
        }

        setUploading(true);
        setUploadProgress(10);

        try {
            // Step 1: Initiate upload
            setUploadProgress(20);
            // Debug logging
            console.log('Sending upload request:', {
                filename: formData.file.name,
                content_type: formData.file.type,
                file_size: formData.file.size,
            });

            const initiateResponse = await trackAPI.initiateUpload({
                filename: formData.file.name,
                content_type: formData.file.type,
                file_size: formData.file.size,
            });

            // Step 2: Upload to S3 (or local storage)
            setUploadProgress(40);
            const { presigned_url, upload_id } = initiateResponse.data;

            console.log('Upload initiated:', { presigned_url, upload_id });

            await fetch(presigned_url, {
                method: 'PUT',
                body: formData.file,
                headers: {
                    'Content-Type': formData.file.type,
                },
            });

            setUploadProgress(70);

            // Prepare description with AI metadata
            const aiPlatformFinal = formData.aiPlatform === 'other' ? formData.aiPlatformOther : formData.aiPlatform;
            const aiMetadata = `\n\n---\nAI Platform: ${aiPlatformFinal}\nAI Model: ${formData.aiModel}\nGenre: ${formData.genre}\nTags: ${formData.tags}`;
            const finalDescription = (formData.description || '') + aiMetadata;

            // Step 3: Finalize upload with metadata
            await trackAPI.finalizeUpload({
                upload_id,
                title: formData.title,
                description: finalDescription,
                genre: formData.genre || null,
                tags: formData.tags ? formData.tags.split(',').map(t => t.trim()) : [],
            });

            setUploadProgress(100);
            alert('업로드 완료!');
            navigate('/profile');
        } catch (error) {
            console.error('Upload failed:', error);
            const errorDetail = error.response?.data?.detail;
            const errorMessage = typeof errorDetail === 'object' ? JSON.stringify(errorDetail) : (errorDetail || error.message);
            alert('업로드 실패: ' + errorMessage);
        } finally {
            setUploading(false);
            setUploadProgress(0);
        }
    };

    return (
        <main className="flex-1">
            <div className="custom-container py-6 sm:py-8 max-w-2xl mx-auto">
                <div className="mb-6 sm:mb-8">
                    <h1 className="text-3xl sm:text-4xl font-black leading-tight tracking-tight text-white">
                        새로운 AI 음악 업로드
                    </h1>
                    <p className="text-gray-400 text-sm sm:text-base mt-2">
                        AI로 생성한 음악 파일을 업로드하고 제목, 설명, 장르 등의 세부 정보를 추가하세요.
                    </p>
                </div>

                <form onSubmit={handleSubmit} className="space-y-6">
                    {/* File Upload Area */}
                    <div
                        className={`flex flex-col items-center gap-6 rounded-xl border-2 border-dashed px-6 py-12 sm:py-14 transition-colors ${dragActive ? 'border-[#8c2bee] bg-[#8c2bee]/10' : 'border-[#4d3267] bg-transparent'
                            }`}
                        onDragEnter={handleDrag}
                        onDragLeave={handleDrag}
                        onDragOver={handleDrag}
                        onDrop={handleDrop}
                    >
                        <div className="flex max-w-[480px] flex-col items-center gap-3 text-center">
                            <span className="material-symbols-outlined text-4xl sm:text-5xl text-[#ad92c9]">
                                upload_file
                            </span>
                            <p className="text-white text-base sm:text-lg font-bold">
                                {formData.file ? formData.file.name : '여기에 음악 파일을 드래그 앤 드롭하세요'}
                            </p>
                            <p className="text-[#ad92c9] text-xs sm:text-sm">
                                지원 형식: MP3, WAV, FLAC. 최대 파일 크기: 100MB
                            </p>
                        </div>
                        <input
                            type="file"
                            id="file-upload"
                            accept="audio/mpeg,audio/wav,audio/flac"
                            onChange={(e) => e.target.files[0] && handleFileChange(e.target.files[0])}
                            className="hidden"
                        />
                        <label
                            htmlFor="file-upload"
                            className="flex min-w-[120px] cursor-pointer items-center justify-center rounded-lg h-10 px-4 bg-[#362348] text-white text-sm font-bold hover:bg-[#4d3267] transition-colors"
                        >
                            파일 선택
                        </label>
                    </div>

                    {/* Upload Progress */}
                    {uploading && (
                        <div className="flex flex-col gap-2">
                            <div className="flex justify-between text-sm">
                                <p className="text-white font-medium">파일 업로드 중...</p>
                                <p className="text-white/70 font-medium">{uploadProgress}%</p>
                            </div>
                            <div className="rounded-full bg-[#4d3267] h-2">
                                <div
                                    className="h-2 rounded-full bg-[#8c2bee] transition-all duration-300"
                                    style={{ width: `${uploadProgress}%` }}
                                />
                            </div>
                        </div>
                    )}

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        {/* Cover Image */}
                        <div className="md:col-span-1 flex flex-col gap-4">
                            <label className="text-white text-base font-medium">앨범 아트</label>
                            <input
                                type="file"
                                id="cover-upload"
                                accept="image/*"
                                onChange={(e) => e.target.files[0] && handleCoverImageChange(e.target.files[0])}
                                className="hidden"
                            />
                            <label
                                htmlFor="cover-upload"
                                className="flex items-center justify-center w-full aspect-square rounded-xl border-2 border-dashed border-[#4d3267] cursor-pointer hover:bg-[#261933] transition-colors overflow-hidden"
                                style={
                                    formData.coverImage
                                        ? { backgroundImage: `url(${URL.createObjectURL(formData.coverImage)})`, backgroundSize: 'cover', backgroundPosition: 'center', height: '15rem' }
                                        : { height: '15rem' }
                                }
                            >
                                {!formData.coverImage && (
                                    <div className="text-center">
                                        <span className="material-symbols-outlined text-4xl text-[#ad92c9]">
                                            add_photo_alternate
                                        </span>
                                        <p className="text-sm text-[#ad92c9] mt-2">이미지 업로드</p>
                                    </div>
                                )}
                            </label>
                        </div>

                        {/* Metadata */}
                        <div className="md:col-span-2 flex flex-col gap-4 sm:gap-6">
                            <label className="flex flex-col w-full">
                                <p className="text-white text-base font-medium mb-2">제목 *</p>
                                <input
                                    type="text"
                                    value={formData.title}
                                    onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
                                    className="form-input flex w-full rounded-lg text-white focus:outline-0 focus:ring-2 focus:ring-[#8c2bee]/50 border border-[#4d3267] bg-[#261933] focus:border-[#8c2bee] h-12 placeholder:text-[#ad92c9] p-3 sm:p-4 text-sm sm:text-base"
                                    placeholder="음악의 제목을 입력하세요"
                                    required
                                />
                            </label>

                            <label className="flex flex-col w-full">
                                <p className="text-white text-base font-medium mb-2">음악에 대한 설명</p>
                                <textarea
                                    value={formData.description}
                                    onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                                    className="form-textarea flex w-full rounded-lg text-white focus:outline-0 focus:ring-2 focus:ring-[#8c2bee]/50 border border-[#4d3267] bg-[#261933] focus:border-[#8c2bee] h-24 sm:h-32 placeholder:text-[#ad92c9] p-3 sm:p-4 text-sm sm:text-base resize-none"
                                    placeholder="음악에 대한 설명을 입력하세요"
                                />
                            </label>
                        </div>
                    </div>


                    {/* AI Metadata Section */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <label className="flex flex-col w-full">
                            <p className="text-white text-base font-medium mb-2">어떤 AI를 사용했나요? (필수)</p>
                            <select
                                value={formData.aiPlatform}
                                onChange={(e) => setFormData(prev => ({ ...prev, aiPlatform: e.target.value }))}
                                className="form-select flex w-full rounded-lg text-white focus:outline-0 focus:ring-2 focus:ring-[#8c2bee]/50 border border-[#4d3267] bg-[#261933] focus:border-[#8c2bee] h-12 p-3 sm:p-4 text-sm sm:text-base"
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
                                    className="mt-2 form-input flex w-full rounded-lg text-white focus:outline-0 focus:ring-2 focus:ring-[#8c2bee]/50 border border-[#4d3267] bg-[#261933] focus:border-[#8c2bee] h-12 placeholder:text-[#ad92c9] p-3 sm:p-4 text-sm sm:text-base"
                                    placeholder="사용하신 AI 플랫폼 이름을 입력하세요"
                                    required
                                />
                            )}
                        </label>

                        <label className="flex flex-col w-full">
                            <p className="text-white text-base font-medium mb-2">사용한 모델 (필수)</p>
                            <input
                                type="text"
                                value={formData.aiModel}
                                onChange={(e) => setFormData(prev => ({ ...prev, aiModel: e.target.value }))}
                                className="form-input flex w-full rounded-lg text-white focus:outline-0 focus:ring-2 focus:ring-[#8c2bee]/50 border border-[#4d3267] bg-[#261933] focus:border-[#8c2bee] h-12 placeholder:text-[#ad92c9] p-3 sm:p-4 text-sm sm:text-base"
                                placeholder="예: v3, v3.5, Udio beta"
                                required
                            />
                        </label>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6">
                        <label className="flex flex-col w-full">
                            <p className="text-white text-base font-medium mb-2">장르</p>
                            <input
                                type="text"
                                value={formData.genre}
                                onChange={(e) => setFormData(prev => ({ ...prev, genre: e.target.value }))}
                                className="form-input flex w-full rounded-lg text-white focus:outline-0 focus:ring-2 focus:ring-[#8c2bee]/50 border border-[#4d3267] bg-[#261933] focus:border-[#8c2bee] h-12 placeholder:text-[#ad92c9] p-3 sm:p-4 text-sm sm:text-base"
                                placeholder="예: Electronic, Lo-fi, Ambient"
                            />
                        </label>

                        <label className="flex flex-col w-full">
                            <p className="text-white text-base font-medium mb-2">분위기 / 태그</p>
                            <input
                                type="text"
                                value={formData.tags}
                                onChange={(e) => setFormData(prev => ({ ...prev, tags: e.target.value }))}
                                className="form-input flex w-full rounded-lg text-white focus:outline-0 focus:ring-2 focus:ring-[#8c2bee]/50 border border-[#4d3267] bg-[#261933] focus:border-[#8c2bee] h-12 placeholder:text-[#ad92c9] p-3 sm:p-4 text-sm sm:text-base"
                                placeholder="예: chill, focus, relaxing (쉼표로 구분)"
                            />
                        </label>
                    </div>

                    {/* Action Buttons */}
                    <div className="flex flex-col-reverse sm:flex-row justify-end gap-3 sm:gap-4 pt-4">
                        <button
                            type="button"
                            onClick={() => navigate('/')}
                            disabled={uploading}
                            className="flex min-w-[120px] cursor-pointer items-center justify-center rounded-lg h-11 sm:h-12 px-6 bg-[#362348] text-white text-sm sm:text-base font-bold hover:bg-[#4d3267] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            취소
                        </button>
                        <button
                            type="submit"
                            disabled={uploading || !formData.file || !formData.aiModel || (formData.aiPlatform === 'other' && !formData.aiPlatformOther)}
                            className="flex min-w-[120px] cursor-pointer items-center justify-center rounded-lg h-11 sm:h-12 px-6 bg-[#8c2bee] text-white text-sm sm:text-base font-bold hover:bg-[#9c3bfe] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {uploading ? '업로드 중...' : '업로드'}
                        </button>
                    </div>
                </form >
            </div >
        </main >
    );
}
