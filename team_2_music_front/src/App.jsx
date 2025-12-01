import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { PlayerProvider } from './context/PlayerContext';
import Header from './components/common/Header';
import MusicPlayer from './components/common/MusicPlayer';
import HomePage from './pages/HomePage';
import UploadPage from './pages/UploadPage';
import ProfilePage from './pages/ProfilePage';
import DetailPage from './pages/DetailPage';
import SearchPage from './pages/SearchPage';

function App() {
  return (
    <BrowserRouter>
      <PlayerProvider>
        <div className="relative flex min-h-screen w-full flex-col bg-[#191022] text-white pb-24">
          <Header />
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/upload" element={<UploadPage />} />
            <Route path="/profile" element={<ProfilePage />} />
            <Route path="/track/:id" element={<DetailPage />} />
            <Route path="/search" element={<SearchPage />} />
          </Routes>
          <MusicPlayer />
        </div>
      </PlayerProvider>
    </BrowserRouter>
  );
}

export default App;
