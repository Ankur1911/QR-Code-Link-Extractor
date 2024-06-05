import React from 'react';
import { Route, Routes } from 'react-router-dom';
import FileUpload from './FileUpload';
import LinksDisplay from './LinksDisplay';

function App() {
  return (
   
      <Routes>
        <Route path="/" element={<FileUpload />} />
        <Route path="/links" element={<LinksDisplay />} />
      </Routes>
   
  );
}

export default App;
