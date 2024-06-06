import React from 'react';
import { Route, Routes } from 'react-router-dom';
import FileUpload from './FileUpload';
import LinksDisplay from './LinksDisplay';
import ProcessedData from './ProcessedData';
import './ProcessedData.css';

function App() {
  return (
   
      <Routes>
        <Route path="/" element={<FileUpload />} />
        <Route path="/links" element={<LinksDisplay />} />
        <Route path="/processeddata" element={<ProcessedData />} />
      </Routes>
   
  );
}

export default App;
