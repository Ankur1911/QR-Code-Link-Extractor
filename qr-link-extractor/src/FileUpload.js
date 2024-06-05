import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const FileUpload = () => {
  const [file, setFile] = useState();
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a file');
      return;
    }
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:5000/extract-qr', formData);
      navigate('/links', { state: { 
        links: response.data.qr_links, 
        opened: response.data.opened_links || [], 
        failed: response.data.failed_links || [] 
      } });
    } catch (error) {
      setError('Error opening link. Please try again.');
    }
  };

  return (
    <div>
      <h2>Upload File</h2>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Find Links</button>
      </form>
      {error && <p>{error}</p>}
    </div>
  );
};

export default FileUpload;