import React from 'react';
import { useLocation, Link } from 'react-router-dom';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const LinksDisplay = () => {
  const location = useLocation();
  const { links,opened,failed } = location.state || { links: [] ,opened:[],failed:[] };
  // const [selectedLink, setSelectedLink] = useState(null);
  const navigate = useNavigate();

  const handleProcessLink = async (link) => {
    try {
      const response = await axios.post('http://localhost:5000/process-link', { url: link });
      console.log(response.data)
      navigate('/processeddata', { state: { data: response.data } });
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <h2>Extracted Links</h2>
      {links.length > 0 ? (
        <ul>
          {links.map((link, index) => (
            <li key={index}>
              <a href={link} target="_blank" rel="noopener noreferrer">{link}</a>
            </li>
          ))}
        </ul>
      ) : (
        <p>No links found.</p>
      )}
        <h2>Opened Links</h2>
        {opened.length > 0 ? (
        <ul>
          {opened.map((link, index) => (
            <li key={index}>
              <a href={link} target="_blank" rel="noopener noreferrer">{link}</a>
              <button onClick={() => handleProcessLink(link)}>Process Link</button>
            </li>
          ))}
        </ul>
      ) : (
        <p>No Opened links found.</p>
      )}

        <h2>Failed Links</h2>
      {failed.length > 0 ? (
        <ul>
          {failed.map((link, index) => (
            <li key={index}>
              <a href={link} target="_blank" rel="noopener noreferrer">{link}</a>
            </li>
          ))}
        </ul>
      ) : (
        <p>No Failed links found.</p>
      )}
      <Link to="/">Go Back</Link>
    </div>
  );
};

export default LinksDisplay;
